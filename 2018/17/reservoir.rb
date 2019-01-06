require 'chunky_png'

COLORS = {
  '+' => "\e[21m\e[36m+\e[0m",
  '#' => "\e[93m#\e[0m",
  '|' => "\e[34m|\e[0m",
  '~' => "\e[36m~\e[0m",
  '*' => "\e[36m*\e[0m"
}

VIZ_COLORS = {
  '+' => ChunkyPNG::Color('aqua'),
  '#' => ChunkyPNG::Color('sandybrown'),
  '|' => ChunkyPNG::Color('lightblue'),
  '~' => ChunkyPNG::Color('blue'),
  '*' => ChunkyPNG::Color('aqua'),
}


class Reservoir

  def initialize
    @squares = []
    set_cell(500,0,"+")
  end

  def counts()
    counts = {}
    @squares.each do |row|
      row.each do |cell|
        counts[cell] ||= 0
        counts[cell] += 1
      end
    end
    counts
  end

  def depth
    @squares.length
  end

  def materialize
    max = 0
    @squares.each do |row|
      max = row.length if row && row.length > max
    end

    @squares.each_with_index do |row, y|
      @squares[y] ||= []
      max.times do |x|
        @squares[y][x] ||= "."
      end
    end
  end

  def visualise(window = nil)
    if(window.nil?) 
      right = 0
      @squares.each do |row|
        if row
          right = row.length if row.length > right
        end
      end
      left = right
      @squares.each do |row|
        if row
          pos_left = row.index {|c| !c.nil? && c != "." }
          left = pos_left if pos_left && pos_left < left
        end
      end
      puts "Left:  #{left}"
      puts "Right: #{right}"
      width = right-left
      puts "Width: #{width}"
      puts "Depth: #{depth}"

      @left = left
      @width = width
      @depth = depth

      window = ChunkyPNG::Image.new(@width, @depth, ChunkyPNG::Color('darkgray'))
    end
    
    @depth.times do |y|
      @width.times do |x|
        cell = cell(x + @left, y)
        if cell != "." && !cell.nil?
          window[x,y] = VIZ_COLORS[cell]
        end
      end
    end
    window.save('viz.png', :interlace => true)
    window
  end

  def colorize(render)
    colors = {
      '+' => "\e[21m\e[36m+\e[0m",
      '#' => "\e[93m#\e[0m",
      '|' => "\e[34m|\e[0m",
      '~' => "\e[36m~\e[0m",
      '*' => "\e[36m*\e[0m"
    }
    colors.each do |sym, color|
      render = render.gsub(sym, color)
    end
    render
  end

  def cell(x,y)
    row = @squares[y] ||= []
    row[x] ||= "."
    row[x]
  end

  def set_cell(x,y,val)
    row = @squares[y] ||= []
    row[x] = val
  end

  def render_at(x_pos, width, height = nil)
    height ||= depth
    render = ""
    height.times do |y|
      width.times do |x|
        render += cell(x + x_pos, y)
      end
      render += "\n"
    end
    render
  end

  def mark_vein(note)
    xs, ys = parse_parts(note)
    xr = (xs[0]..xs[1])
    yr = (ys[0]..ys[1])
    xr.each do |x|
      yr.each do |y|
        set_cell(x,y,'#')
      end
    end
  end

  private 

  def parse_parts(note)
    match = note.match /y=([^,$]*)/
    y = parse_part(match[1])
    match = note.match /x=([^,$]*)/
    x = parse_part(match[1])
    [x, y]
  end

  def parse_part(part)
    part = part.split("..")
    if part.length == 1
      part = part + part  #Always an Array range for simplicity
    end
    part.map &:to_i
  end
end

class NoFlow
  def flow(r); false; end
  def complete?; true; end
  def find_node_at(x,y); false; end
end

class InfiniteFlow
  def flow(r); true; end
  def flowing?; true; end
  def complete?; true; end
end

class FollowerFlow
  def initialize(x,y, parent, reservoir)
    @x = x
    @y = y
    #Find Followed Node
    y = y + 1
    cell = reservoir.cell(x,y)
    while cell == "|"
      y += 1
      cell = reservoir.cell(x,y)
    end
    puts "Following Water @ #{x},#{y}"
    root = parent.root_node
    @following = root.find_node_at(x,y)
    puts " --> #{@following.inspect}"
  end
  def flow(r); true; end
  def complete?
    return true if @following.nil?
    @following.complete?
  end
