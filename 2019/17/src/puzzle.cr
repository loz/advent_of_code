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
    p robot.build_route
  end

end
