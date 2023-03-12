package main

import (
	"bytes"
	"crypto/sha256"
	"fmt"

)


func main(){
    chain := InitBlockChain()
    chain.AddBlock("First Block")
    chain.AddBlock("Second Block")
    chain.AddBlock("Third Block")

    for _, block := range chain.blocks{
        fmt.Printf("Previous Hash: %x\n", block.PrevHash)
        fmt.Printf("Data in Block: %s\n", block.Data)
        fmt.Printf("Hash: %x\n", block.Hash)
    }
}
