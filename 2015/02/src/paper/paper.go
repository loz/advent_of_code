package paper

import "strconv"
import "strings"
import "fmt"

type Paper struct {
  Length int
  Width int
  Height int
  PaperNeeded int
  RibbonNeeded int
}

func NewPapers(lines_string string) []*Paper {
  papers := make([]*Paper,0)
  lines := strings.Split(lines_string, "\n")
  for _, line := range lines {
    if line != "" {
      papers = append(papers, NewPaper(line))
    }
  }
  return papers
}

func NewPaper(details string) *Paper {
 p := Paper{}
 dimensions := strings.Split(details, "x")

 l, err := strconv.Atoi(dimensions[0])
 if err != nil {
  fmt.Print(err)
 }
 p.Length = l

 w, err := strconv.Atoi(dimensions[1])
 if err != nil {
  fmt.Print(err)
 }
 p.Width = w


 h, err := strconv.Atoi(dimensions[2])
 if err != nil {
  fmt.Print(err)
 }
 p.Height = h

 p.PaperNeeded = (2*l*w) + (2*w*h) + (2*h*l)
 p.RibbonNeeded = l*w*h

 if l <= w {
  if w <= h {
    p.PaperNeeded += (l*w)
    p.RibbonNeeded += (l+l+w+w)
  } else {
    p.PaperNeeded += (l*h)
    p.RibbonNeeded += (l+l+h+h)
  }
 } else { // L > W
  if h <= w { //L > W >  H
    p.PaperNeeded += (w*h)
    p.RibbonNeeded += (w+w+h+h)
  } else { // L > W < H
    if l >= h { // L > H > W
      p.PaperNeeded += (h*w)
      p.RibbonNeeded += (w+w+h+h)
    } else { // L < H > W
      p.PaperNeeded += (l*w)
      p.RibbonNeeded += (w+w+l+l)
    }
  }
 }
 return &p
}
