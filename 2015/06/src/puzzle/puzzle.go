package puzzle

import "strings"
//import "fmt"
import "regexp"
import "strconv"

type Puzzle struct {
  lights [1000][1000]int
}

func NewPuzzle(input string) *Puzzle {
  p := Puzzle{}
  lines := strings.Split(input, "\n")
  for _, line := range lines {
    if line != "" {
      process(&p, line)
    }
  }
  //fmt.Printf("Creating New Puzzle From: %s\n", input)
  return &p
}

func (p *Puzzle) LightsOn() uint {
  total := uint(0)
  for x := 0; x < 1000; x++ {
    for y := 0; y < 1000; y++ {
      total += uint(p.lights[x][y])
    }
  }
  return total
}

func process(p *Puzzle, line string) {
  var turnOn bool
  var toggle bool
  re := regexp.MustCompile(`(turn on|turn off|toggle) ([\d]+),([\d]+) through ([\d]+),([\d]+)`)
  matches := re.FindStringSubmatch(line)
  //fmt.Println(line)
  //fmt.Println(matches)
  x1, _ := strconv.Atoi(matches[2])
  y1, _ := strconv.Atoi(matches[3])
  x2, _ := strconv.Atoi(matches[4])
  y2, _ := strconv.Atoi(matches[5])
  //fmt.Println(x1, y1, x2, y2)
  if matches[1] == "turn on" {
    turnOn = true
  } else if matches[1] == "toggle" {
    toggle = true
  }
  for x := x1; x<= x2; x++ {
    for y := y1; y <= y2; y++ {
      if toggle {
        p.lights[x][y] += 2
      } else {
        if turnOn {
          p.lights[x][y] += 1
        } else {
          p.lights[x][y] -= 1
          if p.lights[x][y] < 0 {
            p.lights[x][y] = 0
          }
        }
      }
    }
  }
}
