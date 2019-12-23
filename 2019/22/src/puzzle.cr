alias Rule = Tuple(Symbol, Int32)

class Puzzle
  property rules = [] of Rule
  property deck = [] of Int64
  property desk = [] of Int64
  property cards : Int64

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
    self.deck = (0...10).to_a
    puts " - 9 - "
    p self.deck
    deal_with_increment(9)
    p self.deck
    rev = (0...10).to_a.map do |n|
      reverse_digit_deal_with_increment(9,n)
    end
    puts "What Mapped to X?"
    puts rev
    puts "*"*30

    puts " - 3 - "
    self.deck = (0...10).to_a
    p self.deck
    deal_with_increment(3)
    p self.deck
    rev = (0...10).to_a.map do |n|
      reverse_digit_deal_with_increment(3,n)
    end
    puts "What Mapped to X?"
    puts rev
    puts "*"*30

    puts " - 7 - "
    self.deck = (0...10).to_a
    p self.deck
    deal_with_increment(7)
    p self.deck
    rev = (0...10).to_a.map do |n|
      reverse_digit_deal_with_increment(7,n)
    end
    puts "What Mapped to X?"
    puts rev
    puts "*"*30
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

  def result
    result_search_unshuffled
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

  def reverse_digit_deal_with_increment(n, card)
  "
- 9 -
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
[0, 9, 8, 7, 6, 5, 4, 3, 2, 1]
What Mapped to X?
[0, 9, 8, 7, 6, 5, 4, 3, 2, 1]
******************************
9 => 1 because 9 * 9 = 81  % 10 -> 1
1> 10 * (9-1) = 80 | + 1 = 81 // 9 -> 9

6 => 4 because 6 * 9 = 54 % 10 -> 4
4> 10 * (9-4) = 50 | + 4 = 54 // 9 -> 6

1 => 9 because 9 * 1 = 9 % 10 -> 9
9> 10 * (9-9) = 0 | + 9 = 9 // 9 -> 1

- 3 - 
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
[0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
What Mapped to X?
[0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
******************************
7 => 1 because 7 * 3 = 21, 21 % 10 -> 1
1> 10 * (3-1) = 20  | + 1 = 21  // 3  -> 7

4 => 2 because 4 * 3 = 12   % 10 -> 2
2> 10 * (3-2) = 10  | + 2 = 12  // 3  -> 4

8 => 4 because 8 * 3 = 24  % 10 -> 4
4> 10 * (3-1) = 20  | + 4 = 24  // 3  -> 8

- 7 -
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
[0, 3, 6, 9, 2, 5, 8, 1, 4, 7]

7 => 9 because 7 * 7 = 49 % 10 -> 9
9>  10 * (7-2) = 50 | + 9 = 59   !!!
          7-3  = 40
9> 70 - (9*7)|63 = 7

6 => 2 because 7 * 6 = 42 % 10 -> 2
2>  10 * (7-2) = 50 | + 2 = 52   !!!
          7-3  = 40
2> 70 - (2*7)|14 = 56 -> 6

1 => 7 because 7 * 1 = 7 % 7 -> 7
7>  10 * (7-0) = 70 | + 7 = 77 // 7 -> 11 -> 1

"
    # ORIGINAL FORMULA: cursor = (pos * n) % cards 
    # REVERSE:  cursor = (pos * n) % cards
    #           cursor = 0 - ((pos * n) % cards)
    #cursor = CARDS - ((card * n) % cards)

    #modn = card % n
    #unmod = (cards * (n - modn)) + card
    inv = inverse_mod(card, n, cards)
    oldpos = inv//n
    #unmod = (n * 10) - (n * card )
    #oldpos = (unmod // n) % cards
    #oldpos = unmod % cards

    
    # ORIGINAL FORMULA: cursor = (pos * n) % cards 
    #p "Invert Deal: #{card}th of #{cards} (INC: @#{n}-> #{newcard}th"
    oldpos
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
