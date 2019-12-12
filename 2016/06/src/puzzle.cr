class Puzzle

  property freqs = [] of Hash(Char,Int32)

  def process(str)
    str.lines.first.size.times do
      @freqs << Hash(Char,Int32).new(0)
    end

    str.each_line do |line|
      process_line(line)
    end
  end

  def code
    @freqs.map {|f| most(f) }.join
  end

  def least_code
    @freqs.map {|f| least(f) }.join
  end
  
  def least(freqs)
    min = 10_000_000
    let = '?'
    freqs.keys.each do |k|
      fk = freqs[k] 
      if fk < min
        min = fk
        let = k
      end
    end
    let
  end

  def most(freqs)
    max = 0
    let = '?'
    freqs.keys.each do |k|
      fk = freqs[k] 
      if fk > max
        max = fk
        let = k
      end
    end
    let
  end

  def process_line(line)
    line.each_char_with_index do |c, idx|
      @freqs[idx][c] += 1
    end
  end

  def result
    puts code
    puts least_code
  end

end
