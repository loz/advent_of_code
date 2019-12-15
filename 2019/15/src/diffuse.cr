class Diffuse
  property map = [] of Array(Char)
  property nodes = [] of Tuple(Int32,Int32)

  COLORS = {
    'O' => "\033[0;32m",
    '#' => "\033[0;31m",
    '.' => "\033[0;34m",
    ' ' => "\033[0;34m"
  }

  def process(str)
    str.each_line do |line|
      process_line(line)
    end
  end

  def process_line(line)
    rown = @map.size
    row = [] of Char
    line.each_char_with_index do |ch, col|
      row << ch
      if ch == 'O'
        nodes << {col, rown}
      end
    end
    @map << row
  end

  def dump_map
    print "\033[0;0f"
    @map.each do |row|
      row.each do |ch|
        print COLORS[ch]
        print ch
      end
      puts
    end
  end

  def new_nodes(node)
    deltas = [
      {-1,  0},
      { 1,  0},
      { 0, -1},
      { 0,  1}
    ]
    x, y = node
    newnodes = [] of Tuple(Int32, Int32)
    deltas.each do |delta|
      dx, dy = delta
      nx = x + dx
      ny = y + dy
      newnodes << {nx, ny} if @map[ny][nx] == '.'
    end
    newnodes
  end

  def fill_nodes(nodes)
    nodes.each do |n|
      x, y = n
      @map[y][x] = 'O'
    end
  end

  def result
    minutes = 0
    while !nodes.empty?
      dump_map
      sleep 0.01
      newnodes = [] of Tuple(Int32, Int32)
      nodes.each do |n|
        newnodes += new_nodes(n)
      end
      newnodes = newnodes.uniq
      fill_nodes(newnodes)
      @nodes = newnodes
      minutes += 1
    end
    dump_map
    puts "Tool #{minutes-1} minutes"
  end
end
