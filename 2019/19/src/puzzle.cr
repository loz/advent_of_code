require "./intcode"
require "./vacuum_robot"

class Puzzle

  property machine = Intcode.new
  
  def process(str)
    machine.process(str)
  end

  def run_initial_scan(xoffset, yoffset)
    machine.save_memory
    points = 0
    dx1 = 0
    dx2 = 0
    100.times do |y|
      width = 0
      first = true
      100.times do |x|
        output = [] of Int64
        machine.restore_memory
        machine.execute [(x+xoffset).to_i64, (y+yoffset).to_i64], output
        if output == [1]
          if first
            first = false
            dx1 = x
          end
          print "#"
          points += 1
          width += 1
        else
          print "."
        end
      end
      dx2 = dx1 + width
      puts " -> #{width} @#{y+yoffset} dx:#{dx1} dx2:#{dx2}"
    end
    dy = 99+yoffset
    puts "Pulled at #{points} points"
    puts "start:   #{dy/dx1}"
    puts "finish:  #{dy/dx2}"
    return {(dy/dx1), (dy/dx2)}
  end
  
  def calcrow(n, dydx1, dydx2)
    start = (n.to_i64 / dydx1).to_i64
    finish = (n.to_i64 / dydx2).to_i64
    width = finish - start
    {start, finish, width}
  end

  def find_search_start(dydx1, dydx2)
    lower = 100
    upper = 10_000_000
    val = upper
    100.times do
      start, finish, width = calcrow(val, dydx1, dydx2)
      puts "@#{val} #{width}, s:#{start}, f:#{finish}"
      if width > 100
        upper = val
      elsif width < 100
        lower = val
      else
        return {val, start, finish}
      end
      val = lower + ((upper - lower) // 2)
    end
    return {0, 0, 0}
  end

  def do_search(start, dydx1, dydx2)
    y = start + 100
    x = 0
    1000.times do 
      top_start, top_finish, top_width = calcrow(y, dydx1, dydx2)
      bot_start, bot_finish, bot_width = calcrow(y+100, dydx1, dydx2)
      if (bot_start + 100) <= top_finish
        print "@#{y} #{top_width}, s:#{top_start}, f:#{top_finish}"
        print "---> #{bot_width}, s:#{bot_start}, f:#{bot_finish}"
        puts " -> FITS"
        x = bot_start
        puts "X: = #{x}, Y: #{y}"
        break;
      end
      y += 1
    end
    {x, y}
  end

  def result
    #dydx1, dydx2 = run_initial_scan(0, 0)
    dydx1, dydx2 = [1.356164383561644, 1.1]
    start, sx, ex = find_search_start(dydx1, dydx2)
    loc = do_search(start, dydx1, dydx2)
    x, y = loc
    run_initial_scan(x-1, y-1)
  end
end
