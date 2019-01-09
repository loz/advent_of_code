package puzzle

import "testing"

func TestExample(t *testing.T) {
  p := NewPuzzle("example")
  if p == nil {
    t.Error("Error creating new Puzzle")
  }
}
