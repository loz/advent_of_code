class Puzzle

  property matches = [] of String

  def process(str)
    matches = [] of String
    str.each_line do |line|
      if ssl?(line) 
        puts "T: #{line}"
        matches << line
      else
        puts "F: #{line}"
      end
    end
    @matches = matches
  end

  def result
    p @matches.size
  end

  def mask_hype(str)
    masked = ""
    masking = false
    hype = ""
    hypes = [] of String
    str.each_char do |ch|
      if ch == '['
        masking = true
        masked += '['
      elsif ch == ']'
        masking = false
        masked += "]"
        hypes << hype
        hype = ""
      elsif masking
        masked += "*"
        hype += ch
      else
        masked += ch
      end
    end
    {masked,hypes}
  end

  def ssl?(str, ohypes = nil)
    nohype, hypes = mask_hype(str)
    hypes = ohypes if ohypes
    match = nohype.match /(\w)(\w)\1/
    if match
      if match[1] != match[2]
        bab = match[2] + match[1] + match[2]
        babmatch = hypes.any? {|h| h.match /#{bab}/}
        if babmatch
          print "BAB -> #{bab}:> "
          return true
        else
          #Look Elsewhere in the string
          return ssl?(match[2] + match[1] + match.post_match, hypes)
        end
      else
        return ssl?(match[2] + match[1] + match.post_match, hypes)
      end
    else
      return false
    end
  end

  def tls?(str)
    badmatch = str.match /\[[^\]]*(\w)(\w)\2\1[^\]]*\]/
    if badmatch && badmatch[1] != badmatch[2]
      #print "[ABBA] -> "
      return false
    else
      matches = str.match /(\w)(\w)\2\1/
      if matches
        if matches[1] != matches[2]
          #print  "ABBA: #{matches[0]}"
          return true
        else
          return tls?(matches[2] + matches.post_match)
        end
      else
        #print "NONE -> "
        return false
      end
    end
  end

end
