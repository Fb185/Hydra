package main

import (
	"fmt"
	"os"
	"runtime"
	"strconv"

	"github.com/fb185/MediChain/blockchain"
)

type CommandLine struct {
	blockchain *blockchain.BlockChain
}

func (cli *CommandLine) printUsage() {
	fmt.Println("Usage:")
	fmt.Println("Usage:")
	fmt.Println("Usage:")
}

func (cli *CommandLine) validateArgs() {
	if len(os.Args) < 2 {
		cli.printUsage()
		runtime.Goexit()
	}
}

func (cli *CommandLine) addBlock(data string){
    cli.blockchain.AddBlock(data)
    fmt.Println("Added Block")
}

func(cli *CommandLine) printChain(){
    iter := cli.blockchain.Iterator()
    for{
        block := iter.Next()
		fmt.Printf("Prev hash: %x\n", block.PrevHash)
		fmt.Printf("Data in Block: %s\n", block.Data)
		fmt.Printf("Hash : %x\n", block.Hash)

		pow := blockchain.NewProof(block)
		fmt.Printf("PoW: %s\n", strconv.FormatBool(pow.Validate()))
		fmt.Println()

        if len(block.PrevHash) == 0{
            break
        }

    }
}

func main() {
	chain := blockchain.InitBLockChain()
	chain.AddBlock("First")
	chain.AddBlock("Second")
	chain.AddBlock("Third")

	for _, block := range chain.Blocks {
	}

}

// 20:41
