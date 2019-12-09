class Puzzle

  MOVES = {
    'U' => {0, -1},
    'L' => {-1, 0},
    'D' => {0, 1},
    'R' => {1, 0}
  }

  KEYPAD = [
    [nil, nil, nil, nil, nil, nil, nil],
    [nil, nil, nil, '1', nil, nil, nil],
    [nil, nil, '2', '3', '4', nil, nil],
    [nil, '5', '6', '7', '8', '9', nil],
    [nil, nil, 'A', 'B', 'C', nil, nil],
    [nil, nil, nil, 'D', nil, nil, nil],
    [nil, nil, nil, nil, nil, nil, nil]
  ]


  property code = [] of (Char|Nil)
  property x = 1
  property y = 3

  def process(str)
    str.each_line do |line|
      process_line(line)
    end
  end

  def process_line(line)
    line.each_char do |char|
      move_by(char)
      #puts "#{@x}, #{@y}"
    end
    @code << KEYPAD[@y][@x]
  end

  def move_by(char)
    dx, dy = MOVES[char]
    x = @x + dx
    y = @y + dy
    #puts "#{x}, #{y}"
    unless KEYPAD[y][x].nil?
      @x = x
      @y = y
    end
  end

  def result
    puts code
  end

end
