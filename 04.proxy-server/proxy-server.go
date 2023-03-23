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

var cash map[string]*http.Response

func main() {

	cash = make(map[string]*http.Response)
	readBlackList()

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
	if inBlackList(url) {
		fmt.Println("This url in black list:", url)
		conn.Write([]byte("HTTP/1.1 " + "445" + "\r\n"))
		conn.Write([]byte("\r\n"))
		return
	}
	typeReq := strings.Split(string(buf[:reqLen]), " ")[0]

	var data *http.Response
	var ok bool
	switch typeReq {
	case "GET":
		data, ok = cash[url]
		if ok {
			fmt.Println("Request in cash!")
			break
		}

		data, err = http.Get(url)
		if err != nil {
			println("Error GET request http:", err.Error())
			os.Exit(1)
		}
		cash[url] = data

	case "POST":
		body := bytes.NewReader([]byte(strings.Split(string(buf[:reqLen]), "\r\n\r\n")[1]))
		contentType := strings.Split(
			strings.Split(string(buf[:reqLen]), "\r\n")[1],
			" ",
		)[1]

		data, err = http.Post(url, contentType, body)
		if err != nil {
			println("Error POST request http:", err.Error())
			os.Exit(1)
		}

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

var blackList map[string]struct{}

func readBlackList() {
	blackList = make(map[string]struct{})

	f, _ := os.Open("black-list.txt")
	data := make([]byte, 1024)
	n, _ := f.Read(data)
	for _, s := range strings.Split(string(data[:n]), "\n") {
		blackList[s] = struct{}{}
	}
}

func inBlackList(url string) bool {

	pieces := strings.Split(url, "/")[2:]
	dom := "." + strings.Split(pieces[0], ".")[len(strings.Split(pieces[0], "."))-1]

	_, ok := blackList[dom]
	if ok {
		return true
	}

	prefix := ""
	for i, piece := range pieces {
		if i == 0 {
			prefix += piece
		} else {
			prefix += "/" + piece
		}

		_, ok := blackList[prefix]
		if ok {
			return true
		}
	}
	return false
}
