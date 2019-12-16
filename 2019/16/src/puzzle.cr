class Puzzle

  @digits = [] of Int32

  def process(str)
    @digits = str.chomp.chars.map {|c| c.to_i}
  end

  def result
    #puts @digits
    #Does first 8 only matter
    digits = @digits
    puts digits[0,8].join
    100.times do |n|
      print "*#{n} ->"
      digits = @digits * n
      puts fft(digits)[0,8].join
    end
    #100.times do
    #  digits = fft(digits)
    #  puts digits[0,8].join
    #end
    #print "@100: "
    #puts digits[0,8].join
  end

  def fft(digits)
    newdigits = [] of Int32
    digits.each_with_index do |_,idx|
      newdigits << sumof(digits, idx+1)
    end
    newdigits
  end

  def sumof(digits, digit)
    modes = [:add, :skip, :sub, :skip]
    #skip digit-1 chars
    #Then Repeat:
    # add digit chars
    # skip digit chars
    # sub digit chars
    # skip digit chars
    # until > size
    length = digits.size
    pos =  digit-1 #skip digit -1 chars
    total = 0
    inmode = 0
    while pos < length
      mode = modes.first
      case mode
        when :add
          total += digits[pos]
          #print "1*#{digits[pos]} + "
          pos += 1
          inmode += 1
          if inmode == digit
            modes.rotate!
            inmode = 0
          end
        when :skip
          pos += digit
          modes.rotate!
        when :sub
          total -= digits[pos]
          #print "-1*#{digits[pos]} + "
          pos += 1
          inmode += 1
          if inmode == digit
            modes.rotate!
            inmode = 0
          end
      end
    end
    #puts
    (total.abs) % 10
  end

end
