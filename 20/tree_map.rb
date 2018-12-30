COLORS = {
  "#" => "\e[33m#\e[0m",
  "|" => "\e[31m|\e[0m",
  "-" => "\e[31m-\e[0m",
  "X" => "\e[32mX\e[0m"
}

DIRECTIONS = {
  "N" => [ 0, -1],
  "S" => [ 0,  1],
  "E" => [ 1,  0],
  "W" => [-1,  0]
}

class TreeMap
  class Map
    def initialize(map)
      @map = map
      @x_offset = 0
      @y_offset = 0
    end

    def visualise
      colorize(string)
    end

    def colorize(string)
      COLORS.each do |char, color|
        string = string.gsub(char, color)
      end
      string
    end

    def string
      @map.join("\n") + "\n"
    end

    def walk(tree, x, y, next_tree = nil)
      if tree.terminal?
        if next_tree
          walk(next_tree, x, y)
        end
        return
      elsif tree.split?
        tree.parts.each do |part|
          walk(part, x, y, tree.next)
        end
        return
      else
        case tree.token
          when 'N'
            x, y = walk_north(x,y)
          when 'S'
            x, y = walk_south(x,y)
          when 'E'
            x, y = walk_east(x,y)
          when 'W'
            x, y = walk_west(x,y)
        end
      end
      walk(tree.next, x, y, next_tree)
    end

    def walk_east(x, y)
      x = x + 1; ox, oy = offset([x,y])
      @map[oy][ox] = "|"

      grow_east(x)

      x = x + 1; ox, oy = offset([x,y])
      @map[oy][ox] = "."

      [x, y]
    end

    def walk_west(x, y)
      x = x - 1; ox, oy = offset([x,y])
      @map[oy][ox] = "|"

      grow_west(x)

      x = x - 1; ox, oy = offset([x,y])
      @map[oy][ox] = "."

      [x, y]
    end

    def walk_north(x,y)
      y = y - 1; ox, oy = offset([x,y])
      @map[oy][ox] = "-"

      grow_north(y)

      y = y - 1; ox, oy = offset([x,y])
      @map[oy][ox] = "."

      [x, y]
    end

    def walk_south(x,y)
      y = y + 1; ox, oy = offset([x,y])
      @map[oy][ox] = "-"

      grow_south(y)

      y = y + 1; ox, oy = offset([x,y])
      @map[oy][ox] = "."

      [x, y]
    end

    def grow_north(y)
      if (@y_offset + y) == 0
        length = @map.first.length
        @map.unshift("?" * length)
        @map.unshift("?" * length)
        @y_offset += 2
      end
    end

    def grow_south(y)
      ylength = @map.length
      if (@y_offset + y + 1) == ylength
        length = @map.first.length
        @map << ("?" * length)
        @map << ("?" * length)
      end
    end

    def grow_east(x)
      length = @map.first.length
      if (x+@x_offset+1) == length
        @map.each_with_index do |row, y|
          @map[y] << "??"
        end
      end
    end

    def grow_west(x)
      if (@x_offset + x) == 0
        @map.each_with_index do |row, y|
          @map[y] = "??" + @map[y]
        end
        @x_offset += 2
      end
    end

    def solidify
      @map.each do |line|
        line.gsub!("?", "#")
      end
    end

    private

    def offset(loc)
      x, y = loc
      [x + @x_offset, y + @y_offset]
    end
  end

  class Node
    attr_reader :token, :next, :parts

    def initialize(tokens)
      @token = tokens.shift
      if @token == "^"
        @start = true
      elsif @token == "$" || @token == "|" || @token == ")"
        @terminal = true
        return
      elsif @token == "("
        @split = true
        @parts = []
        part = Node.new(tokens)
        while part.terminates?("|") do
          @parts << part
          part = Node.new(tokens)
        end
        @parts << part
      end
      @next = Node.new(tokens)
    end

    def terminates?(ending)
      return true if @token == ending
      return false if @next.nil?
      return @next.terminates?(ending)
    end

    def dump
      if start?
        print "START: "
      elsif split?
        print " SPLIT["
        @parts.each do |part|
          print " >> "
          part.dump
        end
        print " ] "
      elsif terminal?
        return
      else
        print "> #{@token}"
      end
      @next.dump
    end

    def depth
      return @next.depth if @start
      return 0 if @terminal
      if split?
        sizes = @parts.map &:depth
        if sizes.min == 0
          #skippable
          return @next.depth
        else
          return sizes.max + @next.depth
        end
      else
        return 1 + @next.depth
      end
    end

    def depths(depth = 0, x=0, y=0, depths = {}, next_tree = nil)
      #puts "Depth: #{depth} @ (#{x}, #{y}) > #{@token}"
      if depths[[x,y]]
        if depths[[x,y]] < depth
          return
        else
          depth = depths[[x,y]]
        end
      else
        depths[[x,y]] = depth
      end

      if terminal?
        if next_tree
          next_tree.depths(depth, x, y, depths)
        end
        return
      elsif start?
        @next.depths(depth, x, y, depths)
      elsif split?
        @parts.each do |part|
          part.depths(depth, x, y, depths, @next)
        end
      else
        dx, dy = DIRECTIONS[@token]
        x = x + dx; y = y + dy
        @next.depths(depth + 1, x, y, depths, next_tree)
      end
      depths
    end

    def start?
      @start
    end

    def terminal?
      @terminal
    end

    def split?
      @split
    end
  end

  def self.build(string)
    tokens = string.chars
    Node.new(tokens)
  end

  def self.map(tree)
    map = [
      "???",
      "?X?",
      "???"
    ]
    map = Map.new(map)
    map.walk(tree, 1, 1)
    map.solidify
    map
  end

end
