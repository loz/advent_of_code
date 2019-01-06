package floors

import "testing"

func TestOpenIncreasesFloor(t *testing.T) {
  var floor Floors = *NewFloors("(((")
  if floor.Level != 3 {
    t.Errorf("Level incorrect, got: %d, want: %d", floor.Level, 3)
  }
}

func TestCloseDecreasesFloor(t *testing.T) {
  var floor Floors = *NewFloors(")))")
  if floor.Level != -3 {
    t.Errorf("Level incorrect, got: %d, want: %d", floor.Level, -3)
  }
}

func TestBalanceMatchesExample(t *testing.T) {
  var floor Floors = *NewFloors(")())())")
  if floor.Level != -3 {
    t.Errorf("Level incorrect, got: %d, want: %d", floor.Level, -3)
  }
}

func TestDetectsFirstMoveToBasement(t *testing.T) {
  var floor Floors = *NewFloors(")))")
  if floor.FirstBasement != 1 {
    t.Errorf("Level incorrect, got: %d, want: %d", floor.FirstBasement, 1)
  }
}
