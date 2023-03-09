package main

import (
	"fmt"
	"io"
	"net"
	"os"
	"strconv"
	"strings"
)

const (
	HOST      = "localhost"
	PORT      = "3334"
	TYPE      = "tcp"
	FILE_SIZE = 1 << 13
)

func main() {

	concurrencyLevel := 1
	var err error

	if len(os.Args) >= 2 {
		concurrencyLevel, err = strconv.Atoi(os.Args[1])
		if err != nil {
			fmt.Println("Arg must be int:", err.Error())
			os.Exit(1)
		}
	}

	ansListen, err := net.Listen(TYPE, HOST+":"+PORT)
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		os.Exit(1)
	}
	defer ansListen.Close()
	fmt.Println("Listening on " + HOST + ":" + PORT)
	for {
		conn, err := ansListen.Accept()
		if err != nil {
			fmt.Println("Error accepting: ", err.Error())
			os.Exit(1)
		}

		go handleRequest(conn, make(chan bool, concurrencyLevel))
	}
}

func getFileData(fileName string) ([]byte, error) {

	f, err := os.Open(fileName)

	if err != nil {
		return nil, err
	}
	defer f.Close()
	buf := make([]byte, FILE_SIZE)
	for {
		n, err := f.Read(buf)
		switch err {
		case io.EOF:
			break
		case nil:
			return buf[:n], nil
		default:
			fmt.Println(err)
			continue
		}
	}
}

func handleRequest(conn net.Conn, sem chan bool) {

	sem <- true
	defer func() {
		<-sem
		conn.Close()
	}()

	buf := make([]byte, FILE_SIZE)
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
