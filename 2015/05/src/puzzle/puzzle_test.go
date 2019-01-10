package puzzle

import "testing"

func TestThreeVowelsOnlyAreNaughty(t *testing.T) {
  p := IsNice("aei")
  if p != false {
    t.Error("Error, value was nice when not expected")
  }
}

func TestTwoOfTheSameLettersAreNaughty(t *testing.T) {
  p := IsNice("zxcvbwwsf")
  if p != false {
    t.Error("Error, value was nice when not expected")
  }
}

func TestBothAreNice(t *testing.T) {
  p := IsNice("aaeiou")
  if p != true {
    t.Error("Error, value was not nice when was expected")
  }
}

func TestAB_CD_PQ_XY_AreNaughty(t *testing.T) {
  p := IsNice("abbbbeiou")
  if p == true {
    t.Error("Error, value was nice when was not expected")
  }
}

func TestPairRepeatedIsNewNice(t *testing.T) {
  p := IsNewNice("aaa")
  if p == true {
    t.Error("Error, value was nice when was not expected")
  }

  p = IsNewNice("xyxy")
  if p == false {
    t.Error("Error, value was not nice when was expected")
  }

  p = IsNewNice("aabcdefgaa")
  if p == false {
    t.Error("Error, value was not nice when was expected")
  }
}
