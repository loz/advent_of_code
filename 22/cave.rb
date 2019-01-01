class Cave

  def initialize(depth, target)
    @depth = depth
    @target = target
    @width, @height = target
    @geo_index = Array.new(@height+1) { Array.new(@width+1) }
    #@erosion_index = Array.new(@height+1) { Array.new(@width+1) }
  end
  
  def geo_index(x,y)
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
end
