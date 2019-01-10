package puzzle

//import "strconv"
//import "strings"
import "fmt"
import "regexp"

func IsNewNice(input string) bool {
  return false
}

func IsNice(input string) bool {
  hasForbidden, err := regexp.MatchString("ab|cd|pq|xy", input)
  if err != nil || hasForbidden {
    return false
  }

  hasThreeVowels, err := regexp.MatchString("(.*[aeiou]){3}", input)
  if err != nil {
    return false
  }

  matcher, err := regexp.CompilePOSIX(`([:alpha:])\1+`)
  if err != nil {
    fmt.Print(err)
  }

  //hasTwoTheSame, err := regexp.MatchString("aa|bb|cc|dd|ee|ff|gg|hh|ii|jj|kk|ll|mm|nn|oo|pp|qq|rr|ss|tt|uu|vv|ww|xx|yy|zz", input)
  hasTwoTheSame := matcher.MatchString(input)
  if err != nil {
    return false
  }

  return hasTwoTheSame && hasThreeVowels
}
