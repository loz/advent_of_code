alias Row = Array(Char)
alias Grid = Array(Row)

class Puzzle
  @cells = [] of Row
  @gcells = [] of Row
  @width = 0
  @height = 0

  ADJACENT = [
    { 0, -1},
    {-1,  0},
    { 1,  0},
    { 0,  1},
  ]

  def process(str)
    str.lines.each do |line|
      @cells << line.chars
      @gcells << line.chars
      @width = line.size
    end
    @height = @cells.size
  end

  def neighbors(x,y)
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

  def generation
    @cells.each_with_index do |row, y|
      row.each_with_index do |ch, x|
        ncells = neighbors(x,y).count {|n| n == '#'}
        if ch == '#' && ncells != 1
          @gcells[y][x] = '.' 
        elsif ch == '.' && (ncells == 1 || ncells == 2)
          @gcells[y][x] = '#'
        else
          @gcells[y][x] = ch
        end
      end
    end
    tmp = @cells
    @cells = @gcells
    @gcells = tmp
  end

  def at(x,y)
    @cells[y][x]
  end

end
