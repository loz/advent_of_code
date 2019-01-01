class Cave

  def initialize(depth, target)
    @depth = depth
    @target = target
    @width, @height = target
  end
  
  def geo_index(x,y)
    return 0 if x == @width && y == @height
    if x == 0
      return y * 48271
    elsif y == 0
      return x * 16807
    else
      e1 = erosion_level(x-1,y)
      e2 = erosion_level(x,y-1)
      return e1 * e2
    end
  end

  def erosion_level(x,y)
    return (geo_index(x,y) + @depth) % 20183
  end
end
