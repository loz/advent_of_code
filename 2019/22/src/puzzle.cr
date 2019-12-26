alias Rule = Tuple(Symbol, Int32)

class Func
  property of_c : Int64
  property plus_n : Int64
  property mod : Int64

  def initialize(of_c, plus_n, mod)
    @of_c = of_c.to_i64
    @plus_n = plus_n.to_i64
    @mod = mod.to_i64
  end

  def apply(c : Int64)
    (((c.to_i128 * @of_c.to_i128) + @plus_n) % @mod).to_i64
  end

  def apply(f : Func)
    fc = f.of_c
    fn = f.plus_n

    a = (fc.to_i128 * @of_c) % @mod
    b = ((@of_c.to_i128 * fn.to_i128) + @plus_n.to_i128) % @mod
    Func.new(a.to_i64, b.to_i64, @mod)
  end
end

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

  def expand_refs(n, refs)
    if refs[n]?
      val, mul, div = refs[n]
      #puts "Expanding #{n}.. -> #{val} - #{mul}*#{div}.."
      expand_refs(val,refs) - (expand_refs(div, refs) * mul )
    else
      Solution.new(Operand.new(1.to_i64,n.to_i64))
    end
  end

  def calculate_congurent_values
    values = @rules.select do |rule|
      fn, n = rule
      fn == :dwi
    end.map {|rule| fn, n = rule; n }
    values.uniq!
    values.each do |n|
      cache_congurent(n)
    end
  end

  def congruent(n)
    cache_congurent(n) unless @congruent[n.to_i64]?
    @congruent[n.to_i64]
  end

  def cache_congurent(n)
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
      v = cards + v
      puts " -> #{v}"
    else
      puts
    end
    @congruent[n.to_i64] = v
  end

  def result_part2
    count = if ARGV.empty?
      119315717514047
      10007.to_i64
    else
      ARGV[0].to_i64
    end
    @cards = count
    calculate_congurent_values

    shufcount = 101741582076661

    a = calculate(0)
    puts "0:> #{a}"
    b = calculate(1)
    puts "1:> #{b}"

    a = forward_shuffle(0)
    puts "0:> #{a}"
    b = forward_shuffle(1)
    puts "1:> #{b}"

    # k*b + c  => c'
    #  a' = k * d + 0
    #  b' = k * d + 1
    ab = a*b
    puts a*b
    puts (a*b) % cards

    ar = calculate(a)
    puts "< 0:> #{ar}"
    br = calculate(b)
    puts "< 1:> #{br}"


    c = 2020
    a = forward_shuffle(c)
    puts "a:> #{a}"
    kb = a - c
    puts "kb:> #{kb}"
    
    k = 1
    b = kb
    k = kb // 7
    b = congruent(7) #* (kb//7)
    puts "k: #{k}"
    puts "b: #{b}"
      
    kcb = (k*c) + b

    puts "k*c +b:> #{kcb % cards}"
    abk = (a-b)//k
    puts "c = (a-b)//k  #{(abk % cards)}"

    twice = 2020
    puts "before: #{twice}"
    twice = forward_shuffle(twice)
    puts "once  : #{twice}"
    twice = forward_shuffle(twice)
    puts "twice : #{twice}"
    puts "k*(k*c+b) + b -> #{k*((k*c)+b) + b}"

    tena = 2020
    shuffs = 11
    shuffs.times { tena = forward_shuffle(tena) }
    puts "#{shuffs} shuff: #{tena}"

    k1 = shuffs * k
    b1 = shuffs * b

    nc = ((k1 * c * shuffs) + b1) % cards
    puts "nc: #{nc}" 

    return
    
    seen = {2020.to_i64 => true}
    puts "Seeking Repeated Location"
    loc = 2020
    itter = 0.to_u64
    1000.times do 
      100.times do
        10000.times do
          itter += 1
          loc = calculate(loc)
          if loc == 2020
            puts "Repeated after #{itter} itterations"
            break;
          end
          seen[loc.to_i64] = true
        end
        print "."
      end
      puts "Searched #{itter} @#{loc}"
    end
  end

  def result_part1
    count = if ARGV.empty?
      #119315717514047
      10007.to_i64
    else
      ARGV[0].to_i64
    end
    self.deck = (0...count).to_a.map {|c| c.to_i64 }
    puts "Shuffling #{count} cards.."
    shuffle
    found = self.deck.index(2019)
    puts "2019 card -> : #{found}"
  end

  def power_fn(fn1, repeats, val)
    return fn1.apply(val) if repeats == 1
    return val if repeats == 0
    mul = 2.to_i64
    fmx = fn1.apply(fn1)
    while mul**2 < repeats
      mul = mul * 2
      fmx = fmx.apply(fmx)
    end
    count = repeats // mul
    rem = repeats % mul
    #p "#{repeats} = #{count} * f(#{mul}) + #{rem}"
    #count.times { val = fmx.apply(val) }
    #rem.times { val = fn1.apply(val) }
    val = power_fn(fmx, count, val)
    power_fn(fn1, rem, val)
  end

  def result_fold
    #@cards = 10007
    @cards = 119315717514047
    repeats = 101741582076661

    fn = reverse_fold_fn
    val = 2020.to_i64
    val = power_fn(fn, repeats, val)
    puts "#{repeats} reverse shuffles -> #{val}"

    fn = fold_fn
    val = power_fn(fn, repeats, val)
    puts "#{repeats} shuffles -> #{val}"
  end

  def result
    result_fold
    #result_part2
  end

  def result_test
    count = if ARGV.empty?
      #119315717514047
      10007.to_i64
    else
      ARGV[0].to_i64
    end
    @cards = count
    calculate_congurent_values

    puts "Reverse of 1822 Should Be 2019"
    actual = calculate(1822)
    puts "Actual: #{actual}"
    #result_test
    #result_search_unshuffled
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

  def forward_digit_cut(n, card)
    (card - n.to_i64) % cards
  end

  def reverse_digit_cut(n, card, mulx = 1)
    #n = ((cards * mulx) + (n * mulx)) if n < 0
    #n = cards + n if n < 0
    #newcard = ((card ** mulx) + n).to_i64 % cards
    card = card ** mulx
    n = n**mulx
    newcard = (card + n.to_i64) % cards
    #p "Invert Cut: #{card}th of #{cards} (CUT: @#{n}) -> #{newcard}"
    newcard
  end

  def forward_digit_deal_new_stack(card)
    (-1 - card).to_i64  % cards
  end
  
  def reverse_digit_deal_new_stack(card, mulx=1)
    #newcard = card
    #newcard = (cards - card) -1 if (mulx % 2 == 1)
    card = card ** mulx
    newcard = (-1 - card).to_i64  % cards
    #p "Invert Stack: #{card}th of #{cards} -> #{newcard}"
    newcard
  end

  def forward_digit_deal_with_increment(n, card)
    (card * n) % cards
  end

  def reverse_digit_deal_with_increment(n, card, mulx=1)
    #  n * C === card % cards
    #  Linear Congruence
    #  n and cards are co-prime otherwise overlaps..
    #v = @congruent[n] * mulx
    card = card ** mulx
    n = n**mulx
    v = congruent(n)
    ((card.to_u128 * v.to_u128) % cards).to_i64
  end

  def fold_cut(n, card)
    #puts "fold_cut #{n} #{card.inspect}"
    Func.new(card.of_c, (card.plus_n - n.to_i64) % cards, cards)
  end

  def fold_deal_new_stack(card)
    #puts "fold_dns #{card.inspect}"
    Func.new(card.of_c * -1.to_i64, (-1.to_i64 * card.plus_n) -1.to_i64, cards)
  end

  def fold_deal_with_increment(n, card)
    #puts "fold_dwi #{n} #{card.inspect}"
    Func.new((card.of_c * n.to_i64) % cards, (card.plus_n * n.to_i64) % cards, cards)
  end

  def reverse_fold_cut(n, card)
    Func.new(card.of_c, (card.plus_n + n.to_i64) % cards, cards)
  end

  def reverse_fold_deal_new_stack(card)
    Func.new(card.of_c * -1.to_i64, (-1.to_i64 * card.plus_n) -1.to_i64, cards)
  end

  def reverse_fold_deal_with_increment(n, card)
    #puts "fold_dwi #{n} #{card.inspect}"
    v = congruent(n)
    nc = (card.of_c.to_i128 * v.to_i128) % cards
    nn = (card.plus_n.to_i128 * v.to_i128) % cards
    Func.new(nc.to_i64, nn.to_i64, cards)
  end

  def reverse_fold_fn
    fold_fn
    card = Func.new(1, 0, cards) 
    rules.reverse.each do |rule|
      fn, n = rule
      case fn
        when :cut
          card = reverse_fold_cut n, card
        when :dns
          card = reverse_fold_deal_new_stack card
        when :dwi
          card = reverse_fold_deal_with_increment n, card
      end
    end
    card
  end

  def fold_fn
    card = Func.new(1, 0, cards) 
    rules.each do |rule|
      fn, n = rule
      case fn
        when :cut
          card = fold_cut n, card
        when :dns
          card = fold_deal_new_stack card
        when :dwi
          card = fold_deal_with_increment n, card
      end
    end
    card
  end

  def calculate(card, mulx = 1)
    reverse = rules.reverse
    reverse.each do |rule|
      #print "#{card} "
      fn, n = rule
      case fn
        when :cut
          card = reverse_digit_cut n, card, mulx
        when :dns
          card = reverse_digit_deal_new_stack card, mulx
        when :dwi
          card = reverse_digit_deal_with_increment n, card, mulx
      end
      #puts "#{fn} #{card} @#{n}"
    end
    card
  end

  def forward_shuffle(card)
    rules.each do |rule|
      fn, n = rule
      case fn
        when :cut
          card = forward_digit_cut n, card
        when :dns
          card = forward_digit_deal_new_stack card
        when :dwi
          card = forward_digit_deal_with_increment n, card
      end
    end
    card
  end

  def deal_new_stack
    @deck.reverse!
  end

  def cut(n)
    cards = @deck.size
    n = cards + n if n < 0
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
