package puzzle

import "testing"

func TestTurnOnFlipsLightsOn(t *testing.T) {
  p := NewPuzzle("turn on 10,10 through 20,20")

  if p.lights[9][9] != 0 {
    t.Error("Lights not off when expected at 9,9")
  }
  if p.lights[21][20] != 0 {
    t.Error("Lights not off when expected at 21,20")
  }
  if p.lights[10][10] != 1 {
    t.Error("Lights not on when expected at 10,10")
  }
  if p.lights[20][20] != 1 {
    t.Error("Lights not on when expected at 20,20")
  }
  if p.lights[15][15] != 1 {
    t.Error("Lights not on when expected at 15,15")
  }
}

func TestTurnOffFlipsLightsOff(t *testing.T) {
  input := `turn on 0,0 through 999,999
turn off 10,10 through 20,20
`
  p := NewPuzzle(input)

  if p.lights[10][10] != 0 {
    t.Error("Lights not off when expected at 10,10")
  }
  if p.lights[20][20] != 0 {
    t.Error("Lights not off when expected at 20,20")
  }
  if p.lights[15][15] != 0 {
    t.Error("Lights not off when expected at 15,15")
  }
}

func TestOffDoesNotGoBelowZero(t *testing.T) {
  input := `turn off 0,0 through 999,999`
  p := NewPuzzle(input)

  if p.lights[6][6] != 0 {
    t.Errorf("Lights not 0 when expected at 0,0, got: %d", p.lights[6][6])
  }
}

func TestToggleIncreasesBy2(t *testing.T) {
  input := `turn on 0,0 through 999,999
turn off 10,10 through 20,20
toggle 5,5 through 15,15
`
  p := NewPuzzle(input)

  if p.lights[6][6] != 3 {
    t.Errorf("Lights not 3 when expected at 6,6, got: %d", p.lights[6][6])
  }
  if p.lights[12][12] != 2 {
    t.Errorf("Lights not 2 when expected at 12,12, got: %d", p.lights[12][12])
  }
  if p.lights[18][18] != 0 {
    t.Error("Lights not 0 when expected at 18,18")
  }
}

func TestCanCountOn(t *testing.T) {
  input := `turn on 0,0 through 999,999
turn off 10,10 through 20,20
`
  p := NewPuzzle(input)

  expected := uint(1000000-(11*11))
  actual := p.LightsOn()
  if actual != expected {
    t.Errorf("Expected %d, got %d Lights On", expected, actual)
  }
}
