require "./intcode"
require "./stdioio"
require "./zork"

class Puzzle
  @instructions = ""
  
  def process(str)
    @instructions = str
  end

  def manual_play
    io = StdIOIO.new
    machine = Intcode.new
    machine.process(@instructions)
    machine.execute io, io
  end

  def robo_play
    robo = Zork.new
    robo.load
    machine = Intcode.new
    machine.process(@instructions)
    machine.execute robo, robo
  end

  def result
    robo_play
  end
end
