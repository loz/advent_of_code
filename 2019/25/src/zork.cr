class Zork
  alias Inventory = Set(String)

  GET_TO_SECURITY = <<-EOF
  north
  west
  take planetoid
  west
  take spool of cat6
  east
  east
  south
  west
  north
  take dark matter
  south
  east
  east
  north
  take sand
  west
  take coin
  north
  take jam
  south
  west
  south
  take wreath
  west
  take fuel cell
  east
  north
  north
  west
  inv
  EOF

  ITEMS = Set.new([
  "planetoid",
  "spool of cat6",
  "dark matter",
  "sand",
  "coin",
  "jam",
  "wreath",
  "fuel cell"
  ])

  @buffer = [] of Char
  @inv = Set(String).new
  @frontier = Set(Inventory).new
  @visited = {} of Set(String) => Bool
  @new_frontier = Set(Inventory).new

  @heavies = [] of Inventory

  @check = "heavier"
  @cur_line = ""

  def load
    puts "HERE"
    @buffer = GET_TO_SECURITY.chars
    @inv = ITEMS.dup
    drop_inventory
    ITEMS.each do |item|
      @frontier << Set{item} #Just the first item
    end
  end

  def nl
    @buffer << '\n'
  end

  def type(text)
    text.each_char {|ch| @buffer << ch }
    nl
  end

  def drop_inventory
    @inv.each do |item|
      type("drop #{item}")
    end
    @inv = Set(String).new
  end

  def try_security
    @inv.each do |item|
      type("take #{item}")
    end
    type("south")
  end

  def heavy?(poss)
    @heavies.each do |h|
      return true if (h - poss).empty?
    end
    false
  end

  def add_to_new_frontier
    puts "Trying Heavier Than #{@inv}"
    options = ITEMS - @inv
    options.each do |option|
      poss = Set{option} + @inv
      @new_frontier << poss unless heavy?(poss)
      puts poss
    end
  end

  def take_new_frontier
    @frontier = @new_frontier
    @new_frontier = Set(Set(String)).new
  end

  def explore_frontier
    if @inv.empty?
      take_new_frontier if @frontier.empty?
      @inv = @frontier.to_a.first
      @frontier = @frontier - Set{@inv}
      puts "Trying #{@inv}"
      try_security
    else
      puts "Tried: #{@inv}, Need #{@check}"
      if @check == "heavier"
        add_to_new_frontier
      elsif @check == "lighter"
        @heavies << @inv
      else
        raise "Unknown Check"
      end
      drop_inventory
      @check = "unknown"
    end
  end

  def shift
    if @buffer.empty?
      explore_frontier
    end
    @buffer.shift.ord.to_i64
  end

  def check_weight
    matches = @cur_line.match /Droids on this ship are (heavier|lighter) than the detected value/
    if matches
      @check = matches[1]
    end
  end

  def <<(val)
    @cur_line += val.chr
    if val == 10 #Newline
      check_weight
      @cur_line = ""
    end
    print val.chr
  end
end
