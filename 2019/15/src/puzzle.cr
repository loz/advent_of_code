require "./intcode"
require "./repairdroid"

class Puzzle

  property machine = Intcode.new
  
  def process(str)
    machine.process(str)
  end

  def result
    droid = RepairDroidIO.new
    #droid.draw = true
    machine.execute(droid, droid)
    p droid.found
    p droid.current_path
  end

end
