package puzzle

import "testing"

func TestDeliversTo2HousesMovingEast(t *testing.T) {
  puzzle := NewPuzzle(">")

  if puzzle.Houses != 2 {
    t.Errorf("Houses incorrect, got: %d, want: %d", puzzle.Houses, 2)
  }
}

func TestDeliversToHousesMoreThanOnce(t *testing.T) {
  puzzle := NewPuzzle("^>v<")

  if puzzle.Houses != 4 {
    t.Errorf("Houses incorrect, got: %d, want: %d", puzzle.Houses, 4)
  }
}

func TestWithRobotDeliversToHousesMoreThanOnce(t *testing.T) {
  puzzle := NewPuzzleWithRobot("^v")

  if puzzle.Houses != 3 {
    t.Errorf("Houses incorrect, got: %d, want: %d", puzzle.Houses, 3)
  }

  puzzle = NewPuzzleWithRobot("^v^v^v^v^v")

  if puzzle.Houses != 11 {
    t.Errorf("Houses incorrect, got: %d, want: %d", puzzle.Houses, 11)
  }
}
