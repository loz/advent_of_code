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

  def map_axis(moons, a)
    moons.map do |moon|
      loc, vel = moon
      {loc[a], vel[a]}
    end
  end

  def result
    puts "Running."
    initial = @moons.sum {|m| energy(m) }
    start = @moons.map {|m| m }
    startx = map_axis(@moons, 0)
    starty = map_axis(@moons, 1)
    startz = map_axis(@moons, 2)
    puts "Initial Energy: #{initial}"
    count = 0
    batch_size = 1_000_000
    n = 0
    repx = 0.to_u64
    repy = 0.to_u64
    repz = 0.to_u64
    while repx == 0 || repy == 0 || repz == 0
      n += 1
        step
        count +=1
        nx = map_axis(@moons, 0)
        ny = map_axis(@moons, 1)
        nz = map_axis(@moons, 2)
        repx = count if nx == startx && repx == 0
        repy = count if ny == starty && repy == 0
        repz = count if nz == startz && repz == 0
    end
    puts "X: #{repx}"
    puts "Y: #{repy}"
    puts "Z: #{repz}"
    max = [repx,repy,repz].max.to_u64
    n = max.to_u64
    while (n % repx) != 0 || (n % repy) != 0 || (n % repz) != 0
        n += max
    end
    puts "Common Cycle :#{n}"
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
