class Puzzle

  def looksay(str)
    count = 0
    out = ""
    current = ""
    str.each_char do |ch|
      if ch != current
        if count != 0
          out += count.to_s + current
        end
        current = ch
        count = 1
      else
        count += 1
      end
    end
    out += count.to_s + current
    out
  end

  def result
    input = "1113222113"
    puts "Start: ", input
    gen = input
    50.times do |t|
      gen = looksay(gen)
      puts "#{t} : (#{gen.size})"
    end
  end

end
