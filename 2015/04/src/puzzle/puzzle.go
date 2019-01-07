package puzzle

import "strconv"
//import "strings"
import "fmt"
import "crypto/md5"
import "io"

type Coin struct {
  Number int
}

func isMinedCoin(hash string, length int) bool {
  for i := 0; i < length; i++ {
    if hash[i] != '0' {
      return false
    }
  }
  return true
}

func MineCoin(base string, length int) *Coin {
  c := Coin{}
  mined := false
  c.Number = -1
  for mined != true {
    c.Number += 1
    coin := base + strconv.Itoa(c.Number)
    hash := md5.New()
    io.WriteString(hash, coin)
    coinhash := fmt.Sprintf("%x", hash.Sum(nil))
    mined = isMinedCoin(coinhash, length)
  }
  return &c
}
