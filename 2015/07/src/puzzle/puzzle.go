package puzzle

import "strconv"

//import "strings"

import (
	"fmt"
	"strings"
)

type Puzzle struct {
	wires map[string]uint16
}

func NewPuzzle(input string) *Puzzle {
	p := Puzzle{}
	//fmt.Printf("Creating New Puzzle From: %s\n", input)
	p.wires = make(map[string]uint16)

	lines := strings.Split(input, "\n")
	for _, line := range lines {
		if line != "" {
			process(&p, line)
		}
	}

	return &p
}

func process(p *Puzzle, line string) {
	fmt.Printf("Parsing Line >>%s<<\n", line)
	tokens := strings.Split(line, " ")
	numTokens := len(tokens)
	//fmt.Printf("%d Tokens Parsed\n", numTokens)
	if numTokens == 3 { // X -> Y
		v1, dest := tokens[0], tokens[2]
		//fmt.Printf("A: %s, B: %s, C: %s\n", a, b, c)
		val, err := strconv.ParseUint(v1, 10, 16)
		if err != nil {
			//Non Literal
			p.wires[dest] = p.wires[v1]
		} else {
			p.wires[dest] = uint16(val)
		}
		fmt.Printf("    %d -> %s\n", p.wires[dest], dest)
	} else if numTokens == 4 { // OP X -> Y
		v1, dest := tokens[1], tokens[3]
		p.wires[dest] = (^p.wires[v1])
		fmt.Printf("    %d -> %s\n", p.wires[dest], dest)
	} else if numTokens == 5 { // X OP Y -> Z
		v1, op, v2, dest := tokens[0], tokens[1], tokens[2], tokens[4]
		//fmt.Printf("Operator: %s, V1:%s, V2:%s -> D:%s\n", op, v1, v2, dest)
		if op == "AND" {
			p.wires[dest] = p.wires[v1] & p.wires[v2]
		} else if op == "OR" {
			p.wires[dest] = p.wires[v1] | p.wires[v2]
		} else if op == "LSHIFT" {
			val, err := strconv.ParseUint(v2, 10, 16)
			if err != nil {
				fmt.Printf("Error Parsing Int: %s\n", err)
			}
			p.wires[dest] = p.wires[v1] << uint16(val)
		} else if op == "RSHIFT" {
			val, err := strconv.ParseUint(v2, 10, 16)
			if err != nil {
				fmt.Printf("Error Parsing Int: %s\n", err)
			}
			p.wires[dest] = p.wires[v1] >> uint16(val)
		} else {
			fmt.Print("Error: Unknown Operator")
		}
		fmt.Printf("    %d -> %s\n", p.wires[dest], dest)
	}
}
