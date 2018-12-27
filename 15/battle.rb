COLORS = {
  :yellow => "\e[33m",
  'E' => "\e[33m",
  :green => "\e[32m",
  'G' => "\e[32m"
}

ENEMY = {
  'E' => 'G',
  'G' => 'E'
}

DIRECTIONS = [
  [0,-1], #NORTH
  [-1,0], #WEST
  [+1,0], #EAST
  [0,+1], #SOUTH
]

class Battle
  attr_reader :elves, :map, :round

  def self.visualise_map(map)
    print "\e[0;0H"
    map.each do |row|
      puts row.join
    end
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

  def draw(loc, letter)
    x,y = loc
    print "\e[%d;%dH" % [y+1,x+1]
    print letter
  end

  def unit_at(x,y)
    #p "%s v %s" % [[x,y], @units.map { |u| u.pos }]
    @units.each do |i|
      return i if i.pos == [x,y]
    end
  end

  def remove_unit(unit)
    x,y = unit.pos
    map[y][x] = "."
  end

  def ongoing?
    @units.reject! {|u| u.dead? }
    elves.count != 0 && goblins.count != 0
  end

  def turn
    @units.reject! {|u| u.dead? }
    @units.sort! {|u1, u2| cmp_reading_order(u1.pos,u2.pos) }
    @round += 1
    print " " * 40
    print "Round: #{@round}"

    visualise_map
    #@units.each do |unit|
    #  p "%s, %s" % [unit.pos, unit.type]
    #end
    @units.each do |unit|
      if unit.in_range?(map)
        unit.attack(self)
      else
        unit.determine_range(map)
        unit.filter_reachable(map)
        unit.filter_nearest(map)
        unit.select_target
        unless unit.target.nil?
          dest = unit.move_step
          #visualise_locations(unit.locations, unit.type)
          x,y = unit.pos
          map[y][x] = '.'
          x,y = dest
          map[y][x] = unit.type
          unit.pos = dest
          if unit.in_range?(map)
            unit.attack(self)
          end
        end
      end
      visualise_map
    end
    puts "\n" * 10
  end

  class Step
    attr_reader :loc, :prev, :length

    def plot
      print COLORS[:yellow]
      _plot
      print "\e[0m"
    end

    def _plot
      x,y = loc
      print "\e[%d;%dH" % [y+1,x+1]
      print "X"
      prev.plot unless prev.nil?
    end

    def string
      str = loc.inspect
      str += ":%s" %length
      unless prev.nil?
        str += " < "
        str += prev.string
      end
      str
    end

    def first_step
      unless prev.nil?
        return prev.first_step
      end
      self
    end

    def visited?(loc)
      if loc == @loc
        true
      elsif prev.nil?
        false
      else
        @prev.visited?(loc)
      end
    end

    def initialize(loc, prev, length)
      @loc = loc
      @prev = prev
      @length = length
    end
  end

  class Unit
    attr_reader :type, :locations
    attr_accessor :pos, :targets, :target, :hitpoints

    def initialize(x,y,type)
      @pos = [x,y]
      @type = type
      @targets = []
      @hitpoints = 200
    end

    def dead?
      hitpoints <= 0
    end

    def in_range?(map)
      x, y = pos
      enemy = ENEMY[type]
      DIRECTIONS.each do |d|
        dx,dy = d
        nx = x + dx
        ny = y + dy
        return true if map[ny][nx] == enemy
      end
      false
    end

    def attack(battle)
      x, y = pos
      enemy = ENEMY[type]
      enemies = DIRECTIONS.map do |d|
        dx,dy = d
        nx = x + dx
        ny = y + dy
        if battle.map[ny][nx] == enemy
          battle.unit_at(nx,ny)
        else
          nil
        end
      end
      #puts "---Attack #{pos} > #{enemy} ---"
      #puts battle.map_string
      #puts "-------------------"
      enemies = enemies.compact
      enemies.sort! {|e1, e2| e1.hitpoints <=> e2.hitpoints }
      weakest = enemies.first
      if weakest
        enemies.select! {|e| e.hitpoints == weakest.hitpoints }
        unless enemies.count == 1
          enemies.sort! { |e1, e2| cmp_reading_order(e1.pos,e2.pos) }
        end
        enemy = enemies.first
        enemy.hitpoints -= 3
        if enemy.dead?
          battle.remove_unit(enemy)
        end
      end
      #puts "-------------------"
    end

    def determine_range(map)
      @locations = []
      @target = nil
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
      @all_locations = @locations.dup
      @locations.sort! do |l1, l2|
        d1 = (@pos[0]-l1[0]).abs + (pos[1]-l1[1]).abs
        d2 = (@pos[0]-l2[0]).abs + (pos[1]-l2[1]).abs
        d1 <=> d2
      end
      @locations.each do |l|
        #puts "Searching For Nearest: #{l}"
        explore_all_routes(map, l)
      end
      routes = @routes.select do |loc, routes|
        shortest = shortest_route(routes)
        if shortest
          shortest.length == @shortest
        end
      end
      @locations = routes.keys
    end

    def select_target
      @target = @locations.min do |l1, l2|
        cmp_reading_order(l1,l2)
      end
    end

    def move_step
      options = @routes[@target]
      #puts '*'*20
      #options.each do |option|
      #  p option.string
      #end
      #puts '*'*20
      options.select! do |route|
        route.length == @shortest
      end
      #puts "Locking for First Steps towards #{pos}"
      steps = options.map {|route| route.first_step.loc }
      steps.sort! do |l1, l2|
        cmp_reading_order(l1,l2)
      end
      steps.first
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

    def distance(loc)
      shortest_route(@routes[loc]).length
    end

    def shortest_route(routes)
      routes.min do |r1,r2|
        r1.length <=> r2.length
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
      #puts "Exploring all routes to #{location}(#{type}:#{pos})"
      x,y = pos
      visited_in = {}
      @all_locations.each do |loc|
        visited_in[loc] = 0
      end
      visited_in.delete location
      routes = explore_to(map, x,y, location, visited_in)
      @routes[location] = routes
    end

    def explore_to_first(map, sx, sy, location, visited = [])
      visited << [sx,sy]

      DIRECTIONS.each do |d|
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

    def explore_to(map, sx, sy, location, visited_in, head = nil, routes = [], visits=0)
      visits+=1
      if @shortest
        return if visits > @shortest
      end
      
      DIRECTIONS.each do |d|
        dx,dy = d
        nx = sx + dx
        ny = sy + dy
        seen = false

        if best = visited_in[[nx,ny]]
          if visits < best
            visited_in[[nx,ny]] = visits
          else
            seen = true
          end
        else
          visited_in[[nx,ny]] = visits
        end
        if map[ny][nx] == '.'
          new_head = Step.new([nx,ny],head, visits)

          if nx == location[0] && ny == location[1]
            @shortest ||= visits
            #puts "(#{type}): Route to %s Found: %s (shortest: %s, this: %s)" %
            #  [location, new_head.string, @shortest, visits]
            @shortest = visits if visits < @shortest
            routes << new_head
          else
            #Battle.visualise_map(map)
            #head.plot
            unless seen
              explore_to(map, nx, ny, location, visited_in, new_head, routes, visits)
            end
          end
        end
      end
      return routes
    end
  end

  def set_map(map)
    @round = 0
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

  def goblins
    @units.select {|u| u.type == 'G' }
  end

  def map_string
    @map.map do |row|
      row.join
    end.join("\n") + "\n"
  end

  def visualise_map
    print "\e[0;0H"
    @map.each do |row|
      puts row.join
    end
  end

  def visualise_locations(locations, color)
    rows = @map.size
    print "\e[0;0H"
    print COLORS[color]
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
