require "./intcode"

class RobotIO
  DIRECTIONS = {
    :N => {
      1 => {1, 0, :E},
      0 => {-1, 0, :W}
    },
    :W => {
      1 => {0, -1, :N},
      0 => {0, 1, :S}
    },
    :E => {
      1 => {0, 1, :S},
      0 => {0, -1, :N}
    },
    :S => {
      1 => {-1, 0, :W},
      0 => {1, 0, :E}
    }
  }
  property panels = {} of Tuple(Int32, Int32) => Int64
  property mode = :paint
  property loc = {0,0}
  property facing = :N

  def color(x,y)
    if panels[{x,y}]?
      panels[{x,y}]
    else
      0.to_i64
    end
  end

  def <<(instruction)
    if mode == :paint
      panels[loc] = instruction.to_i64
      #print "P#{instruction}"
      @mode = :move
    else # :move
      moves = DIRECTIONS[facing][instruction]
      dx, dy, newfacing = moves
      x, y = loc
      x += dx
      y += dy
      @loc = {x, y}
      @facing = newfacing
      #print "M#{instruction}"
      @mode = :paint
    end
  end

  def shift
    x, y = loc
    color(x,y)
  end
end
