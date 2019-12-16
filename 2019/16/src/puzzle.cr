class Puzzle

  @digits = [] of Int32

  def process(str)
    @digits = str.chomp.chars.map {|c| c.to_i}
  end

  def result
    offset = @digits[0,7].join.to_i
    repeat = 10_000
    digits = @digits * repeat
    digits = digits[offset, digits.size]

    puts offset, repeat, digits.size
    100.times do |n|
      digits = offset_fft(offset, digits)
      print "."
    end
    puts
    puts digits[0,8].join
    #Does first 8 only matter
   # digits = @digits
   # puts digits[0,8].join
   # 100.times do |n|
   #   print "*#{n} ->"
   #   digits = @digits * n
   #   puts fft(digits)[0,8].join
   # end
  end

  def gen(digits)
    1.times do
      digits = fft(digits)
      puts digits[0,8].join
    end
    print "@100: "
    puts digits[0,8].join
  end

  def fft(digits)
    #puts "#{digits.size} digits"
    newdigits = [] of Int32
    digits.each_with_index do |_,idx|
      newdigits << sumof(digits, idx+1)
    end
    newdigits
  end

  def offset_fft(offset, digits)
    newdigits = [] of Int32
    digits.each_with_index do |_,idx|
      newdigits << offset_sumof(offset,digits, idx+1)
    end
    newdigits
  end

  def offset_sumof(offset, digits, digit)
    # NTH digit always
    # N 0's folloed by SUM(N next digits)
    # SKIP N 0s
    # - SUM(N next digits)
    # SKIP N 0s
    # ... until end of string
    # [1,2,3,4,5,6,7,8]
    # 1: [1], _ -[3], _ [5], _ -[7] _
    # 2: _ [2,3], _ _, -[6, 7], _
    # 3: _ _ [3,4,5] _ _ _ 
    # 4: _ _ _ [4, 5, 6, 7] _
    # 5: _ _ _ _ [5, 6, 7, 8]
    # 6: _ _ _ _ _ [6, 7, 8]
    # 7: _ _ _ _ _ _ [7, 8]
    # 8: _ _ _ _ _ _ _ [8]
    n = digit + offset
    #N 0' already trimmed
    #print "#{digit}:> "
    max = digits.size
    pos = digit-1
    total = 0
    modes = [:add, :skip, :sub, :skip]
    while pos < max
      mode = modes.first
      case mode
        when :add
          #print "#{n}x1:"
          ones = digits[pos, n]
          #print "#{ones}"
          total += ones.sum
          pos += ones.size
        when :skip
          #N 0's
          #print "#{n}x0:"
          pos += n
        when :sub
          #print "#{n}x-1:"
          ones = digits[pos, n]
          #print "-#{ones}"
          total -= ones.sum
          pos += ones.size
      end
      modes.rotate!
    end
    #puts " => #{total}"
    (total.abs) % 10
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
    #print "#{digits[digit-1]} => "
    #print "0*n + " * (digit-1)
    #print "#{digit}:> "
    length = digits.size
    pos =  digit-1 #skip digit -1 chars
    total = 0
    inmode = 0
    while pos < length
      mode = modes.first
      case mode
        when :add
          #print "#{digit}x1:" if inmode == 0
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
          #print "#{digit}x0:"
          #print "0*n + " * digit
        when :sub
          #print "#{digit}x-1:" if inmode == 0
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
    #puts " => #{total}"
    (total.abs) % 10
  end

end
