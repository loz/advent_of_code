class Puzzle
  alias Coord = Tuple(Int32,Int32)
  alias State = Tuple(Coord, Set(Char))

  DELTAS = [
    {-1, 0},
    { 1, 0},
    {0, -1},
    {0,  1}
  ]

  ROBOTS = [
    {-1, -1},
    { 1,  1},
    {-1,  1},
    { 1, -1}
  ]
  
  property maze = [] of Array(Char)
  property start = {0,0}
  property spaces = 0
  property keys = Set(Char).new
  property robots = Array(Coord).new

  def process(str)
    str.lines.each do |line|
      process_line(line)
    end
    analyse
    @curpos = @start
  end

  def deploy_robots
    ROBOTS.each do |delta|
      dx, dy = delta
      x, y = start
      rx = x + dx
      ry = y + dy
      @robots << {rx,ry}
    end
    DELTAS.each do |delta|
      dx, dy = delta
      x, y = start
      nx = x + dy
      ny = y + dx
      @maze[ny][nx] = '#'
    end
    x, y = start
    @maze[y][x] = '#'
  end

  def neighbors(state)
    curpos, keys = state
    x, y = curpos
    states = [] of State
    DELTAS.each do |delta|
      dy, dx = delta
      nx = x + dx
      ny = y + dy
      ch = at(nx, ny)
      if can_visit?(nx, ny, keys)
        if ch.ascii_lowercase?
          states << { {nx, ny}, keys + Set.new([ch]) }
        else
          states << { {nx, ny}, keys }
        end
      end
    end
    states
  end

  def can_visit?(x,y, keys)
    cell = at(x,y)
    if cell == '#'
      false
    elsif cell.ascii_uppercase?
      key = cell.downcase
      if keys.includes?(key)
        return true
      else
        return false
      end
    else
      return true
    end
  end

  def new_candidates(state)
    neighbors(state)
  end

  def analyse
    @maze.each_with_index do |row, y|
      row.each_with_index do |ch, x|
        @start = {x,y} if ch == '@'
        @spaces += 1 if ch != '#'
        @keys << ch if ch.ascii_lowercase?
      end
    end
  end

  def process_line(line)
    @maze << line.chomp.chars
  end

  def at(x,y)
    @maze[y][x]
  end

  def explore
    keys = Set(Char).new
    frontier = [{start, keys}]
    distances = {} of State => Int32

    distances[{start, keys}] = 0

    #1000.times do
    #if frontier.any?
    while frontier.any?
      new_frontier = [] of State
      frontier.each do |state|
        states = neighbors(state)
        state_distance = distances[state]
        states.each do |nstate|
          if distances[nstate]?
            if distances[nstate] > state_distance + 1
              #Shorter
              raise "Shorter Path"
            end
          else
            #New
            distances[nstate] = state_distance + 1
            new_frontier << nstate
          end
        end
      end
      frontier = new_frontier
   # else
   #   break
    end
    #end
    allkeys = distances.select do |state, cost|
      _, keys = state
      keys == @keys
    end
    shortest = allkeys.min_by {|state, cost| cost }
    p shortest
  end

  def explore_robots
    keys = Set(Char).new
    
    robostates = @robots.dup


    cost = 0
    1000.times do
      if keys == @keys
        puts "FOUND ALL KEYS @#{cost} STEPS"
        break
      end
      robot = robostates.shift
      rstate = {robot,keys}
      frontier = [rstate]
      distances = {rstate => 0 }
      puts "SWITCH: @#{cost} -> #{frontier}"
   # #if frontier.any?
    while frontier.any?
      new_frontier = [] of State
      frontier.each do |state|
        states = neighbors(state)
        state_distance = distances[state]
        states.each do |nstate|
          if distances[nstate]?
            if distances[nstate] > state_distance + 1
              #Shorter
              raise "Shorter Path"
            end
          else
            #New
            distances[nstate] = state_distance + 1
            new_frontier << nstate
          end
        end
      end
      frontier = new_frontier
    end
    bestlet = distances.max_by {|k, v| _, let = k; let.size }
    bstate, _ = bestlet
    _, keys = bstate
    bestkeys = distances.select {|k,v| _, keyset = k; keyset == keys }
    beststate = bestkeys.min_by {|k, v| v }
    bstate, statecost = beststate
    robot, _ = bstate
    #p robot
    cost += statecost
    robostates << robot
    end

  end

  def result
    deploy_robots
    explore_robots
  end

end
