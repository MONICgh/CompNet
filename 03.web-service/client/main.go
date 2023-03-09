package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"os"
)

const (
	TYPE = "tcp"
)

func main() {

	if len(os.Args) != 4 {
		println("Must be 4 args")
		os.Exit(1)
	}

	host := os.Args[1]
	port := os.Args[2]
	fileName := os.Args[3]

	conn, err := net.Dial(TYPE, host+":"+port)
	if err != nil {
		println("Dial failed:", err.Error())
		os.Exit(1)
	}
	defer conn.Close()

	_, err = conn.Write([]byte("GET /" + fileName + " \r\n"))
	if err != nil {
		println("Write data failed:", err.Error())
		os.Exit(1)
	}

	reader := bufio.NewReader(conn)
	for {
		lineStatus, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading from server:", err)
			os.Exit(1)
		}
		fmt.Print(lineStatus)
		if lineStatus == "\r\n" {
			break
		}
	}

getDataFile:
	for {
		lineData, err := reader.ReadString('\n')
		switch err {
		case io.EOF:
			break getDataFile
		case nil:
			fmt.Print(lineData)
		default:
			fmt.Println("Error reading from server:", err)
			os.Exit(1)
		}
	}
}
