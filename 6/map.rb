class Map

  def initialize
    @points = []
  end

  def calculate_areas
    width, height = finite_size
    #puts "width: %s, height: %s" % [width, height]
    areas = Hash.new { 0 }
    @grid.each_with_index do |row, y|
      if y == 0 || y == height
        #All Infinite
        row.each do |cell|
          areas[cell] = :infinity
        end
      else
        row.each_with_index do |cell, x|
          if x == 0 || x == width
            areas[cell] = :infinity
          else
            unless areas[cell] == :infinity
              areas[cell] += 1
            end
          end
        end
      end
    end
    areas
  end

  def calculate_grid
    width, height = finite_size
    @grid = []
    (height+1).times do |y|
      row = @grid[y] ||= []
      (width+1).times do |x|
        row[x] = closest_point_to_location(x,y)
      end
    end
  end

  def calculate_distance_sums
    width, height = finite_size
    @sums = []
    (height+1).times do |y|
      row = @sums[y] ||= []
      (width+1).times do |x|
        row[x] ||= 0
        row[x] += sum_points_to_location(x,y)
      end
    end
  end

  def sum_below(bad_val)
    total =0
    @sums.each do |row|
      row.each do |cell|
        if cell < bad_val
          total += 1
        end
      end
    end
    total
  end

  def dump_sum(bad_val)
    puts ''
    puts '---------'
    @sums.each do |row|
      row.each do |cell|
        if cell < bad_val
          print '#'
        else
          print '.'
        end
      end
      puts ''
    end
    puts '---------'
  end

  def dump(labels)
    puts ''
    puts '---------'
    @grid.each do |row|
      row.each do |cell|
        print labels[cell]
      end
      puts ''
    end
    puts '---------'
  end

  def sum_at(x,y)
    @sums[y][x]
  end

  def closest_at(x, y)
    @grid[y][x]
  end

  def calculate_distance(p1, p2)
    (p2[:x] - p1[:x]).abs + (p2[:y] - p1[:y]).abs
  end

  def finite_size
    x_points = @points.map { |p| p[:x] }
    max_x = x_points.max || 0

    y_points = @points.map { |p| p[:y] }
    max_y = y_points.max || 0

    [max_x, max_y]
  end

  def sum_points_to_location(x,y)
    distances = distances_from_location(x,y)
    s = 0
    distances.each do |k, v|
      s += v
    end
    s
  end

  def closest_point_to_location(x,y)
    distances = distances_from_location(x,y)
    points = []
    distances.each do |point, distance|
      new_point = {point: point, distance: distance}
      if points.empty?
        points << new_point
      else 
        current = points.first
        if current[:distance] > distance
          points = [new_point]
        elsif current[:distance] == distance
          points << new_point
        end
      end
    end
    if points.count > 1
      {nopoint: true}
    else
      points.first[:point]
    end
  end

  def distances_from_location(x,y)
    start = {x: x, y: y}
    distances = {}
    @points.each do |point|
      distances[point] = calculate_distance(start, point)
    end
    distances
  end

  def add_point(point)
    @points << point
  end

end
