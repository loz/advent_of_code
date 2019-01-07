package main

import "puzzle"
import "fmt"
import "io/ioutil"
import "os"

func main() {
  b, err := ioutil.ReadFile("input.txt")
  if err != nil {
    fmt.Println(err)
    os.Exit(1)
  }

  answer := puzzle.NewPuzzle(string(b))
  fmt.Println(answer)
}
