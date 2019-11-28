# TODO: Write documentation for `Battle`
DIRECTIONS = [
  [0,-1], #NORTH
  [-1,0], #WEST
  [+1,0], #EAST
  [0,+1], #SOUTH
]

class Battle
  class Unit
    property targets = [] of Unit
    property pos : Tuple(Int32,Int32)
    property type : String
    property locations : Array(Tuple(Int32,Int32))

    def initialize(x, y, type : String)
      @type = type
      @pos = {x,y}
      @locations = [] of Tuple(Int32,Int32)
    end
    
    def determine_range(map)
      @locations = [] of Tuple(Int32,Int32)
      @targets.each do |target|
        tx, ty = target.pos
        @locations << {tx,ty-1} if map[ty-1][tx] == "."
        @locations << {tx-1,ty} if map[ty][tx-1] == "."
        @locations << {tx+1,ty} if map[ty][tx+1] == "."
        @locations << {tx,ty+1} if map[ty+1][tx] == "."
      end
    end

    def filter_nearest(map)
      return if @locations.empty?
      #@routes = {}
      @shortest = 0
      @shortest = map.size * map.first.size #Largest possible Value
      @all_locations = [] of Tuple(Int32,Int32)
      @all_locations = @locations.dup
      @paths = {} of Tuple(Int32, Int32) =>  Array(Array(Int32))
      @paths = explore_map(map, @locations)


      #lengths = @paths.map { |t, r| r.size }
      #@shortest = lengths.min
      @shortest = @paths.map_with_index { |k,v| v.size }

      @locations = [] of Tuple(Int32,Int32)
      @paths.each do |target, route|
        if route.size == @shortest
          @locations << target
        end
      end
      #p @locations
    end

    def explore_map(map, locations)
      paths = {} of Tuple(Int32,Int32) => Array(Array(Int32))
      height = map.size
      width =  map.first.size
      worst_case = width * height #Largest possible Value
      locations.each do |location|
        #puts "Exploring Map: #{pos} -> #{location}"
        #Explore from NWES locations
        # Thus, will ALWAYS take shortest path in reading order
        x, y = pos
        shortest = worst_case
        DIRECTIONS.each do |d|
          dx,dy = d
          nx = x + dx
          ny = y + dy
          next if nx == 0 || nx == width - 1
          next if ny == 0 || ny == height - 1
          next if map[ny][nx] != "."
          neighbour = [nx, ny]
          path = a_star(neighbour, location, map)
          #puts "-> : #{path.inspect}"
          next if path.nil? #No Route
          if path.size < shortest
            paths[location] = path
            shortest = path.size
          end
        end
      end
      return paths
    end

    def manhatten(a, b)
      ax, ay = a
      bx, by = b
      (ax-bx).abs + (ay-by).abs
    end

    def reconstruct_path(routes, current)
      #puts "Reconstruct: #{routes.inspect}"
      path = [current]
      while !routes[current].nil? 
        current = routes[current]
        path.unshift current
      end
      path
    end

  def cmp_reading_order(l1,l2)
    x1, y1 = l1
    x2, y2 = l2
    if y1 < y2
      -1
    elsif y1 > y2
      1
    else
      x1 <=> x2
    end
  end

    def best_score(scores, set)
      min = set.min_by { |val| scores[val] }
      min = scores[min]
      best = set.select {|loc| scores[loc] == min }
      #sort options in READING order
      best.sort! { |l1, l2| cmp_reading_order(l1,l2) }
      best.first
    end


    def a_star(start, goal, map)
      #puts "Searching #{start} -> #{goal}:..."
      #all = []
      closed_set = [] of Array(Int32)
      open_set = [start]
      cameFrom = {} of Array(Int32) => Array(Int32)

      height = map.size
      width =  map.first.size
      worst_case = width * height #Largest possible Value
      shortest = worst_case
      gScore = {} of Array(Int32) => Int32
      fScore = {} of Array(Int32) => Int32
      height.times do |y|
        width.times do |x|
          gScore[[x,y]] = worst_case
          fScore[[x,y]] = worst_case
        end
      end
      gScore[start] = 0

      fScore[start] = manhatten(start, goal)

      while !open_set.empty?
        current = best_score(fScore, open_set)
        if current == goal
          path = reconstruct_path(cameFrom, current)
          #puts "Found A Shortest Route!, #{path}"
          #all << path
          #shortest = path.length - 1 
          #open_set.delete current
          #return cameFrom
          return path
        else
          open_set.delete current
          closed_set << current

          next if gScore[current] > shortest
          #puts "Current: #{current}"
          x, y = current
          DIRECTIONS.each do |d|
            dx,dy = d
            nx = x + dx
            ny = y + dy
            neighbour = [nx, ny]
            #puts "N: #{neighbour}, #{width}x#{height}"
            next if map[ny][nx] != "."
            next if closed_set.includes? neighbour
            poss_gscore = gScore[current] + 1

            if open_set.includes? neighbour
              next if poss_gscore > gScore[neighbour]
            else
              #Discover
              open_set << neighbour
            end
            #Best path for now..
            cameFrom[neighbour] = current
            gScore[neighbour] = poss_gscore
            fScore[neighbour] = poss_gscore + manhatten(neighbour, goal)
          end
        end
      end
      #puts "---DONE---"
      nil
    end
  end




  property units = [] of Unit
  property map

  def initialize
    @map = [] of Array(String)
  end

  def elves
    @units.select {|u| u.type == "E" }
  end

  def set_map(map_string)
    @round = 0
    @units = [] of Unit
    @map = [] of Array(String)
    find_units(map_string)
  end

  def define_targets
    @units.each do |unit|
      unit.targets = @units.select {|u| u.type != unit.type }
    end
  end


  def find_units(map_string)
    map_string.split("\n").each_with_index do |row, y|
      @map << [] of String
      row.split("").each_with_index do |cell, x|
        @map[y] << cell
        if cell == "E" || cell == "G"
          @units << Unit.new(x,y,cell)
        end
      end 
    end
  end
end
