class Puzzle

  @current = [] of String
  property width = 0
  property height = 0

  def process(str)
    width = 0
    height = 0
    str.each_line do |line|
      height += 1
      width = line.size
      @current << line
    end
    #Force corners
    @current[0] = @current[0].sub(0, "#")
    @current[0] = @current[0].sub(width-1, "#")
    @current[height-1] = @current[height-1].sub(0, "#")
    @current[height-1] = @current[height-1].sub(width-1, "#")

    @width = width
    @height = height
  end

  def generate
    newgen = [] of String
    height.times do |y|
      curline = [] of Char
      width.times do |x|
        n = on_neighbors(x,y)
        cur = @current[y][x]
        if (x == 0 || x == width-1) &&
           (y == 0 || y == height-1)
           curline << '#'
        elsif cur == '#'
          if n == 2 || n == 3
            curline << '#'
          else
            curline << '.'
          end
        else
          if n == 3
            curline << '#'
          else
            curline << '.'
          end
        end
      end
      newgen << curline.join
    end
    @current = newgen
    newgen.join("\n")
  end

  def current
    @current.join("\n")
  end

  def on_neighbors(x,y)
    on = 0
    neighbors = [] of Tuple(Int32,Int32)

    neighbors << {x-1, y} unless x == 0
    neighbors << {x-1, y-1} unless x == 0 || y==0
    neighbors << {x-1, y+1} unless x == 0 || y==height-1

    neighbors << {x+1, y} unless x == width-1
    neighbors << {x+1, y-1} unless x == width-1 || y==0
    neighbors << {x+1, y+1} unless x == width-1 || y==height-1

    neighbors << {x, y-1} unless y==0
    neighbors << {x, y+1} unless y == height-1
    on = neighbors.count do |n|
      xx, yy = n
      @current[yy][xx] == '#'
    end
    on
  end

  def onlights
    on = 0
    @current.each do |line|
      line.each_char do |char|
        on += 1 if char == '#'
      end
    end
    on
  end

  def result
    puts "Generating.."
    100.times { generate }
    puts "On: #{onlights}"   
  end

end
