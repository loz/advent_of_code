COLORS = {
  :yellow => "\e[33m",
  'E' => "\e[33m",
  :green => "\e[32m",
  'G' => "\e[32m"
}

VIS_SUBS = {
  '#' => "\e[33m#\e[0m",
  'E' => "\e[32mE\e[0m",
  'G' => "\e[31mG\e[0m",
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
  attr_reader :units, :elves, :map, :round

  def self.visualise_route(node)
    print "\e[0;0H"
    print COLORS[:cyan]
    node.visualise_route
      #print "\e[%d;%dH" % [y+1,x+1]
    print "\e[0m"
  end

  def self.map_string(map)
    map.map do |row|
      row.join
    end.join("\n") + "\n"
  end

  def self.visualise_map(map)
    print "\e[0;0H"
    str = map_string(map)
    VIS_SUBS.each do |ch, rep|
      str = str.gsub(ch, rep)
    end
    puts str
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
    #print " " * 40
    #print "Round: #{@round}"

    #visualise_map
    #@units.each do |unit|
    #  p "%s, %s" % [unit.pos, unit.type]
    #end
    @units.each do |unit|
      if unit.in_range?(map)
        unit.attack(self)
      else
        unit.determine_range(map)
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
      #visualise_map
    end
    #puts "\n" * 10
  end

  class Step
    attr_reader :loc, :prev, :length

    def first?; false; end

    def visualise_route
      x,y = loc
      print "\e[%d;%dH" % [y+1,x+1]
      if first?
        print "?"
      else
        print "X"
        prev.visualise_route unless first?
      end
    end

    def string
      return "" if first?
      str = loc.inspect
      str += ":%s" %length
      str += " < "
      str += prev.string
      str
    end

    def step(n)
      return self if length == n
      return prev.step(n)
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

    def initialize(loc, prev = nil, length = 0)
      @loc = loc
      @prev = prev
      @length = length
    end
  end

  class StartStep < Step
    def visited?(pos); false; end
    def first?; true; end
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
      return if @locations.empty?
      @routes = {}
      @shortest = map.length * map.first.length #Largest possible Value
      @all_locations = @locations.dup
      @routes = explore_map(map, @locations)
      shortests = @routes.map do |target, routes|
        shortest = shortest_route(routes)
        [target, shortest]
      end
      #shortests.each do |target, route|
      #  puts "#{target} -> #{route.string}"
      #end
      #puts "Shortest Route: #{@shortest}"
      @locations = []
      shortests.each do |target, route|
        if route.length == @shortest
          @locations << target
        end
      end
      #p @locations
    end

    def select_target
      @target = @locations.min do |l1, l2|
        cmp_reading_order(l1,l2)
      end
    end

    def move_step
      #puts "making a Move: #{@target} from #{pos}"
      options = @routes[@target]
      #puts '*'*20
      #options.each do |option|
      #  p option.string
      #end
      #puts '*'*20

      options.select! do |route|
        route.length == @shortest
      end

      #puts '*'*20
      #options.each do |option|
      #  p option.string
      #end
      #puts '*'*20

      #puts "Locking for First Steps towards #{pos}"
      steps = options.map {|route| route.step(1).loc }
      #puts "*" * 20
      #puts steps.inspect
      #puts "*" * 20

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

    def explore_map(map, locations)
      #puts "Explore Map: #{self.pos.inspect} -> #{locations.inspect}"
      start = StartStep.new(pos)
      routes = Hash.new { |h, k| h[k] = [] }
      worst_case = @shortest
      shortests = Hash.new { |h, k| h[k] = worst_case }
      x, y = pos
      explore(x, y, map, locations, routes, start, shortests)
      #routes.each do |k,v|
      #  puts "#{k} -> "
      #    v.each do |r|
      #      puts "  #{r.string}"
      #    end
      #end
      routes
    end

    def explore(x, y, map, locations, routes, current, shortests, length = 0)
      #puts "Exploring @(#{x}, #{y}) :> #{current.string}"
      exp_pos = [x,y]
      return if length > @shortest #Shortcut if we already found shorter routes
      return if length > shortests[[x,y]] #Short-circuit, we've found shorter path here
      return if current.visited?(exp_pos)
      return if map[y][x] != "." unless current.first?

      here = Step.new(exp_pos, current, length)
      #Battle.visualise_map(map)
      #Battle.visualise_route(here)
      if locations.include? exp_pos
        @shortest = length if length < @shortest
        routes[exp_pos] << here
      end
      shortests[[x,y]] = length if length < shortests[[x,y]]

      #puts "----UPLR---"
      DIRECTIONS.each do |d|
        dx,dy = d
        nx = x + dx
        ny = y + dy
        explore(nx, ny, map, locations, routes, here, shortests, length + 1)
      end
      #puts ">----UPLR---<"
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
    str = map_string
    VIS_SUBS.each do |ch, rep|
      str = str.gsub(ch, rep)
    end
    puts str
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
