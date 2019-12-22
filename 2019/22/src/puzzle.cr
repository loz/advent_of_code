alias Rule = Tuple(Symbol, Int32)

class Puzzle
  property rules = [] of Rule
  property deck = [] of Int32
  property desk = [] of Int32

  def deck=(newdeck)
    @deck = newdeck
    @desk = newdeck.dup
  end

  def process(str)
    str.each_line do |line|
      @rules << parse_rules(line)
    end
  end

  def parse_rules(line)
    if line == "deal into new stack"
      {:deal_new_stack, 0}
    else
      matches = line.match /deal with increment (\d+)/
      if matches
        {:deal_with_increment, matches[1].to_i}
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
      if fn == :deal_with_increment
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

  def result
    count = if ARGV.empty?
      10007
    else
      ARGV[0].to_i
    end
    if !acceptable_deck?(count)
      puts "Cannot Shuffle #{count} as increments overlap"
      exit 0
    end
    puts "Shuffling #{count} Cards using #{@rules.size} rules:"
    self.deck = (0...count).to_a
    shuffle
    find = @deck.index(2019)
    puts "Card 2019 @ #{find}"
    #find_repetition
  end

  def find_repetition
    seen = {@deck.dup => true}
    repcount = 12000
    found = false
    repcount.times do |t|
      shuffle
      if seen[@deck.dup]?
        puts "Repeated after #{t} shuffles"
        found = true
        break
      end
      seen[@deck.dup] = true
    end
    puts "No Repeats Found after #{repcount} shuffles :(" if !found
  end

  def shuffle(deck = nil)
    rules.each do |rule|
      fn, n = rule
      case fn
        when :cut
          cut n
        when :deal_new_stack
          deal_new_stack
        when :deal_with_increment
          deal_with_increment n
      end
    end
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
    cards = @deck.size
    newdeck = Array(Int32).new(cards, -1)
    cursor = 0
    cards.times do |pos|
      newdeck[cursor] = @deck[pos]
      cursor = (cursor + n ) % cards
    end
    @deck = newdeck
  end

end
