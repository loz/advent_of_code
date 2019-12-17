require "./intcode"
require "./vacuum_robot"

class Puzzle

  property machine = Intcode.new
  
  def process(str)
    machine.process(str)
  end

  def run_prog
    robot = VacuumRobot.new
   # puts robot.render
   # route = robot.build_route
   # puts route
    main = "A,B,B,A,C,A,A,C,B,C"
    fa = "R,8,L,12,R,8"
    fb = "R,12,L,8,R,10"
    fc = "R,8,L,8,L,8,R,8,R,10"

    p main.size
    p fa.size
    p fb.size
    p fc.size

    input = main.chars.map {|c| c.ord }
    input << 10 
    input += fa.chars.map {|c| c.ord }
    input << 10
    input += fb.chars.map {|c| c.ord }
    input << 10
    input += fc.chars.map {|c| c.ord }
    input << 10
    input << 'n'.ord  #No Feed
    input << 10


    i64 = input.map {|i| i.to_i64}

    robot.input = i64

    machine.memory[0] = 2
    output = [] of Int64
    machine.execute(robot, output)
    puts output
  end

  def map_screen
    input = [] of Int64
    robot = VacuumRobot.new
    machine.execute(input, robot)
    puts robot.render
    route = robot.build_route
    puts route
  end

  def result
    run_prog
  end
end
