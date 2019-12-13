class Puzzle

  property matches = [] of String

  def process(str)
    matches = [] of String
    str.each_line do |line|
      matches << line if tls?(line)
    end
    @matches = matches
  end

  def result
    p @matches.size
  end

  def tls?(str)
    matches = str.match /(\w)(\w)\2\1/
    if matches
      badmatch = str.match /\[(\w)(\w)\2\1\]/
      if badmatch
        false
      else
        badmatch = matches[0].match /(\w)\1\1\1/
        if badmatch
          #Search rest of string
          tls?(matches.post_match)
        else
          true
        end
      end
    else
      false
    end
  end

end
