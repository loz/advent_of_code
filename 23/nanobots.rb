class Nanobots
  attr_reader :bots

  class Bot
    attr_accessor :range, :x, :y, :z

    def initialize(x, y, z, r)
      @x = x; @y = y; @z = z;
      @range = r;
    end

    def pos
      [@x, @y, @z]
    end

    def in_range(other)
      distance = (other.x - x).abs + (other.y - y).abs + (other.z - z).abs
      #puts "#{self.pos} -> #{other.pos} -> #{distance}"
      distance <= range
    end
  end

  def initialize
    @bots = []
  end

  def bounding_box
    f = @bots.first
    min_x = max_x = f.x
    min_y = max_y = f.y
    min_z = max_z = f.z
    @bots.each do |b|
      min_x = b.x if b.x < min_x
      max_x = b.x if b.x > max_x
      min_y = b.y if b.y < min_y
      max_y = b.y if b.y > max_y
      min_z = b.z if b.z < min_z
      max_z = b.z if b.z > max_z
    end
    [min_x, min_y, min_z, max_x, max_y, max_z]
  end

  def centre(bbox)
    min_x, min_y, min_z, max_x, max_y, max_z = bbox
    x = min_x + ((max_x-min_x)/ 2)
    y = min_y + ((max_y-min_y)/ 2)
    z = min_z + ((max_z-min_z)/ 2)
    [x, y, z]
  end

  def subdivide(bbox, center = nil)
    min_x, min_y, min_z, max_x, max_y, max_z = bbox
    centre ||= centre(bbox)
    mid_x, mid_y, mid_z = centre
    [
      [min_x, min_y, min_z, mid_x, mid_y, mid_z],
      [mid_x, min_y, min_z, max_x, mid_y, mid_z],
      [min_x, mid_y, min_z, mid_x, max_y, mid_z],
      [mid_x, mid_y, min_z, max_x, max_y, mid_z],
      [min_x, min_y, mid_z, mid_x, mid_y, max_z],
      [mid_x, min_y, mid_z, max_x, mid_y, max_z],
      [min_x, mid_y, mid_z, mid_x, max_y, max_z],
      [mid_x, mid_y, mid_z, max_x, max_y, max_z],
    ]
  end

  def add(definition)
    matches = definition.match(/pos=<(.+),(.+),(.+), r=(.+)/)
    _, x, y, z, r = matches.to_a.map &:to_i
    @bots << Bot.new(x,y,z,r)
  end

  def greatest_range
    @bots.max {|b1, b2| b1.range <=> b2.range }
  end

  def nearest_to(coord)
    x, y, z = coord
    bot = Bot.new(x, y, z, 0)
    @bots.select {|b| b.in_range(bot)}
  end

  def nearest(target)
    @bots.select {|b| target.in_range(b)}
  end

  def weighted_average(bots=nil)
    bots ||= @bots
    sum_x = sum_y = sum_z = 0
    total = bots.count
    bots.each do |b|
      x, y, z = b.pos
      sum_x += x
      sum_y += y
      sum_z += z
    end
    [sum_x/total, sum_y/total, sum_z/total]
  end

  def in_bbox(bbox)
    min_x, min_y, min_z, max_x, max_y, max_z = bbox
    @bots.select do |bot|
      bot.x >= min_x-bot.range && bot.x <= max_x+bot.range &&
      bot.y >= min_y-bot.range && bot.y <= max_y+bot.range &&
      bot.z >= min_z-bot.range && bot.z <= max_z+bot.range
    end
  end
end
