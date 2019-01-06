package main

import "floors"
import "fmt"
import "io/ioutil"

func main() {
  b, err := ioutil.ReadFile("input.txt")
  if err != nil {
    fmt.Print(err)
  }

  f := floors.NewFloors(string(b))
  fmt.Printf("Floors in input: %d\n", f.Level)
  fmt.Printf("First in Basement: %d\n", f.FirstBasement)
}
