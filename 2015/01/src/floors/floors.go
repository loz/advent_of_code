package floors

type Floors struct {
  Level int
  FirstBasement int
}

func NewFloors(details string) *Floors {
 p := Floors{}
 firstBasement := false
 //for index, runeValue := range details {
 for index, runeValue := range details {
  if runeValue == '(' {
    p.Level = p.Level + 1
  } else if runeValue == ')' {
    p.Level = p.Level - 1
  }
  if p.Level < 0 && !firstBasement {
    p.FirstBasement = index+1
    firstBasement = true
  }
 }
 return &p
}