end

class Water
  def initialize(x=500, y=0, options = {})
    @direction = options[:direction] || :down
    @parent = options[:parent]

    @x = x
    @y = y
  end

  def root_node
    return self if @parent.nil?
    return @parent.root_node
  end

  def find_node_at(x, y)
    return self if (x == @x && y == @y)
    left = @left.find_node_at(x, y) if @left
    return left if left
    right = @right.find_node_at(x,y) if @right
    return right if right
    nil
  end

  def remove(child)
    @left = nil if @left == child
    @right = nil if @right == child
  end

  def complete?
    #puts "Complete?:> #{inspect}"
    if @down
      return @down.complete?
    else
      complete = (!@left.nil? || !@right.nil?)
      if @left
        complete &= @left.complete?
      end
      if @right
        complete &= @right.complete?
      end
      return complete
    end
  end

  def flow(reservoir)
    return false if @rest
    flowed = false
    cell = reservoir.cell(@x,@y)

    reservoir.set_cell(@x, @y, "|") if cell == "."

    flowed = flow_down(reservoir)
    return true if flowed

    if @direction == :left || @direction == :down
      left = flow_left(reservoir)
      flowed ||= left
    end

    if @direction == :right || @direction == :down
      right = flow_right(reservoir)
      flowed ||= right
    end

    if !flowed
      flowed ||= flow_back(reservoir)
    end
    return flowed
  end

  private

  def rest(reservoir)
    @rest = true
    reservoir.set_cell(@x,@y, "~")
  end

  def flow_back(reservoir)
    if @direction == :down
      @left = nil
      @right = nil
      if walled_in?(reservoir)
        rest_water(reservoir)
        @y -= 1
        return true
      end
    end
    return false
  end

  def walled_in?(reservoir)
    y = @y
    x = @x
    cell = reservoir.cell(x,y)
    while cell != "#" && cell != "." do
      x -= 1
      cell = reservoir.cell(x,y)
    end
    wall_left = cell == "#"
    y = @y
    x = @x
    cell = reservoir.cell(x,y)
    while cell != "#" && cell != "." do
      x += 1
      cell = reservoir.cell(x,y)
    end
    wall_right = cell == "#"
    wall_left && wall_right
  end

  def rest_water(reservoir)
    y = @y
    x = @x
    while reservoir.cell(x, y) != "#" &&
          reservoir.cell(x, y) != "." do
      reservoir.set_cell(x,y, "~")
      x -= 1
    end
    x = @x+1
    while reservoir.cell(x, y) != "#" &&
          reservoir.cell(x, y) != "." do
      reservoir.set_cell(x,y, "~")
      x += 1
    end
  end

  def flow_down(reservoir)
    return @down.flow(reservoir) if @down
    if (@y+1) == reservoir.depth
      @down = InfiniteFlow.new
      reservoir.set_cell(@x,@y,"*")
      return true
    end

    down = reservoir.cell(@x,@y+1)
    if (down == '|')
      #@parent.remove(self)
      #@down = FollowerFlow.new(@x,@y, self, reservoir)
      return true
    end

    if (down != '.')
      return false
    end

    @y = @y + 1
    @direction = :down
    return true
  end

  def flow_left(reservoir)
    return @left.flow(reservoir) if @left

    left = reservoir.cell(@x-1, @y)
    if left != "." && left != "|"
      @left = NoFlow.new
      return false
    end

    if @direction == :down
      #reservoir.set_cell(@x-1,@y, "<")
      @left = Water.new(@x-1,@y, :direction => :left, :parent => self)
    else
      @x -= 1
    end
    return true
  end

  def flow_right(reservoir)
    return @right.flow(reservoir) if @right
    right = reservoir.cell(@x+1, @y)
    if right != "." && right != "|"
      @right = NoFlow.new
      return false
    end

    if @direction == :down
      #reservoir.set_cell(@x+1,@y, ">")
      @right = Water.new(@x+1,@y, :direction => :right, :parent => self)
    else
      @x += 1
    end
    return true
  end
end
