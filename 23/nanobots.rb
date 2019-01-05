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

    def distance_to(coord)
      (coord[0] - x).abs + (coord[1] - y).abs + (coord[2] - z).abs
    end

    def in_range(other)
      distance = (other.x - x).abs + (other.y - y).abs + (other.z - z).abs
      #puts "#{self.pos} -> #{other.pos} -> #{distance}"
      distance <= range
    end

    def in_range_coord(coord)
      #puts "Distance, #{pos} -> #{coord} @#{range}"
      distance = distance_to(coord)
      #puts "TRUE" if distance <= range
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
    x = min_x + ((max_x-min_x)/ 2.0)
    y = min_y + ((max_y-min_y)/ 2.0)
    z = min_z + ((max_z-min_z)/ 2.0)
    [x, y, z]
  end

  def distance(coord1, coord2)
    (coord2[0]-coord1[0]).abs +
    (coord2[1]-coord1[1]).abs +
    (coord2[2]-coord1[2]).abs
  end

  def subdivide(bbox, center = nil)
    min_x, min_y, min_z, max_x, max_y, max_z = bbox
    centre ||= centre(bbox)
    mid_x, mid_y, mid_z = centre
    [
      [min_x, min_y, min_z, mid_x.floor, mid_y.floor, mid_z.floor],

      [mid_x.ceil, min_y, min_z, max_x, mid_y.floor, mid_z.floor],
      [min_x, mid_y.ceil, min_z, mid_x.floor, max_y, mid_z.floor],
      [min_x, min_y, mid_z.ceil, mid_x.floor, mid_y.floor, max_z],

      [mid_x.ceil, mid_y.ceil, min_z, max_x, max_y, mid_z.floor],
      [min_x, mid_y.ceil, mid_z.ceil, mid_x.floor, max_y, max_z],
      [mid_x.ceil, min_y, mid_z.ceil, max_x, mid_y.floor, max_z],

      [mid_x.ceil, mid_y.ceil, mid_z.ceil, max_x, max_y, max_z],
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

  def in_bbox_old(bbox)
    min_x, min_y, min_z, max_x, max_y, max_z = bbox
    @bots.select do |bot|
      bot.x >= min_x-bot.range && bot.x <= max_x+bot.range &&
      bot.y >= min_y-bot.range && bot.y <= max_y+bot.range &&
      bot.z >= min_z-bot.range && bot.z <= max_z+bot.range
    end
  end

  def squared(x)
    x * x
  end

  def in_bbox(bbox)
    min_x, min_y, min_z, max_x, max_y, max_z = bbox
    corners = [
      [min_x, min_y, min_z],
      [min_x, min_y, max_z],
      [min_x, max_y, min_z],
      [min_x, max_y, max_z],
      [max_x, min_y, min_z],
      [max_x, min_y, max_z],
      [max_x, max_y, min_z],
      [max_x, max_y, max_z],
    ]
    #def in_range_coord(coord)
    @bots.select do |bot|
      range = false
      in_x = bot.x >= min_x && bot.x <= max_x
      in_y = bot.y >= min_y && bot.y <= max_y
      in_z = bot.z >= min_z && bot.z <= max_z
      in_rx = bot.x >= (min_x-bot.range) && bot.x <= (max_x+bot.range)
      in_ry = bot.y >= (min_y-bot.range) && bot.y <= (max_y+bot.range)
      in_rz = bot.z >= (min_z-bot.range) && bot.z <= (max_z+bot.range)
      #In Corners
      corners.each do |box_c|
        range ||= bot.in_range_coord(box_c)
        #puts "In Range of: #{box_c}" if range
        break if range
      end
      #puts "In Corners #{bbox} > #{bot.pos}:#{bot.range}" if range

      #In Box
      range ||= (in_x && in_y && in_z)

      #In range of faces
      range ||= (in_x && in_y &&
                (bot.in_range_coord([bot.x,bot.y,min_z]) ||
                bot.in_range_coord([bot.x,bot.y,max_z])))
      range ||= (in_x && in_z &&
                (bot.in_range_coord([bot.x,min_y,bot.z]) ||
                bot.in_range_coord([bot.x,max_y,bot.z])) )
      range ||= (in_y && in_z &&
                (bot.in_range_coord([min_x,bot.y,bot.z]) ||
                bot.in_range_coord([max_x,bot.y,bot.z])) )

      range
    end
  end

  def in_bbox_bad(bbox)
    min_x, min_y, min_z, max_x, max_y, max_z = bbox
    @bots.select do |bot|
      dist_squared = squared(bot.range)
      if bot.x < min_x
        dist_squared -= squared(bot.x - min_x)
      elsif bot.x > max_x
        dist_squared -= squared(bot.x - max_x)
      end

      if bot.y < min_y
        dist_squared -= squared(bot.y - min_y)
      elsif bot.y > max_y
        dist_squared -= squared(bot.y - max_y)
      end

      if bot.z < min_z
        dist_squared -= squared(bot.z - min_z)
      elsif bot.z > max_z
        dist_squared -= squared(bot.z - max_z)
      end

      dist_squared > 0
    end
  end
end
