package puzzle

//import "strconv"
//import "strings"
import "fmt"

type Puzzle struct {
}

func NewPuzzle(input string) *Puzzle {
  p := Puzzle{}
  fmt.Printf("Creating New Puzzle From: %s\n", input)
  return &p
}
