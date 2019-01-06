class Particles
  attr_reader :particles

  class Particle
    attr_accessor :x, :y, :dx, :dy

    def self.from_line(line)
      particle = new
      matches = line.match /position=<(.+),(.+)> velocity=<(.+),(.+)>/
      points = matches.to_a.map {|p| p.to_i }
      points.shift #drop overall match
      particle.set(points)
      particle
    end

    def set(points)
      @x, @y, @dx, @dy = points
    end

    def move(speed)
      @x += (@dx*speed)
      @y += (@dy*speed)
    end

    def to_str
      "(%2s,%2s) [%2s,%2s]" % [x,y,dx,dy]
    end
  end

  def initialize
    @particles = []
  end

  def move(speed = 1)
    @particles.each do |particle|
      particle.move(speed)
    end
  end

  def bounds
    particle = @particles.first

    left = right = particle.x
    top  = bottom = particle.y
    @particles.each do |particle|
     left   = particle.x if particle.x < left
     top    = particle.y if particle.y < top
     right  = particle.x if particle.x > right
     bottom = particle.y if particle.y > bottom 
    end
    [left, top, right, bottom]
  end

  def scale_for(target_width, target_height)
    left, top, right, bottom = bounds
    width = right - left
    height = bottom - top
    target_width = target_width.to_f
    target_height = target_height.to_f
    [target_width/width, target_height/height]
  end

  def add_line(line)
    @particles << Particle.from_line(line)
  end

  def add_lines(lines)
    lines.each_line { |line| add_line(line) }
  end
end
