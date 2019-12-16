class Puzzle

  @digits = [] of Int32

  def process(str)
    @digits = str.chomp.chars.map {|c| c.to_i}
  end

  def result
    #puts @digits
    #Does first 8 only matter
   # digits = @digits
   # puts digits[0,8].join
   # 100.times do |n|
   #   print "*#{n} ->"
   #   digits = @digits * n
   #   puts fft(digits)[0,8].join
   # end
   gen([1,2,3,4])
   puts "="*40
   gen([1,2,3,4,1,2,3,4])
   puts "="*40
   gen([1,2,3,4,5,1,2,3,4,5])
   puts "="*40
   gen([9,1,2,3,4,5,6,7,8,9])
   puts "="*40
   optimised_fft([9,1,2,3,4,5,6,7,8,9])

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
    newdigits = [] of Int32
    digits.each_with_index do |_,idx|
      newdigits << sumof(digits, idx+1)
    end
    newdigits
  end

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

  def optimised_fft(digits)
    #The LAST 4 digits is always
    #SUM:4, SUM:3, SUM:2, LAST
    #N-5 digit SUM:5
    #N-6 digit SUM:N-6 + 4
    #N-7 digit SUM:N-7 + 3
    #N-8 digit SUM:N-8 + 2
    #N-9 digit SUM:N-9 + 1

    p digits

    newdigits = [] of Int32
    len = digits.size
    digits.each_with_index do |_,idx|
      s_start = idx
      s_end = [idx+4,len-1].min
      #p [s_start, s_end]
      #subset = digits[idx,len-idx]
      subset = digits[s_start,4]
      p subset
      newdigits << (subset.sum % 10)
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
    print "#{digits[digit-1]} => "
    print "0*n + " * (digit-1)
    length = digits.size
    pos =  digit-1 #skip digit -1 chars
    total = 0
    inmode = 0
    while pos < length
      mode = modes.first
      case mode
        when :add
          total += digits[pos]
          print "1*#{digits[pos]} + "
          pos += 1
          inmode += 1
          if inmode == digit
            modes.rotate!
            inmode = 0
          end
        when :skip
          pos += digit
          modes.rotate!
          print "0*n + " * digit
        when :sub
          total -= digits[pos]
          print "-1*#{digits[pos]} + "
          pos += 1
          inmode += 1
          if inmode == digit
            modes.rotate!
            inmode = 0
          end
      end
    end
    puts " => #{total}"
    (total.abs) % 10
  end

end
