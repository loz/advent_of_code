package main

import "paper"
import "fmt"
import "io/ioutil"
import "os"

func main() {
  b, err := ioutil.ReadFile("input.txt")
  if err != nil {
    fmt.Println(err)
    os.Exit(1)
  }

  papers := paper.NewPapers(string(b))
  total := 0
  totalRibbon := 0

  for _, paper := range papers {
    total += paper.PaperNeeded
    totalRibbon += paper.RibbonNeeded
  }

  fmt.Printf("Paper required in input: %d\n", total)
  fmt.Printf("Ribbon required in input: %d\n", totalRibbon)
}
