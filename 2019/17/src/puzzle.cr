require "./intcode"
require "./vacuum_robot"

class Puzzle

  property machine = Intcode.new
  
  def process(str)
    machine.process(str)
  end

  def result
    robot = VacuumRobot.new
    machine.execute([] of Int64, robot)
    puts robot.render
    intersections = robot.locate_intersections
    p intersections
    total = intersections.sum do |i|
      x,y = i
      x*y
    end
    p total
  end

end
