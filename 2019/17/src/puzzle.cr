require "./intcode"
require "./vacuum_robot"

class Puzzle

  property machine = Intcode.new
  
  def process(str)
    machine.process(str)
  end

  def result
    robot = VacuumRobot.new
   # puts robot.render
   # route = robot.build_route
   # puts route
    main = "A,B,B,A,C,C,B,C"
    fa = "R,8,L,12,R,8"
    fb = "R,12,L,8,R,10"
    fc = "R,8,L,8,L,8,R,8,R,10"

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

    machine.memory[0] = 2
    output = [] of Int64
    machine.execute(i64, output)
    puts output
  end
end
