require "./intcode"
require "./vacuum_robot"

class Puzzle

  property machine = Intcode.new
  
  def process(str)
    machine.process(str)
  end

  def run_prog(route)
    robot = VacuumRobot.new
    dict, zipped = robot.do_zip(route)
    mapping = ["A","B","C"]
    main = zipped.map {|z| mapping[z] }.join(",")

    input = [] of Int32
    input = main.chars.map {|c| c.ord }
    input << 10 
    dict.each do |fn|
      input += fn.chars.map {|c| c.ord }
      input << 10
    end
    input << 'n'.ord  #No Feed
    input << 10

    i64 = input.map {|i| i.to_i64}

    robot.input = i64
    machine.memory[0] = 2
    output = [] of Int64

    machine.execute(robot, output)
    puts "Dust Gathered: #{output.last}"
  end

  def map_screen
    input = [] of Int64
    robot = VacuumRobot.new
    machine.execute(input, robot)
    #puts robot.render
    robot.build_route
  end

  def result
    machine.save_memory
    route = map_screen
    machine.restore_memory
    run_prog(route)
  end
end
