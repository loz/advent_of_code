alias Row = Array(Char)

class Layer
  @cells = [] of Row
  @gcells = [] of Row
  @width = 5
  @height = 5

  ADJACENT = [
    { 0, -1},
    {-1,  0},
    { 1,  0},
    { 0,  1},
  ]
  def row(n)
    @cells[n]
  end

  def each_row(&block)
    @cells.each do |row|
      yield row
    end
  end

  def empty!
    @cells = [] of Row
    @gcells = [] of Row
    @height.times do |y|
      @cells << ['.'] * @width
      @gcells << ['.'] * @width
    end
  end

  def process(str)
    str.lines.each do |line|
      @cells << line.chars
      @gcells << line.chars
      @width = line.size
    end
    @height = @cells.size
  end

  def neighbors(x,y, layer)
    cells = [] of Char
    ADJACENT.each do |delta|
      dx, dy = delta
      nx = x + dx
      ny = y + dy
      cells << @cells[ny][nx] if nx >= 0 && ny >= 0 && nx < @width && ny < @height
    end
    cells
  end

  def result
    seen = {dump => true}
    generation
    while !seen[dump]?
      seen[dump] = true
      generation
    end
    puts "*** REPEATED ***"
    puts dump
    puts diversity
  end

  def count
    total = 0.to_u64
    @cells.each do |row|
      row.each do |ch|
        total += 1 if ch == '#'
      end
    end
    total
  end

  def diversity
    total = 0.to_u64
    val = 1.to_u64
    @cells.each do |row|
      row.each do |ch|
        total += val if ch == '#'
        val <<= 1
      end
    end
    total
  end

  def dump
    @cells.map {|row| row.join("")}.join("\n")
  end

  def generation(neighbor_giver = self, layer = 0)
    generation_without_tick(neighbor_giver, layer)
    tick!
  end

  def tick!
    tmp = @cells
    @cells = @gcells
    @gcells = tmp
  end

  def generation_without_tick(neighbor_giver, layer)
    @cells.each_with_index do |row, y|
      row.each_with_index do |ch, x|
        ncells = neighbor_giver.neighbors(x,y, layer).count {|n| n == '#'}
        if ch == '#' && ncells != 1
          @gcells[y][x] = '.' 
        elsif ch == '.' && (ncells == 1 || ncells == 2)
          @gcells[y][x] = '#'
        else
          @gcells[y][x] = ch
        end
      end
    end
  end

  def at(x,y)
    @cells[y][x]
  end
end

class Puzzle
  @layer = Layer.new

  @depth = 105

  property deck = {} of Int32 => Layer

  def process(str)
    @layer.process(str)
  end

  def neighbors(x,y,level) #nRecurisive Version
    return [] of Row if x == 2 && y == 2
    layer = @deck[level]
    cells = layer.neighbors(x,y,0)
    #OUTER
    if y == 0 || y == 4 #Top/Bottom Row, include center top
      return cells unless @deck[level-1]?
      outer = @deck[level-1]
      row = y == 0 ? 1 : 3
      cells << outer.row(row)[2]
      cells << outer.row(2)[1] if x == 0
      cells << outer.row(2)[3] if x == 4
    elsif x == 0 || x == 4
      return cells unless @deck[level-1]?
      outer = @deck[level-1]
      row = outer.row(2)
      col = x == 0 ? 1 : 3
      cells << row[col]
    #INNER
    elsif y == 2 #Inner Left / Right
      return cells unless @deck[level+1]?
      inner = @deck[level+1]
      col = x == 1 ? 0 : 4
      inner.each_row do |row|
        cells << row[col]
      end
    elsif x == 2 #Inner Bottom / Top
      return cells unless @deck[level+1]?
      inner = @deck[level+1]
      #col = x == 1 ? 0 : 4
      row = y == 1 ? 0 : 4
      inner.row(row).each do |c|
        cells << c
      end
    end
    cells
  end

  def result_part1
    seen = {@layer.dump => true}
    @layer.generation
    while !seen[@layer.dump]?
      seen[@layer.dump] = true
      @layer.generation
    end
    puts "*** REPEATED ***"
    puts @layer.dump
    puts @layer.diversity
  end

  def init_decks
    deck[0] = @layer
    ((0-@depth)...0).each do |d|
      l = Layer.new
      l.empty!
      deck[d] = l
    end
    (1..@depth).each do |d|
      l = Layer.new
      l.empty!
      deck[d] = l
    end
  end

  def dump
    ((0-@depth)..@depth).each do |level|
      layer = @deck[level]
      puts "-- #{level} --"
      puts layer.dump
      puts " (#{layer.count}) cells"
    end
  end

  def generation
    @deck.each do |level, layer|
      layer.generation_without_tick(self, level)
    end
    @deck.each do |_, layer|
      layer.tick!
    end
  end

  def result_part2
    init_decks
    200.times do
      generation
    end
    dump
    total = @deck.sum {|_, layer| layer.count }
    puts "After 200 mins, #{total} bugs"
  end

  def result
    result_part2
  end
end
