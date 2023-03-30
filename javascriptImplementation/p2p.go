package main

import (
	"encoding/gob"
	"fmt"
	"log"
	"net"
)

const (
	protocol      = "tcp"
	nodeVersion   = 1
	commandLength = 12
)

var nodeAddress string
var knownNodes = []string{"localhost:3000"}

type command [commandLength]byte

func main() {
	// Initialize the blockchain and wallets here

	nodeID := 1
	nodeAddress = fmt.Sprintf("localhost:%d", 3000+nodeID)

	server, err := net.Listen(protocol, nodeAddress)
	if err != nil {
		log.Panic(err)
	}
	defer server.Close()

	for {
		conn, err := server.Accept()
		if err != nil {
			log.Panic(err)
		}

		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	// Replace this with your own message struct
	var message interface{}
	decoder := gob.NewDecoder(conn)
	err := decoder.Decode(&message)
	if err != nil {
		log.Panic(err)
	}

	// Process the received message here
}

func sendMessage(addr string, message interface{}) {
	conn, err := net.Dial(protocol, addr)
	if err != nil {
		fmt.Printf("%s is not available\n", addr)
		return
	}
	defer conn.Close()

	encoder := gob.NewEncoder(conn)
	err = encoder.Encode(message)
	if err != nil {
		log.Panic(err)
	}
}
