require "./intcode"
require "./vacuum_robot"

class Puzzle

  property machine = Intcode.new
  
  def process(str)
    machine.process(str)
  end

  def scan_line(y, xoffset, scanwidth, display = true)
    dx1 = 0
    dx2 = 0
    width = 0
    first = true
    scanwidth.times do |x|
      output = [] of Int64
      machine.restore_memory
      machine.execute [(x+xoffset).to_i64, y.to_i64], output
      if output == [1]
        if first
          first = false
          dx1 = x+xoffset
        end
        print "#" if display
        width += 1
      else
        print "." if display
      end
    end
    return {width, dx1}
  end

  def run_initial_scan(xoffset, yoffset, sheight = 100 , swidth = 100)
    points = 0
    dx1 = 0
    dx2 = 0
    sheight.times do |y|
      width, dx1 = scan_line(y+yoffset, xoffset, swidth)
      points += width
      dx2 = dx1 + width
      puts " ---> @#{y+yoffset} #{width}, s:#{dx1}"
    end
    dy = 99+yoffset
    puts "Pulled at #{points} points"
    puts "start:   #{dy/dx1}"
    puts "finish:  #{dy/dx2}"
    return {(dy/dx1), (dy/dx2)}
  end
  
  def approximate_scan_line(n, dydx1, dydx2)
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
      start, finish, width = approximate_scan_line(val, dydx1, dydx2)
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
      top_start, top_finish, top_width = approximate_scan_line(y, dydx1, dydx2)
      bot_start, bot_finish, bot_width = approximate_scan_line(y+99, dydx1, dydx2)
      if (bot_start + 99) == top_finish
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

  def do_real_search(xoffset, upper, lower)
    pos = upper
    100.times do
      machine.restore_memory
      top_width, top_start = scan_line(pos, xoffset, xoffset)
      puts "#{top_start} -> #{top_start+top_width}"
      machine.restore_memory
      bot_width, bot_start = scan_line(pos+100, xoffset, xoffset)
      puts "#{bot_start} -> #{bot_start+bot_width}"

      if bot_start + 99 < (top_start + top_width)
        #Not low enough
        lower = pos
      elsif bot_start + 99 > (top_start + top_width)
        #Too high
        upper = pos
      else
        raise "FOUND!"
      end
      puts "Y: #{pos} X:#{bot_start}"
      pos = lower + ((upper - lower) // 2)
    end
  end

  def run_final_scan(xoffset, yoffset, sheight = 100 , swidth = 100)
    points = 0
    dx1 = 0
    dx2 = 0
    sheight.times do |y|
      width, dx1 = scan_line(y+yoffset, xoffset, swidth, false)
      points += width
      dx2 = dx1 + width
      puts " ---> @#{y+yoffset} #{width}, s:#{dx1}"
    end
    dy = 99+yoffset
    puts "Pulled at #{points} points"
    puts "start:   #{dy/dx1}"
    puts "finish:  #{dy/dx2}"
    return {(dy/dx1), (dy/dx2)}
  end

  def test_coord(x,y)
    output = [] of Int64
    machine.restore_memory
    machine.execute [x.to_i64, y.to_i64], output
    if output == [1]
      puts " #{x},#{y} => T"
    else
      puts " #{x},#{y} => F"
    end
  end

  def result
    machine.save_memory
    #run_final_scan(600, 800, height = 300 , width = 500)
    #dydx1, dydx2 = run_initial_scan(0, 0)
    
    dydx1, dydx2 = [1.356164383561644, 1.1]
    start, sx, ex = find_search_start(dydx1, dydx2)
    loc = do_search(start, dydx1, dydx2)
    x, y = loc

    pos = 990
    20.times do
      machine.restore_memory
      top_width, top_start = scan_line(pos, 700, 400, false)
      puts "#{top_start} -> #{top_start+top_width-1}"
      machine.restore_memory
      bot_width, bot_start = scan_line(pos+99, 700, 400, false)
      puts "   #{bot_start} -> #{bot_start+bot_width-1}"
      stop = top_start+top_width-1-99
      sbot = bot_start
      x1 = sbot
      x2 = sbot+99
      y1 = pos
      y2 = pos+99
      test_coord(x1,y1)
      test_coord(x2,y1)
      test_coord(x1,y2)
      test_coord(x2,y2)
      puts "DELTA: @ #{pos} #{stop} vs #{sbot}"
      if stop == sbot
        puts "X: #{stop}, Y:#{pos}"
        break;
      end
      pos += 1
    end
    

   # Approximation:  X: = 814, Y: 1006

    #start, finish, width = approximate_scan_line(1008, dydx1, dydx2)
    #start, finish, width = approximate_scan_line(1008+99, dydx1, dydx2)
    ##do_real_search(500, y-10, x+10)
    
    #do_real_search(500, 1000, 800)
    
    ##run_initial_scan(x-1, y-1)
  end
end
