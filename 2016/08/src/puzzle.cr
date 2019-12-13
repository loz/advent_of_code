class Puzzle

  property display = [] of Array(Char)

  def initialize
    rows = [] of Array(Char)
    6.times do 
      row = [] of Char
      50.times { row << '.' }
      rows << row
    end
    @display = rows
  end

  def process(str)
    str.each_line do |line|
      process_line line
      #render
      #puts ">---------------------------------------------------"
    end
  end

  def render
    @display.each do |row|
      row.each do |cell|
        print cell
      end
      puts
    end
  end

  def process_line(line)
    parse_rect(line) ||
    parse_rotate_row(line) ||
    parse_rotate_column(line)
  end

  def parse_rect(line)
    rect = line.match /rect (\d+)x(\d+)/
    if rect
      x = rect[1].to_i
      y = rect[2].to_i
      y.times do |y|
        x.times do |x|
          @display[y][x] = '#'
        end
      end
      return true
    end
    return false
  end

  def parse_rotate_row(line)
    row = line.match /rotate row y=(\d+) by (\d+)/
    if row
      y = row[1].to_i
      by = row[2].to_i
      row = @display[y].rotate(0-by)
      @display[y] = row
      return true
    end
    return false
  end

  def parse_rotate_column(line)
    col = line.match /rotate column x=(\d+) by (\d+)/
    if col
      x = col[1].to_i
      by = col[2].to_i
      orig = [] of Char
      @display.each do |row|
        orig << row[x]
      end
      orig = orig.rotate(0-by)
      @display.each_with_index do |row, idx|
        row[x] = orig[idx]
      end
      return true
    end
    return false
  end

  def result
    total = 0
    render
    @display.each do |row|
      total += row.count { |c| c == '#' }
    end
    puts "Total On: #{total}"
  end

  def on?(x,y)
    @display[y][x] == '#'
  end

end
