class Power
  def cell_power(x,y,serial)
    #rack ID, which is its X coordinate plus 10.
    rackid = x + 10
    #Begin with a power level of the rack ID times the Y coordinate.
    power = rackid * y
    #Increase the power level by the value of the grid serial number
    power += serial
    #Set the power level to itself multiplied by the rack ID.
    power *= rackid
    #Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
    hundred = (power % 1000) - (power % 100)
    hundred = hundred / 100
    #Subtract 5 from the power level.
    power = hundred - 5
  end

  def build_cells(width, height, serial)
    @cells = []
    @width = width
    @height = height
    height.times do |y|
      @cells[y+1] ||= []
      width.times do |x|
        @cells[y+1][x+1] = cell_power(x+1,y+1,serial)
      end
    end
  end

  def calculate_grids(size)
    @grids = []
    x_grids = @width - size
    y_grids = @height - size
    #puts "calculating #{size}x#{size}"
    x_grids.times do |x|
      x=x+1
      y_grids.times do |y|
        y=y+1
        @grids[y] ||= []
        @grids[y][x] = calculate_grid_power(x,y, size)
      end
    end
  end

  def calculate_grid_power(x,y,size)
    power = 0
    size.times do |dx|
      size.times do |dy|
        power += at(x+dx, y+dy)
      end
    end
    power
  end

  def largest_grid
    largest = 0
    largest_location = [0,0]
    @grids.each_with_index do |row, y|
      next if y == 0
      row.each_with_index do |power, x|
        next if x == 0
        if power > largest
          largest = power
          largest_location = [x,y]
        end
      end
    end
    largest_location
  end

  def at(x, y)
    @cells[y][x]
  end

  def grid_power_at(x, y)
    @grids[y][x]
  end

  def dump_at(x, y, size)
    puts "----"
    size.times do |ty|
      row = @cells[y+ty]
      p row[x,size]
    end
    puts "----"
  end
end
