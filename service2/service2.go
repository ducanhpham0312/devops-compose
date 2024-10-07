package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os/exec"
	"strings"
)

// Struct to hold system info
type SystemInfo struct {
    IPAddress  string `json:"ip_address"`
    Processes  string `json:"processes"`
    DiskSpace  string `json:"disk_space"`
    Uptime     string `json:"uptime"`
}

// Fetch system information
func getSystemInfo() SystemInfo {
    ip, _ := exec.Command("hostname", "-i").Output()
    processes, _ := exec.Command("ps", "-ax").Output()
    diskSpace, _ := exec.Command("df").Output()
    uptime, _ := exec.Command("uptime").Output()

    return SystemInfo{
        IPAddress:  string(ip),
        Processes:  string(processes),
        DiskSpace:  string(diskSpace),
        Uptime:     strings.TrimSpace(string(uptime)),
    }
}

// Handler to return system information
func infoHandler(w http.ResponseWriter, r *http.Request) {
    systemInfo := getSystemInfo()

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(systemInfo)
}

func main() {
    http.HandleFunc("/info", infoHandler)
    fmt.Println("Service2 running on port 8200")
    http.ListenAndServe(":8200", nil)
}
