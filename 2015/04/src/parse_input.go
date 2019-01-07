package main

import "puzzle"
import "fmt"

func main() {
  coin := puzzle.MineCoin("iwrupvqb", 6)
  fmt.Printf("The Mined Number: %d\n", coin.Number)
}
