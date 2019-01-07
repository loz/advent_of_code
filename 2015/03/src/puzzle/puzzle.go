package puzzle

//import "fmt"

type Coord struct {
  X int
  Y int
}

type Puzzle struct {
  Houses int
  Map map[Coord]int
}

func NewPuzzleWithDeliverers(directions string, deliverers []Coord) *Puzzle {
  current := deliverers[0]
  num_people := len(deliverers)
  p := Puzzle{}
  p.Map = make(map[Coord]int)
  p.Map[current] = 1
  for step, move := range directions {
    current := deliverers[step%num_people]
    //fmt.Println(current)
    if move == '>' {
      current = Coord{current.X+1,current.Y}
    }else if move == '^' {
      current = Coord{current.X,current.Y-1}
    }else if move == '<' {
      current = Coord{current.X-1,current.Y}
    }else if move == 'v' {
      current = Coord{current.X,current.Y+1}
    }
    p.Map[current] = 1
    deliverers[step%num_people] = current
  }
  p.Houses = len(p.Map)
  return &p
}

func NewPuzzleWithRobot(directions string) *Puzzle {
  santa := Coord{0,0}
  robot := Coord{0,0}
  people := make([]Coord, 2)
  people[0] = santa
  people[1] = robot
  return NewPuzzleWithDeliverers(directions, people)
}

func NewPuzzle(directions string) *Puzzle {
  current := Coord{0,0}
  people := make([]Coord, 1)
  people[0] = current
  return NewPuzzleWithDeliverers(directions, people)
}
