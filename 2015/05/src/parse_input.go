package main

import "puzzle"
import "fmt"
import "io/ioutil"
import "os"
import "strings"

func main() {
  b, err := ioutil.ReadFile("input.txt")
  if err != nil {
    fmt.Println(err)
    os.Exit(1)
  }

  nice := 0

  lines := strings.Split(string(b), "\n")
  for _, line := range lines {
    if line != "" {
      fmt.Print(line)
      if puzzle.IsNice(line) {
        nice += 1
        fmt.Print(" => nice\n")
      } else {
        fmt.Print(" => naughty\n")
      }
    }
  }
  fmt.Printf("Total Nice: %d\n", nice)
}

