class Puzzle
  
  @stats = {} of String => Tuple(Int32, Int32, Int32)
  @reindeers = [] of String

  def process(str)
    reindeers = [] of String
    str.each_line do |line|
      name = process_line line
      reindeers << name
    end
    @reindeers = reindeers.uniq
  end

  def speed(reindeer)
    s, _, _ = @stats[reindeer]
    s
  end

  def stamina(reindeer)
    _, s, _ = @stats[reindeer]
    s
  end

  def rest(reindeer)
    _, _, r = @stats[reindeer]
    r
  end

  def process_line(line)
    match = line.match /(.*) can fly (\d+) km\/s for (\d+) seconds, but then must rest for (\d+) seconds\./
    if match
      name = match[1]
      speed = match[2].to_i
      stamina = match[3].to_i
      rest = match[4].to_i
      @stats[name] = {speed, stamina, rest}
      name
    else
      puts "Failed To Parse! #{line}"
      "??"
    end
  end

  def distance_after(time, reindeer)
    speed, stamina, rest = @stats[reindeer]
    cycletime = stamina + rest

    rests = (time / cycletime).to_i
    midcycle = time % cycletime
    midruntime = [midcycle, stamina].min

    resttime = rests * rest
    middistance = midruntime * speed
    runtime = rests * (speed * stamina) + middistance

    #puts "#{reindeer} -> #{rests} rests, #{midcycle} in cycle -> #{runtime} travelled"
    runtime
  end

  def points_at(time)
    distances = {} of String => Int32
    points = {} of String => Int32
    winning = 0
    @reindeers.each do |reindeer|
      distance = distance_after(time, reindeer)
      winning = distance if distance > winning
      distances[reindeer] = distance
    end
    @reindeers.each do |reindeer|
      if distances[reindeer] == winning
        points[reindeer] = 1
      else 
        points[reindeer] = 0
      end
    end
    points
  end

  def result
    scores = {} of String => Int32
    @reindeers.each {|reindeer| scores[reindeer] = 0 }
    2503.times do |t|
      time = t+1
      print '.'
      leg = points_at(time)
      @reindeers.each {|r| scores[r] += leg[r]}
      p scores
    end
  end

end
