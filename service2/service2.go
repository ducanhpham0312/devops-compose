package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"os/exec"
)

// Struct to hold system info
type SystemInfo struct {
	IPAddress string `json:"ip_address"`
	Processes string `json:"processes"`
	DiskSpace string `json:"disk_space"`
	Uptime    string `json:"uptime"`
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
	systemInfo := getSystemInfo()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(systemInfo)
}

func main() {
	// Create a channel to listen for OS signals
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	http.HandleFunc("/info", infoHandler)

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
