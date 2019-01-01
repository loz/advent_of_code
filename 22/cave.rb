class Cave

  def initialize(depth, target)
    @depth = depth
    @target = target
    width, height = target
    @geo_index = Array.new(height+1) { Array.new(width+1) }
    @erosion_index = Array.new(height+1) { Array.new(width+1) }

    (width+1).times do |x|
      geo = @geo_index[0][x] = (x) * 16807
      erosion = (geo + @depth) % 20183
      @erosion_index[0][x] = erosion
    end

    (height+1).times do |y|
      geo = @geo_index[y][0] = (y) * 48271
      erosion = (geo + @depth) % 20183
      @erosion_index[y][0] = erosion
    end

    height.times do |y|
      yy = y + 1
      width.times do |x|
        xx = x + 1
        #puts "GEO for #{xx},#{yy}"
        e1 = @erosion_index[yy][xx-1]
        e2 = @erosion_index[yy-1][xx]
        geo = @geo_index[yy][xx] = e1 * e2
        erosion = (geo + @depth) % 20183
        @erosion_index[yy][xx] = erosion
      end
    end

    @geo_index[height][width] = 0 #Target
    @erosion_index[height][width] = @depth #Target
  end
  
  def geo_index(x,y)
    @geo_index[y][x]
  end

  def erosion_level(x,y)
    @erosion_index[y][x]
  end
end
