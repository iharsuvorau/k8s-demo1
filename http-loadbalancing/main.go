package main

import (
	"net"
	"net/http"
	"os"
)

func main() {
	http.HandleFunc("/", rootHandler)
	http.ListenAndServe(":8080", nil)
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	hostname, err := os.Hostname()
	if err != nil {
		panic(err)
	}

	addrs, err := net.InterfaceAddrs()
	if err != nil {
		panic(err)
	}

	for _, address := range addrs {
		if ipnet, ok := address.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				hostname = hostname + " " + ipnet.IP.String()
			}
		}
	
	}
	w.Write([]byte("Hello from " + hostname))
}
