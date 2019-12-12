class Puzzle

  property moons = [] of Tuple(Tuple(Int32, Int32, Int32), Tuple(Int32, Int32, Int32))

  def process(str)
    str.each_line do |line|
      parse_line(line)
    end
  end

  def parse_line(line)
    match = line.match /<x=(.+), y=(.+), z=(.+)>/
    if match
      x = match[1].to_i
      y = match[2].to_i
      z = match[3].to_i
      loc = {x,y,z}
      vel = {0,0,0}
      @moons << {loc,vel}
    else
      raise "NO MATCH:" + line
    end
  end

  def result
    puts "Running."
    initial = @moons.sum {|m| energy(m) }
    start = @moons.map {|m| m }
    puts "Initial Energy: #{initial}"
    count = 0
    batch_size = 1_000_000
    n = 0
    while true
      n += 1
      batch_size.times do
        step
        count +=1
        if @moons.sum {|m| energy(m)} == 0
          if @moons == start
            puts "Repeat @ #{count}"
            return
          end
        end
      end
      puts "#{n*batch_size} steps"
    end
  end
  
  def energy(moon)
    loc, vel = moon
    mx, my, mz = loc
    vx, vy, vz = vel
    pot = mx.abs + my.abs + mz.abs
    kin = vx.abs + vy.abs + vz.abs
    pot * kin
  end

  def step
    @moons = @moons.map do |moon|
      mloc, mvel = moon
      mx, my, mz = mloc
      vx, vy, vz = mvel
      @moons.each do |other|
        next if other == moon
        oloc, _ = other
        ox, oy, oz = oloc
        #puts "#{ox-mx}/#{mx-ox} => #{((ox-mx)/(mx-ox).abs)}"
        #puts "#{oy-my}/#{my-oy} => #{((oy-my)/(my-oy).abs)}"
        #puts "#{oz-mz}/#{mz-oz} => #{((oz-mz)/(mz-oz).abs)}"
        dx = (ox-mx)
        vx += dx//dx.abs unless dx == 0
        dy = (oy-my)
        vy += dy//dy.abs unless dy == 0
        dz = (oz-mz)
        vz += dz//dz.abs unless dz == 0
      end
      nloc = {mx+vx,my+vy,mz+vz}
      nvel = {vx, vy, vz}
      {nloc, nvel}
    end
  end

end
