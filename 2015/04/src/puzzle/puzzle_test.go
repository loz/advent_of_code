package puzzle

import "testing"

func TestCalculatesCoinForStart(t *testing.T) {
  coin := MineCoin("abcdef", 5)
  expected := 609043

  if coin.Number != expected {
    t.Errorf("Failed, expected %d, got %d", expected, coin.Number)
  }
}

func TestCalculatesCoinForSecondExample(t *testing.T) {
  coin := MineCoin("pqrstuv", 5)
  expected := 1048970

  if coin.Number != expected {
    t.Errorf("Failed, expected %d, got %d", expected, coin.Number)
  }
}
