package paper

import "testing"

func TestCalculatesPaperForDimensions(t *testing.T) {
  var paper Paper = *NewPaper("2x3x4")
  if paper.PaperNeeded != 58 {
    t.Errorf("Level incorrect, got: %d, want: %d", paper.PaperNeeded, 58)
  }
}

func TestCalculatesExtraFromSmallestSide(t *testing.T) {
  var paper Paper = *NewPaper("4x2x3")
  if paper.PaperNeeded != 58 {
    t.Errorf("Level incorrect, got: %d, want: %d", paper.PaperNeeded, 58)
  }
}

func TestCalculatesRibbonNeeded(t *testing.T) {
  var paper Paper = *NewPaper("4x2x3")
  if paper.RibbonNeeded != 34 {
    t.Errorf("Level incorrect, got: %d, want: %d", paper.RibbonNeeded, 34)
  }
}


func TestCanProcessAllPaper(t *testing.T) {
  var papers = NewPapers("4x2x3\n1x1x10\n")
  total := 0

  for _, paper := range papers {
    total += paper.PaperNeeded
  }

  if total != 101 {
    t.Errorf("Level incorrect, got: %d, want: %d", total, 101)
  }
}
