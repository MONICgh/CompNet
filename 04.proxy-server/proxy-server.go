package main

import (
	"bytes"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"strings"
)

const (
	HOST = "localhost"
	PORT = "3334"
	TYPE = "tcp"
)

func main() {

	request, err := net.Listen(TYPE, HOST+":"+PORT)
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		os.Exit(1)
	}
	defer request.Close()
	fmt.Println("Listening on " + HOST + ":" + PORT)

	for {
		conn, err := request.Accept()
		if err != nil {
			fmt.Println("Error accepting: ", err.Error())
			os.Exit(1)
		}
		go handleRequest(conn)
	}
}

func handleRequest(conn net.Conn) {

	buf := make([]byte, 1024)
	reqLen, err := conn.Read(buf)

	if err != nil {
		fmt.Println("Error reading:", err.Error())
	}

	url := strings.Split(string(buf[:reqLen]), " ")[1][1:]
	typeReq := strings.Split(string(buf[:reqLen]), " ")[0]

	var data *http.Response
	switch typeReq {
	case "GET":
		data, err = http.Get(url)

	case "POST":
		body := bytes.NewReader([]byte(strings.Split(string(buf[:reqLen]), "\r\n\r\n")[1]))
		contentType := strings.Split(
			strings.Split(string(buf[:reqLen]), "\r\n")[1],
			" ",
		)[1]

		data, err = http.Post(url, contentType, body)

	default:
		println("Error request type http:", typeReq)
		os.Exit(1)
	}

	defer func() {
		fmt.Println()
		data.Body.Close()
	}()

	fmt.Println("Request heard:", data.Status, url)

	conn.Write([]byte("HTTP/1.1 " + data.Status + "\r\n"))
	if data.StatusCode >= 300 {
		conn.Write([]byte("\r\n"))
		return
	}

	for header, values := range data.Header {
		for _, value := range values {
			conn.Write([]byte(header + ": " + value + "\r\n"))
		}
	}
	conn.Write([]byte("\r\n"))

	bodyBytes, err := io.ReadAll(data.Body)
	if err != nil {
		println("Error request:", err.Error())
		os.Exit(1)
	}
	conn.Write(bodyBytes)
	conn.Write([]byte("\r\n"))
}
