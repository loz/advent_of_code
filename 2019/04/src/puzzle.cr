class Puzzle

  def process(str)
  end
  
  def valid(pass)
    seq = false
    seqlen=1
    last = '!'
    pass.each_char do |c|
      return false if c < last
      if !seq
        if (c == last)
          seqlen+=1
        else
          if seqlen == 2
            seq = true
          end
          seqlen = 1
        end
      end
      last = c
    end
    (seqlen == 2) || seq
  end

  def result
    num = 0
    (206938..679128).each do |n|
      if valid(n.to_s)
        puts "#{n} valid"
        num += 1
      end
    end
    puts "Total #{num}"
  end

end
