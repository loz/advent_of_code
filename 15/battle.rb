class Battle
  attr_reader :elves, :map

  class Unit
    attr_reader :pos, :type, :locations
    attr_accessor :targets

    def initialize(x,y,type)
      @pos = [x,y]
      @type = type
      @targets = []
    end

    def determine_range(map)
      @locations = []
      @targets.each do |target|
        tx, ty = target.pos
        @locations << [tx,ty-1] if map[ty-1][tx] == '.'
        @locations << [tx-1,ty] if map[ty][tx-1] == '.'
        @locations << [tx+1,ty] if map[ty][tx+1] == '.'
        @locations << [tx,ty+1] if map[ty+1][tx] == '.'
      end
    end

    def filter_nearest(map)
      @routes = {}
      @shortest = nil
      @locations.each do |l|
        puts "Searching For Nearest: #{l}"
        explore_all_routes(map, l)
      end
      @routes.select! do |loc, routes|
        shortest = shortest_route(routes)
        shortest && shortest.length == @shortest
      end
      @locations = @routes.keys
    end

    def distance(loc)
      shortest_route(@routes[loc]).length
    end

    def shortest_route(routes)
      routes.min do |r1,r2|
        r1.count <=> r2.count
      end
    end

    def filter_reachable(map)
      @locations.select! {|l| can_reach(map, l) }
    end

    def can_reach(map, location)
      x,y = pos
      explore_to_first(map, x,y,location)
    end

    def explore_all_routes(map, location)
      x,y = pos
      routes = explore_to(map, x,y, location)
      @routes[location] = routes
    end

    def explore_to_first(map, sx, sy, location, visited = [])
      visited << [sx,sy]

      directions = [
        [0,-1], #NORTH
        [-1,0], #WEST
        [+1,0], #EAST
        [0,+1], #SOUTH
      ]
      
      directions.each do |d|
        dx,dy = d
        nx = sx + dx
        ny = sy + dy
        unless visited.include? [nx,ny]
          if map[ny][nx] == '.'
            return true if nx == location[0] && ny == location[1]
            return true if explore_to_first(map, nx, ny, location, visited)
          end
        end
      end
      false
    end

    def explore_to(map, sx, sy, location, visited = [], routes = [])
      visited << [sx,sy]

      if @shortest
        return if visited.length > @shortest
      end

      directions = [
        [0,-1], #NORTH
        [-1,0], #WEST
        [+1,0], #EAST
        [0,+1], #SOUTH
      ]
      
      directions.each do |d|
        dx,dy = d
        nx = sx + dx
        ny = sy + dy

        unless visited.include? [nx,ny]
          if map[ny][nx] == '.'
            if nx == location[0] && ny == location[1]
              @shortest ||= visited.length
              #puts "Route Found: %s (shortest: %s, this: %s)" %
              #  [visited.inspect, @shortest[location], visited.length]
              @shortest = visited.length if visited.length < @shortest
              routes << visited
            else
              explore_to(map, nx, ny, location, visited.dup, routes)
            end
          end
        end
      end
      routes
    end
  end

  def set_map(map)
    find_units(map)
  end

  def define_targets
    @units.each do |unit|
      unit.targets = @units.select { |u| u.type != unit.type }
    end
  end

  def elves
    @units.select {|u| u.type == 'E' }
  end

  def visualise_map
    print "\e[0;0H"
    @map.each do |row|
      puts row.join
    end
  end

  def visualise_locations(locations)
    rows = @map.size
    print "\e[0;0H"
    print "\e[32m" #Green
    locations.each do |loc|
      x,y = loc
      print "\e[%d;%dH" % [y+1,x+1]
      print "*"
    end
    print "\e[0m"
    print "\e[%d;0H" % (rows + 2)
  end

  private
  def find_units(map)
    @units = []
    @map = []
    map.split("\n").each_with_index do |row, y|
      @map[y] ||= []
      row.split("").each_with_index do |cell, x|
        @map[y][x] = cell
        if cell == 'E' || cell == 'G'
          @units << Unit.new(x,y,cell)
        end
      end
    end
  end
end
