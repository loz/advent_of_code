class Puzzle
  property result = ""
  property original = ""

  def process(str)
    @original = str
    @result = decompress(str) 
  end

  def decompress(str)
    newstr = ""
    cursor = 0
    len = str.size
    while cursor < len
      char = str[cursor]
      if char == '('
        cursor, added = process_repeat(cursor, str)
        newstr += added
      else
        newstr += char
      end
      cursor += 1
    end
    newstr
  end
  
  def process_repeat(cursor, str)
    cursor, rep = process_reps(cursor, str)
    cursor, count = process_count(cursor, str)
    cursor, chars = fetch_chars(cursor, str, rep)
    {cursor, chars * count}
  end

  def v2_process_repeat(cursor, str)
    cursor, rep = process_reps(cursor, str)
    cursor, count = process_count(cursor, str)
    #print "add #{rep} x #{count} of next"
    cursor, chars = fetch_chars(cursor, str, rep)
    #puts "Recuring: #{chars}"
    vlen = v2length(chars)
    {cursor, vlen * count}
  end

  def fetch_n_to(cursor, str, target)
    ch = ""
    num = ""
    while ch != target
      num += ch
      cursor += 1
      ch = str[cursor]
    end
    {cursor, num.to_i}
  end

  def process_reps(cursor, str)
    fetch_n_to(cursor, str, 'x')
  end

  def process_count(cursor, str)
    fetch_n_to(cursor, str, ')')
  end

  def fetch_chars(cursor, str, count)
    chars = ""
    count.times do
      cursor +=1 
      chars += str[cursor]
    end
    {cursor, chars}
  end

  def v2length(str)
    vlen = 0.to_u64
    cursor = 0
    len = str.size
    while cursor < len
      char = str[cursor]
      if char == '('
        cursor, addlen = v2_process_repeat(cursor, str)
        vlen += addlen
      else
        vlen += 1
      end
      cursor += 1
    end
    vlen
  end

  def result
    nows = @result.gsub /\s+/, ""
    puts "Decompressed to: #{nows.size}"
    onows = original.gsub /\s+/, ""

    puts "V2 Length: #{v2length(onows)}"
  end

end
