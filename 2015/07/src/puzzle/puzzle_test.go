package puzzle

import "testing"

func TestNumberSentToWire(t *testing.T) {
	p := NewPuzzle("123 -> x")

	if p.wires["x"] != uint16(123) {
		t.Error("Expexted wire x to be set to 123")
	}
}

func TestNonLiteralSentToWire(t *testing.T) {
	p := NewPuzzle("123 -> x\nx -> y")

	if p.wires["y"] != uint16(123) {
		t.Error("Expexted wire y to be set to 123")
	}
}

func TestBitwiseAND(t *testing.T) {
	p := NewPuzzle("123 -> x\n345 -> y\nx AND y -> z")

	expected := uint16(123 & 345)
	if p.wires["z"] != expected {
		t.Errorf("Expexted wire z to be set to %d, got %d", expected, p.wires["z"])
	}
}

func TestLeftShift(t *testing.T) {
	p := NewPuzzle("123 -> x\nx LSHIFT 2 -> y")

	expected := uint16(123 << 2)
	if p.wires["y"] != expected {
		t.Errorf("Expexted wire y to be set to %d, got %d", expected, p.wires["y"])
	}
}

func TestOR(t *testing.T) {
	p := NewPuzzle("123 -> x\n456 -> y\nx OR y -> z")

	expected := uint16(123 | 456)
	if p.wires["z"] != expected {
		t.Errorf("Expexted wire z to be set to %d, got %d", expected, p.wires["z"])
	}
}

func TestNOT(t *testing.T) {
	p := NewPuzzle("123 -> x\nNOT x -> y")

	expected := (^uint16(123))
	if p.wires["y"] != expected {
		t.Errorf("Expexted wire y to be set to %d, got %d", expected, p.wires["y"])
	}
}
func TestRightShift(t *testing.T) {
	p := NewPuzzle("123 -> x\nx RSHIFT 2 -> y")

	expected := uint16(uint16(123) >> 2)
	if p.wires["y"] != expected {
		t.Errorf("Expexted wire y to be set to %d, got %d", expected, p.wires["y"])
	}
}
