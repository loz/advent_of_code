require "./intcode"

class ScreenIO
  property screen = {} of Tuple(Int64,Int64) => Symbol
  property mode = :locx
  property x : Int64
  property y : Int64
  property score : Int64
  property scores = [] of Int64
  property ballx : Int64
  property paddlex : Int64

  TILE = {
    0 => :empty,
    1 => :wall,
    2 => :block,
    3 => :paddle,
    4 => :ball
  }

  CHAR = {
    :empty => ' ',
    :wall => '#',
    :block => '=',
    :paddle => '_',
    :ball => 'O'
  }

  def initialize
    @x = 0.to_i64
    @y = 0.to_i64
    @ballx = 0.to_i64
    @paddlex = 0.to_i64
    @score = 0.to_i64
  end

  def render
    23.times do |y|
      37.times do |x|
        print CHAR[at(x,y)]
      end
      puts
    end
  end

  def shift
    if @paddlex < @ballx
      1.to_i64
    elsif @paddlex > @ballx
      -1.to_i64
    else
      0.to_i64
    end
  end

  def <<(val)
    case @mode
      when :locx
        @x = val
        @mode = :locy
      when :locy
        @y = val
        @mode = :tile
      when :tile
        if @x == -1 && @y == 0
          @score = val
          @scores << val
          #print "\033[1;3f SCORE: #{val} "
        else
          bloc = TILE[val]
          @screen[{@x,@y}] = bloc
          #Render
          #print "\033[#{@y+1};#{@x+1}f#{CHAR[bloc]}"
          @paddlex = x if bloc == :paddle
          if bloc == :ball
            @ballx = x
          end
        end
        @mode = :locx
    end
  end

  def at(x,y)
    @screen[{x,y}]
  end
end
