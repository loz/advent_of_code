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
  '#' => ChunkyPNG::Color('yellow'),
  '|' => ChunkyPNG::Color('lightblue'),
  '~' => ChunkyPNG::Color('aqua'),
  '*' => ChunkyPNG::Color('aqua'),
}


class Reservoir

  def initialize
    @squares = []
    set_cell(500,0,"+")
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
  def flow(reservoir); end
  def flowing?; false; end
  def complete?(v); true; end
end

class InfiniteFlow
  def flow(r); true end
  def flowing?; true; end
  def complete?(v); true; end
end

class Water
  def initialize(x=500, y=0, options = {})
    @parent = options[:parent]
    @left = options[:left]
    @right = options[:right]

    @x = x
    @y = y
  end

  def complete?(visited = [])
    visited << self
    return true if @rest
    return false if @down.nil? #Not Yet Flowed Infinitely
    return false unless @down.complete?(visited)

    unless @left.nil? || visited.include?(@left)
      return false unless @left.complete?(visited)
    end

    unless @right.nil? || visited.include?(@right)
      return false unless @right.complete?(visited)
    end
    return true
  end

  def flow(reservoir)
    return false if @rest

    flowed = flow_down(reservoir)
    return true if flowed

    left = flow_left(reservoir)
    right = flow_right(reservoir)

    flowed = left || right
    if !flowed
      rest(reservoir)
    end
    return flowed
  end

  private

  def rest(reservoir)
    @rest = true
    reservoir.set_cell(@x,@y, "~")
  end

  def flow_down(reservoir)
    if @down
      return @down.flow(reservoir)
    else
      if (@y+1) == reservoir.depth
        @down = InfiniteFlow.new
        reservoir.set_cell(@x,@y,"*")
        return true
      end
      down = reservoir.cell(@x,@y+1)
      if (down == '#' || down == '~')
        @down = NoFlow.new
        return false
      end
      reservoir.set_cell(@x,@y + 1,"|")
      @down = Water.new(@x, @y + 1, :parent => self)
      return true
    end
  end

  def flow_left(reservoir)
    if @left
      return false if @left == @parent
      return @left.flow(reservoir)
    else
     left = reservoir.cell(@x-1, @y)
     if (left == '#' || left == '~')
       @left = NoFlow.new
       return false
     end
     reservoir.set_cell(@x-1,@y, "|")
     @left = Water.new(@x-1,@y, :right => self, :parent => self)
     return true
    end
  end

  def flow_right(reservoir)
    if @right
      return false if @right == @parent
      return @right.flow(reservoir)
    else
     right = reservoir.cell(@x+1, @y)
     if (right == '#' || right == '~')
       @right = NoFlow.new
       return false
     end
     reservoir.set_cell(@x+1,@y, "|")
     @right = Water.new(@x+1,@y, :left => self, :parent => self)
     return true
    end
  end
end
