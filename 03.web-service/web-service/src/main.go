package main

import (
	"fmt"
	"io"
	"net"
	"os"
	"strings"
)

const (
	CONN_HOST = "localhost"
	CONN_PORT = "3334"
	CONN_TYPE = "tcp"
)

func main() {
	l, err := net.Listen(CONN_TYPE, CONN_HOST+":"+CONN_PORT)
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		os.Exit(1)
	}
	defer l.Close()
	fmt.Println("Listening on " + CONN_HOST + ":" + CONN_PORT)
	for {
		conn, err := l.Accept()
		if err != nil {
			fmt.Println("Error accepting: ", err.Error())
			os.Exit(1)
		}
		println()
		go handleRequest(conn)
	}
}

func getFileData(fileName string) ([]byte, error) {

	f, err := os.Open(fileName)

	if err != nil {
		return nil, err
	}
	defer f.Close()
	buf := make([]byte, 1024)
	for {
		n, err := f.Read(buf)
		if err == io.EOF {
			break
		}
		if err != nil {
			fmt.Println(err)
			continue
		}
		if n > 0 {
			return buf[:n], nil
		}
	}

	return nil, nil
}

func handleRequest(conn net.Conn) {

	defer conn.Close()

	buf := make([]byte, 1024)
	reqLen, err := conn.Read(buf)

	if err != nil {
		fmt.Println("Error reading:", err.Error())
	}
	getReq := strings.Split(string(buf[:reqLen]), " ")
	data, err := getFileData(getReq[1][1:])

	if err != nil {
		conn.Write([]byte("HTTP/1.1 404 Not Found\r\n"))
		conn.Write([]byte("\r\n"))
		return
	}

	conn.Write([]byte("HTTP/1.1 200 OK\r\n"))
	conn.Write([]byte(fmt.Sprintf("Content-Length: %d\r\n", len(data))))
	conn.Write([]byte("Content-Type: text/plain\r\n"))
	conn.Write([]byte("\r\n"))
	conn.Write([]byte(string(data)))
	conn.Write([]byte("\r\n"))
}
