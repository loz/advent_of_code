require "./intcode"

class VacuumRobot
  property image = [] of Array(Char)
  property curline = [] of Char

  def <<(item)
    ch = item.chr
    case item
      when '\n'
        @image << @curline
        @curline = [] of Char
      else
        @curline << ch
    end
  end
  
  def render
    str = ""
    @image.each do |line|
      str += line.join
      str += '\n'
    end
    str += @curline.join
    str
  end

  def locate_intersections
    all = @image + [@curline]
    all = all.reject {|l| l.empty? }
    intersections = []  of Tuple(Int32,Int32)
    all.each_with_index do |row,y|
      row.each_with_index do |ch,x|
        next if x == 0 || y == 0
        next if x == row.size-1
        next if y == all.size-1
        if ch == '#'
          if all[y-1][x] == '#' &&
             all[y+1][x] == '#' &&
             all[y][x-1] == '#' &&
             all[y][x+1] == '#'
            intersections << {x,y}
            #print 'O'
          #else
            #print '#'
          end
        #else
          #print ch
        end
      end
      #print "\n:>"
    end
    intersections
  end
end
