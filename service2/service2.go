package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"
)

// Struct to hold system info
type SystemInfo struct {
	IPAddress string `json:"ip_address"`
	Processes string `json:"processes"`
	DiskSpace string `json:"disk_space"`
	Uptime    string `json:"uptime"`
}
var (
	state     = "INIT"
	stateLog  []string
	stateLock sync.Mutex
)

func manageState(w http.ResponseWriter, r *http.Request) {
	stateLock.Lock()
	defer stateLock.Unlock()

	if r.Method == http.MethodGet {
			// Return the current state without forcing re-authentication
			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(state)
			w.WriteHeader(http.StatusOK)
			return
}

// Read and log the raw request body
	body, err := io.ReadAll(r.Body)
	if err != nil {
			http.Error(w, `Unable to read request body: ` + err.Error(), http.StatusBadRequest)
			return
	}

	// Handle state change requests
	newState := strings.TrimSpace(strings.ToUpper(string(body)))

	if newState != "INIT" && newState != "RUNNING" && newState != "PAUSED" && newState != "SHUTDOWN" {
			http.Error(w, `ERROR: Invalid state: `+newState, http.StatusBadRequest)
			return
	}

	if newState == state {
			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode("No change in state")
			w.WriteHeader(http.StatusOK)
			return
	}

	// Handle INIT state
	if newState == "INIT" {
			stateLog = append(stateLog, time.Now().UTC().Format(time.RFC3339) + ": " + state + " -> INIT")
			state = "INIT"
			w.Header().Set("Content-Type", "application/json")
			w.Header().Set("WWW-Authenticate", `Basic realm="Restricted Access"`)
			w.WriteHeader(http.StatusUnauthorized)
			json.NewEncoder(w).Encode("State changed to INIT. Please re-authenticate.")
			return
	}

	// Handle RUNNING state
	if newState == "RUNNING" {
		if r.Header.Get("Authorization") == "" {
			http.Error(w, `ERROR: Login required to change state to RUNNING`, http.StatusForbidden)
			return
		}
		if state != "INIT" && state != "PAUSED" {
			http.Error(w, `ERROR: Cannot change state to RUNNING from `+ state, http.StatusForbidden)
			return
		}

		stateLog = append(stateLog, time.Now().UTC().Format(time.RFC3339) + ": " + state + " -> RUNNING")
		state = "RUNNING"
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode("State changed to RUNNING")
		w.WriteHeader(http.StatusOK)
		return
	}

	// Handle PAUSED state
	if newState == "PAUSED" {
		if state != "RUNNING" {
			http.Error(w, `ERROR: Cannot change state to PAUSED from `+ state, http.StatusForbidden)
			return
		}
		stateLog = append(stateLog, time.Now().UTC().Format(time.RFC3339) + ": " + state + " -> PAUSED")
		state = "PAUSED"
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode("State changed to PAUSED")
		w.WriteHeader(http.StatusOK)
		return
	}

	// Handle SHUTDOWN state
	if newState == "SHUTDOWN" {
		if state != "RUNNING" && state != "PAUSED" {
			http.Error(w, `ERROR: Cannot change state to SHUTDOWN from `+ state, http.StatusForbidden)
			return
		}
		stateLog = append(stateLog, time.Now().UTC().Format(time.RFC3339) + ": " + state + " -> SHUTDOWN")
		state = "SHUTDOWN"
		shutdownContainers()
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode("State changed to SHUTDOWN. Stopping all containers...")
		w.WriteHeader(http.StatusOK)
		return
	}
}

func shutdownContainers() {
	// Shutdown all running Docker containers
	defer func() {
		if r := recover(); r != nil {
			log.Printf("Unexpected error during SHUTDOWN: %v", r)
		}
	}()

	// Get IDs of all running containers
	cmd := exec.Command("docker", "ps", "-q")
	output, err := cmd.Output()
	if err != nil {
		log.Printf("Error during container shutdown: %v", err)
		return
	}

	containerIDs := strings.Fields(string(output))
	if len(containerIDs) > 0 {
		// Stop the running containers
		cmd = exec.Command("docker", append([]string{"stop"}, containerIDs...)...)
		stopOutput, err := cmd.Output()
		if err != nil {
			log.Printf("Error during container shutdown: %v", err)
			return
		}

		stoppedContainers := strings.Fields(string(stopOutput))
		log.Printf("Stopped containers: %v", stoppedContainers)

		// Remove the stopped containers
		cmd = exec.Command("docker", append([]string{"rm"}, stoppedContainers...)...)
		rmOutput, err := cmd.Output()
		if err != nil {
			log.Printf("Error during container removal: %v", err)
			return
		}

		removedContainers := strings.Fields(string(rmOutput))
		log.Printf("Removed containers: %v", removedContainers)
	} else {
		log.Println("No running containers to stop.")
	}
}
// Fetch system information
func getSystemInfo() SystemInfo {
	ip, _ := exec.Command("hostname", "-i").Output()
	processes, _ := exec.Command("ps", "-ax").Output()
	diskSpace, _ := exec.Command("df").Output()
	uptime, _ := exec.Command("uptime").Output()

	return SystemInfo{
		IPAddress: string(ip),
		Processes: string(processes),
		DiskSpace: string(diskSpace),
		Uptime:    strings.TrimSpace(string(uptime)),
	}
}

// Handler to return system information
func infoHandler(w http.ResponseWriter, r *http.Request) {
	if state != "RUNNING" {
		http.Error(w, "Service2 is not in RUNNING state", http.StatusServiceUnavailable)
		return
	}
	systemInfo := getSystemInfo()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(systemInfo)
}

func main() {
	// Create a channel to listen for OS signals
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	http.HandleFunc("/info", infoHandler)
	http.HandleFunc("/state", manageState)

	go func() {
		log.Println("Service2 running on port 8200")
		if err := http.ListenAndServe(":8200", nil); err != nil {
			log.Fatalf("Error starting the server: %v", err)
		}
	}()

	// Block until receive a termination signal (SIGINT or SIGTERM) from e.g., Docker
	sig := <-sigs
	log.Printf("Received signal %s, shutting down service2...", sig)

	log.Println("Service2 has shut down.")
	os.Exit(0)
}
