require "./intcode"

class RepairDroidIO
  @buffer = [] of Int64 #Channel(Int64).new(2)
  property x = 0
  property y = 0
  property ox = 0
  property xy = 0
  property moving = {0,0}
  property moving_dir = :X

  property found = false
  property shortest = [] of Tuple(Symbol, Tuple(Int32, Int32))
  property shortest_len = 0
  property reverting = false

  property visited = [{0,0}]
  property walls = [] of Tuple(Int32,Int32)
  property current_path = [] of Tuple(Symbol, Tuple(Int32, Int32))
  property unexplored = [] of Tuple(Int32, Int32)
  property draw = false

  DIR = {
    :N => {1.to_i64, { 0,-1}},
    :S => {2.to_i64, { 0, 1}},
    :W => {3.to_i64, {-1, 0}},
    :E => {4.to_i64, { 1, 0}}
  }

  OPPOSITE = {
    :N => :S,
    :S => :N,
    :W => :E,
    :E => :W
  }

  def visited?(loc)
    visited.includes?(loc) || walls.includes?(loc)
  end

  def wall?(loc)
    walls.includes?(loc)
  end

  def visit(dir)
    cmd, move = DIR[dir]
    @moving_dir = dir
    @moving = move
    @buffer << cmd
  end

  def revert(move)
    @reverting = true
    dir, _ = move
    visit OPPOSITE[dir]
  end

  def dump_map
    50.times do |y|
      50.times do |x|
        lx = x - 25
        ly = y - 25
        if found && lx == @ox && ly == @oy
          #print "\033[0;32mO"
          print "O"
        elsif lx == @x && ly == @y
          #print "\033[0;32mR"
          print "R"
        elsif lx == 0 && ly == 0
          #print "\033[0;36mS"
          print "S"
        elsif wall?({lx,ly})
          #print "\033[0;31m#"
          print "#"
        elsif visited?({lx,ly})
          #print "\033[0;34m."
          print "."
        elsif unexplored.includes?({lx,ly})
          #print "\033[0;33m?"
          print "?"
        else
          #print "\033[0;37m."
          print " "
        end
      end
      puts
    end
    if found
      puts "R: #{@x},#{@y} O:#{@ox},#{@oy}"
      puts "Best: #{shortest_len}"
    else
      puts "R: #{@x},#{@y}"
    end
  end

  def shift
    if found && unexplored.empty?
      dump_map
      raise "FULLY EXPLORED"
    end
    if @buffer.empty?
      explore_map
    end
    if @buffer.empty?
      p unexplored
      raise "WHAT?"
    end
    @buffer.shift
  end

  def explore_map
    neigbors = fetch_neigbors
    tovisit = neigbors.reject {|n| _, loc = n; visited? loc }
    if tovisit.empty?
      unless current_path.empty?
        lastmove = current_path.pop
        revert(lastmove)
      end
    else
      #Visit the first
      dir, _ = tovisit.pop
      add_to_unexplored(tovisit)
      visit(dir)
    end
  end

  def add_to_unexplored(visits)
    visits.each do |v|
      _, loc = v
      @unexplored << loc
    end
  end

  def fetch_neigbors
    DIR.map do |d, detail|
      _, delta = detail
      dx, dy = delta
      {d, {@x + dx, @y + dy}}
    end
  end

  def <<(status)
    case status
      when 1, 2
        #Accepted and Moved
        dx, dy = @moving
        curloc = {@x, @y}
        @x += dx
        @y += dy
        loc = {@x, @y}
        @visited << loc
        if @reverting
          @reverting = false
        else
          @current_path << {@moving_dir, curloc}
        end
        if status == 2
          @found = true
          @ox = @x
          @oy = @y
          @shortest = @current_path.dup
          @shortest_len = @shortest.size
        end

        @unexplored.delete loc #remove from unexplored
        #puts "#{@moving_dir}. #{loc}, #{found}"
      when 0
        #Failed to Move, but hit a wall
        dx, dy = @moving
        wall = {@x + dx, @y + dy}
        @walls << wall
        @unexplored.delete wall #remove from unexplored
        #puts "#{@moving_dir}#"
    end
    if draw
     #sleep 0.001
     print "\033[0;0f"
     dump_map
    end
  end
end
