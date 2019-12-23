alias Rule = Tuple(Symbol, Int32)

class Solution
  property operands = {} of Int64 => Int64

  def initialize(op : Operand)
    @operands[op.o_of] = op.o_n
  end

  def initialize(@operands); end

  def for(o_of)
    @operands[o_of]
  end

  def *(i : Int64)
    ops = @operands.dup
    ops.keys.each do |o_of|
      ops[o_of] *= i
    end
    Solution.new(ops)
  end

  def -(s : Solution)
    ops = @operands.dup
    s.operands.keys.each do |o_of|
      o_n = s.operands[o_of]
      if ops[o_of]?
        ops[o_of] -= o_n
      else
        ops[o_of] = 0.to_i64 - o_n
      end
    end
    Solution.new(ops)
  end

  def to_s
    @operands.map {|o_of, o_n| "(#{o_n})#{o_of}" }.join ","
  end
end

class Operand
  property o_n : Int64
  property o_of : Int64

  def initialize(@o_n, @o_of)
  end

  def *(i : Int64)
    Operand.new(@o_n * i, @o_of)
  end
end

class Puzzle
  property rules = [] of Rule
  property deck = [] of Int64
  property desk = [] of Int64
  property cards : Int64
  property congruent = {} of Int64 => Int64

  def initialize(@cards = 0.to_i64)
  end

  def deck=(newdeck)
    @deck = newdeck
    @desk = newdeck.dup
    @cards = newdeck.size.to_i64
  end

  def process(str)
    str.each_line do |line|
      @rules << parse_rules(line)
    end
  end

  def parse_rules(line)
    if line == "deal into new stack"
      {:dns, 0}
    else
      matches = line.match /deal with increment (\d+)/
      if matches
        {:dwi, matches[1].to_i}
      else
        matches = line.match /cut ([-]{0,1}\d+)/
        if matches
          {:cut, matches[1].to_i}
        else
          {:notparsed, -1}
        end
      end
    end
  end

  def acceptable_deck?(count)
    increments = [] of Int32
    @rules.each do |rule|
      fn, n = rule
      if fn == :dwi
        increments << n
      end
    end
    increments.uniq!
    increments.each do |n|
      cursor = 0
      seen = {} of Int32 => Bool
      count.times do
        return false if seen[cursor]?
        seen[cursor] = true
        cursor = (cursor + n ) % count
      end
    end
    return true
  end

  def result_test
    @cards = 10
    print "            "
    10.times do |n|
      print " #{n}"
    end
    puts
    print "CUT -4 FROM:"
    10.times do |n|
      from = reverse_digit_cut(-4,n)
      print " #{from}"
    end
    puts
    print "CUT  3 FROM:"
    10.times do |n|
      from = reverse_digit_cut(3,n)
      print " #{from}"
    end
    puts
    print "DNS    FROM:"
    10.times do |n|
      from = reverse_digit_deal_new_stack(n)
      print " #{from}"
    end
    puts
    print "DWI  3 FROM:"
    10.times do |n|
      from = reverse_digit_deal_with_increment(3,n)
      print " #{from}"
    end
    puts
    print "DWI  7 FROM:"
    10.times do |n|
      from = reverse_digit_deal_with_increment(7,n)
      print " #{from}"
    end
    puts
    print "DWI  9 FROM:"
    10.times do |n|
      from = reverse_digit_deal_with_increment(9,n)
      print " #{from}"
    end
    puts

  end

  def result_search_unshuffled
    count = if ARGV.empty?
      10007.to_i64
    else
      ARGV[0].to_i64
    end
    if !acceptable_deck?(count)
      puts "Cannot Shuffle #{count} as increments overlap"
      exit 0
    end
    puts "Shuffling #{count} Cards using #{@rules.size} rules:"
    self.deck = (0...count).to_a.map {|n| n.to_i64}
    shuffle
    find = @deck.index(2019.to_i64)
    puts "Card 2019 @ #{find}"
    self.deck = (0...count).to_a.map {|n| n.to_i64}
    #offset = 0
    #seen = {@deck.dup => true}
    #10000.times do
    #  seen, offset = find_repeat_shuffle(seen, offset)
    #end
    find_repetition(@deck.dup)
    
  end

  def result_part2
    count = if ARGV.empty?
      119315717514047
    else
      ARGV[0].to_i64
    end

    @cards = count

    puts "2020 for 1 itteration:"
    puts calculate(2020)
  end

  def expand_refs(n, refs)
    if refs[n]?
      val, mul, div = refs[n]
      #puts "Expanding #{n}.. -> #{val} - #{mul}*#{div}.."
      expand_refs(val,refs) - (expand_refs(div, refs) * mul )
    else
      Solution.new(Operand.new(1.to_i64,n.to_i64))
    end
  end

  def calculate_w_values
    values = @rules.select do |rule|
      fn, n = rule
      fn == :dwi
    end.map {|rule| fn, n = rule; n }
    values.uniq!
    values.each do |n|
      print  "Calculating Congruent for #{n} (mod #{cards}) -> "
      ##ASSUME cards prime, and GCD(mod,cards) == 1 otherwise overlaps
      refs = {} of Int64 => Tuple(Int64,Int64,Int64)
      val = cards
      div = n.to_i64
      mul = val // div
      rem = val % div
      refs[rem] = {val,mul,div}
      while rem > 1
        #puts "#{val} = #{mul}*#{div} + #{rem}"
        val = div
        div = rem
        rem = val % div
        mul = val // div
        refs[rem] = {val,mul,div}
      end
      #puts "#{val} = #{mul}*#{div} + #{rem}"
      v = expand_refs(1, refs).for(n)
      print v
      if v < 0
        v = cards - v
        puts " -> #{v}"
      else
        puts
      end
      @congruent[n.to_i64] = v
    end
  end

  def result
    count = if ARGV.empty?
      #119315717514047
      10007.to_i64
    else
      ARGV[0].to_i64
    end
    @cards = count
    calculate_w_values
    #result_test
    #result_search_unshuffled
  end

  def find_repetition(unshuffled)
    repcount = 12000
    found = false
    repcount.times do |t|
      shuffle
      if @deck == unshuffled
        puts "Repeated after #{t} shuffles"
        found = true
        break
      end
    end
    puts "No Repeats Found after #{repcount} shuffles :(" if !found
  end

  def shuffle
    #puts @deck
    rules.each do |rule|
      fn, n = rule
      case fn
        when :cut
          cut n
        when :dns
          deal_new_stack
        when :dwi
          deal_with_increment n
      end
      #puts "#{fn} #{@deck} @#{n}"
    end
  end

  def reverse_digit_cut(n, card)
    n = (cards + n) if n < 0
    newcard = (card + n) % cards
    #p "Invert Cut: #{card}th of #{cards} (CUT: @#{n}) -> #{newcard}"
    newcard
  end
  
  def reverse_digit_deal_new_stack(card)
    newcard = (cards - card) -1
    #p "Invert Stack: #{card}th of #{cards} -> #{newcard}"
    newcard
  end

  def chinese_remainder(mods, rems)
    max = 1
    mods.each {|m| max = max * m }
    series = rems.zip(mods).map {|r,m| r.step(to: max, by: m).to_a }
    return nil if series.empty?
    inall = series.first
    series.each {|s| inall &= s }
    return nil if inall.empty?
    return inall.first
  end

  def reverse_digit_deal_with_increment(n, card)
    #  n * C === card % cards
    #  Linear Congruence
    #  n and cards are co-prime otherwise overlaps..
    mods = [] of Int64
    rems = [] of Int64
    val = cards
    div = n.to_i64
    rem = val % div
    while rem > 1
      mods << div
      rems << rem
      val = div
      div = rem
      rem = val % div
    end
    puts "***"
    print ":>#{cards} % #{n} -> "
    crem = chinese_remainder(mods, rems)
    puts crem

    card
  end

  def inverse_mod(target, n, max)
    max.times do |m|
      poss = m * n
      #puts "#{m} -> #{mod} v #{target}" 
      return poss if poss % max == target
    end
    return -1
  end

  def calculate(card)
    reverse = rules.reverse
    reverse.each do |rule|
      #print "#{card} "
      fn, n = rule
      case fn
        when :cut
          card = reverse_digit_cut n, card
        when :dns
          card = reverse_digit_deal_new_stack card
        when :dwi
          card = reverse_digit_deal_with_increment n, card
      end
      #puts "#{fn} #{card} @#{n}"
    end
    card
  end

  def find_repeat_shuffle(seen = nil, offset = 0)
    seen = {@deck.dup => true} unless seen
    t = 0
    found = false
    rules.each do |rule|
      fn, n = rule
      case fn
        when :cut
          cut n
        when :dns
          deal_new_stack
        when :dwi
          deal_with_increment n
      end
      if seen[@deck.dup]?
        puts "Repeated after #{offset+t} steps"
        found = true
        break
      end
      seen[@deck.dup] = true
      t += 1
    end
    puts "No Repeats Found in #{offset+t} steps" if !found
    return {seen, offset+t}
  end

  def deal_new_stack
    @deck.reverse!
  end

  def cut(n)
    #puts @deck.size
    #puts @desk.size
    #puts "===="
    cards = @deck.size
    n = cards + n if n < 0
    #m = cards - n
    ##First Part (up to end of deck)
    #(0...m).each do |loc|
    #  #puts "#{loc} <- #{loc+n} of #{cards}"
    #  @desk[loc] = @deck[loc+n]
    #end
    ##Second PArt
    #(0...n).each do |loc|
    #  mloc = m + loc
    #  #puts "#{mloc} <- #{loc} of #{cards}"
    #  @desk[mloc] = @deck[loc]
    #end
    #tmp = @deck
    #@deck = @desk
    #@desk = tmp
    @deck = @deck[n,@deck.size] + @deck[0,n]
  end

  def deal_with_increment(n)
    #cards = @deck.size
    #newdeck = Array(Int32).new(cards, -1)
    #cursor = 0
    #cards.times do |pos|
    #  newdeck[cursor] = @deck[pos]
    #  cursor = (cursor + n ) % cards
    #end
    #@deck = newdeck
    cards = @deck.size
    cards.times do |pos|
      cursor = (pos * n) % cards
      #p "#{pos} -> #{cursor}"
      @desk[cursor] = @deck[pos]
      #cursor = (cursor + n ) % cards
    end
    tmp = @deck
    @deck = @desk
    @desk = tmp
  end

end
