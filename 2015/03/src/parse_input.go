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

  fmt.Printf("Houses Visited With Santa: %d\n", answer.Houses)

  answer = puzzle.NewPuzzleWithRobot(string(b))

  fmt.Printf("Houses Visited With Santa+Robot: %d\n", answer.Houses)
}
