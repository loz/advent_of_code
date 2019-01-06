TOOL_CHANGE = {
  [0, :torch] => :gear, #ROCK
  [0, :gear] => :torch,
  [1, :gear] => :neither, #WET
  [1, :neither] => :gear,
  [2, :torch] => :neither, #NARROW
  [2, :neither] => :torch
}

MOVE_COSTS = {
  [:torch,   0] => 1,
  [:torch,   1] => 8,
  [:torch,   2] => 1,
  [:gear,    0] => 1,
  [:gear,    1] => 1,
  [:gear,    2] => 8,
  [:neither, 0] => 8,
  [:neither, 1] => 1,
  [:neither, 2] => 1,
}

TOOL_OK = {
  [0, :torch] => true, #ROCK
  [0, :gear] => true,
  [1, :gear] => true, #WET
  [1, :neither] => true,
  [2, :torch] => true, #NARROW
  [2, :neither] => true 
}

DIRECTIONS = [
  [ 0, -1], #N
  [-1,  0], #W
  [ 1,  0], #E
  [ 0,  1]  #S
]

class PriorityQueue
  def initialize(node)
    @nodes = [node]

    @distance = Hash.new { 999_999_999_999 }
    @distance[node] = 0
  end

  def distance(node, value=nil)
    if value
      @distance[node] = value
    else
      @distance[node]
    end
  end

  def empty?
    @nodes.empty?
  end

  def add(node)
    @nodes << node
  end

  def pop
    @nodes.sort! do |n1, n2|
      @distance[n1] <=> @distance[n2]
    end
    @nodes.pop
  end
end

class Cave

  def initialize(depth, target)
    @depth = depth
    @target = target
    @width, @height = target
    @geo_index = []
    #@erosion_index = Array.new(@height+1) { Array.new(@width+1) }
  end
  
  def geo_index(x,y)
    @geo_index[y] ||= []
    geo = @geo_index[y][x]
    return geo if geo
    return 0 if x == @width && y == @height
    if x == 0
      return y * 48271
    elsif y == 0
      return x * 16807
    else
      e1 = erosion_level(x-1,y)
      e2 = erosion_level(x,y-1)
      geo = e1 * e2
      @geo_index[y][x] = geo
      return geo
    end
  end

  def erosion_level(x,y)
    return (geo_index(x,y) + @depth) % 20183
  end

  def risk(x,y)
    erosion_level(x,y) % 3
  end

  def total_risk
    total = 0
      (@height+1).times do |y|
        (@width+1).times do |x|
          total += risk(x,y)
        end
      end
    total
  end

  def cost(route)
    total = 0
    last = nil
    route.each do |step|
      _, tool = step
      if last == nil
      else
        if tool == last
          total += 1
        else
          total += 7
        end
      end
      last = tool
    end
    total
  end

  def Xnavigate(start, goal)
    prev = {}
    explored = {}

    frontier = PriorityQueue.new(start)
    while true do
      if frontier.empty?
        raise "No Route!"
      end
      current = frontier.pop
      if current == goal
        raise "Solution"
      end

      neighbours(current).each do |neighbour|
        unless explored[neighbour]
          alt = frontier.distance(current) + cost([current,neighbour])
          if alt < frontier.distance(neighbour)
            frontier.distance(neighbour,alt)
            prev[neighbour] = current
          end
          explored[neighbour] = true
          frontier.add(neighbour)
        end
      end
    end
  end

  def navigate(start, goal)
    closed_set = {}
    open_set = {}
    open_set[start] = true
    came_from = {}
    gScore = Hash.new { 999_999_999_999 }
    fScore = Hash.new { 999_999_999_999 }
    gScore[start] = 0
    fScore[start] = estimated_cost(start, goal)

    while !open_set.empty? do
      current = best_score(fScore, open_set, goal)
      #puts "Current #{current}"
      if current == goal
        #puts "Route Found.. Construct"
        #p came_from
        return construct_route(came_from, current)
      else
        open_set.delete current
        closed_set[current] = true
        if closed_set.length % 100 == 0
          print  "%s @ %s > " % [current, closed_set.length]
        end

        possible = neighbours(current)
        possible.each do |neighbour|
          #puts "N: #{neighbour}"
          if closed_set[neighbour]
            next
          end

          tentative_gScore = gScore[current] + cost([current, neighbour])
          #puts "Score: #{tentative_gScore}"
          if !open_set.include? neighbour
            open_set[neighbour] = true
          elsif tentative_gScore >= gScore[neighbour]
            next
          end
          #This path is the best until now. Record it!
          came_from[neighbour] = current
          gScore[neighbour] = tentative_gScore
          fScore[neighbour] = tentative_gScore + estimated_cost(neighbour, goal)
        end
      end
    end
  end

  private

  def construct_route(routes, node)
    path = [node]
    while !routes[node].nil? do
      node = routes[node]
      path.unshift node
    end
    path
  end

  def best_score(scores, set, goal)
    min = set.keys.min { |l1, l2| scores[l1] <=> scores[l2] }
    min = scores[min]
    best = set.keys.select {|loc| scores[loc] == min }
    best.sort! do |l1,l2|
      manhatten(l1,goal) <=> manhatten(l2,goal)
    end

    best.first
  end

  def manhatten(p1, p2)
    pos1, _ = p1
    pos2, _ = p2
    ((pos1[0] - pos2[0]).abs + (pos1[1] - pos2[1]).abs)
  end

  def estimated_cost(src, dest)
    rest = manhatten(src,dest) - 1

    neighbours = neighbours(src)
    sp, _ = src
    costs = neighbours.map do |n|
      np, _ = n
      if np[0] < sp[0]
        cost([src,n]) + 2 + rest
      elsif np[1] < sp[0]
        cost([src,n]) + 2 + rest
      else
        cost([src,n]) + rest
      end
    end
    #p "Cost N: %s" % costs.inspect
    costs.min
  end
  
  def neighbours(start)
    pos, tool = start

    neighbours = []
    x, y = pos
    type = risk(x, y)
    DIRECTIONS.each do |d|
      dx, dy = d
      nx = x + dx
      ny = y + dy
      next if nx < 0 || ny < 0
      next if nx > @width+100 || ny > @height+100
      ntype = risk(nx, ny)
      #puts "Tool OK #{ntype}:#{tool}? (#{[nx,ny]})"
      neighbours << [[nx,ny], tool] if TOOL_OK[[ntype, tool]]
    end
    neighbours << [pos, TOOL_CHANGE[[type, tool]]]
    neighbours
  end
end
