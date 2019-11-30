class Puzzle
  property destinations = [] of String
  property distances = {} of Tuple(String,String) => Int32
  property possible_routes = [] of Array(String)
  property paths = {} of Array(String) => Int32

  def process(str)
    str.lines.each do |line|
      loc1, loc2, distance = parse_line(line)
      destinations << loc1
      destinations << loc2
      distances[{loc1,loc2}] = distance
      distances[{loc2,loc1}] = distance
    end
    destinations.uniq!
    @possible_routes = destinations.permutations
    @possible_routes.each do |path|
      @paths[path] = distance_for(path)
    end
  end

  def shortest
    short = @paths.keys.min_by {|k| @paths[k] }
    {short, @paths[short]}
  end

  def longest
    long = @paths.keys.max_by {|k| @paths[k] }
    {long, @paths[long]}
  end

  def distance(loc1, loc2)
    distances[{loc1,loc2}]
  end

  def distance_for(path)
    route = path.dup
    cur = route.shift
    travel = 0
    while !route.empty?
      dest = route.shift
      travel += distance(cur,dest)
      cur = dest
    end
    travel
  end

  def result
    puts "Destinations", destinations
    puts "Permutations", possible_routes.size
    short, dist = shortest
    puts "Shortest", short
    puts "Distance", dist
    long, dist = longest
    puts "Longest", long
    puts "Distance", dist
  end

  def parse_line(l)
    loc1, rest = l.split(" to ")
    loc2, rest = rest.split(" = ")
    {loc1, loc2, rest.to_i}
  end

end
