require "spec"
require "./spec_helper"

describe Puzzle do

  it "supports effectively infinite memory" do
    puzzle = Puzzle.new

    puzzle.at(12334).should eq 0
  end

  it "executes 1 command to add into memory" do
    puzzle = Puzzle.new
    puzzle.process("1,0,0,3,99")
    puzzle.execute

    puzzle.at(3).should eq 2
  end

  it "executes until halts" do
    puzzle = Puzzle.new
    puzzle.process("1,0,0,3,1,3,3,7,99")
    puzzle.execute

    puzzle.at(7).should eq 4
  end

  it "executes 2 command to multiply into memory" do
    puzzle = Puzzle.new
    puzzle.process("2,0,0,3,99")
    puzzle.execute

    puzzle.at(3).should eq 4
  end

  it "executes 3 commands to store inout value" do
    puzzle = Puzzle.new
    puzzle.process("3,0,99")
    puzzle.execute [100.to_i64]

    puzzle.at(0).should eq 100
  end

  it "executes 4 commands to output value" do
    puzzle = Puzzle.new
    puzzle.process("3,0,4,0,99")
    out = puzzle.execute [125.to_i64]
    out.first.should eq 125.to_i64
  end

  it "executes 5 commands to jump-if-true" do
    puzzle = Puzzle.new
    puzzle.process("1105,1,4,123123123,99")
    puzzle.execute
    puzzle.halted.should eq true
  end

  it "executes 6 commands to jump-if-false" do
    puzzle = Puzzle.new
    puzzle.process("1106,0,4,123123123,99")
    puzzle.execute
    puzzle.halted.should eq true
  end

  it "executes 7 commands to less than to 1" do
    puzzle = Puzzle.new
    puzzle.process("11107,2,4,0,99")
    puzzle.execute
    puzzle.at(0).should eq 1
  end

  it "executes 7 commands to gt than to 0" do
    puzzle = Puzzle.new
    puzzle.process("11107,4,2,0,99")
    puzzle.execute
    puzzle.at(0).should eq 0
  end

  it "executes 8 commands to equals to 1" do
    puzzle = Puzzle.new
    puzzle.process("11108,2,2,0,99")
    puzzle.execute
    puzzle.at(0).should eq 1
  end

  it "executes 8 commands to equals to 0" do
    puzzle = Puzzle.new
    puzzle.process("11108,4,2,0,99")
    puzzle.execute
    puzzle.at(0).should eq 0
  end

  it "supports parameter modes for instructions" do
    puzzle = Puzzle.new
    puzzle.process("1002,4,3,4,33")
    puzzle.execute
    puzzle.at(4).should eq 99
  end

  it "supports relative mode" do
    puzzle = Puzzle.new
    puzzle.process("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
    output = [] of Int64
    puzzle.execute output, output

    puzzle.halted.should eq true
    output.should eq [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
  end

  it "supports large numbers" do
    puzzle = Puzzle.new
    puzzle.process("1102,34915192,34915192,7,4,7,99,0")
    output = [] of Int64
    puzzle.execute output, output
    output.first.to_s.size.should eq 16
  end

  it "supports other large numbers" do
    puzzle = Puzzle.new
    puzzle.process("104,1125899906842624,99")
    output = [] of Int64
    puzzle.execute output, output
    output.first.should eq 1125899906842624
  end
  it "supports large numbers" do
    puzzle = Puzzle.new
    puzzle.process("1102,34915192,34915192,7,4,7,99,0")
    output = [] of Int64
    puzzle.execute output, output
    output.first.to_s.size.should eq 16
  end
end

describe IOPipe do
  it "can have data put in and out" do
    pipe = IOPipe.new
    pipe << 1234.to_i64
    pipe.shift.should eq 1234.to_i64
  end

  it "blocks a read until data arrives" do
    pipe = IOPipe.new
    spawn do
      read = pipe.shift
      read.should eq 1234.to_i64
    end
    sleep 1.seconds
    pipe << 1234.to_i64
  end
end

describe ScreenIO do
  it "put empty tile at x,y" do
    screen = ScreenIO.new
    screen << 10.to_i64
    screen << 24.to_i64
    screen << 0.to_i64
    screen.at(10,24).should eq :empty
  end

  it "put wall tile at x,y" do
    screen = ScreenIO.new
    screen << 13.to_i64
    screen << 21.to_i64
    screen << 1.to_i64
    screen.at(13,21).should eq :wall
  end

  it "will handle score" do
    screen = ScreenIO.new
    screen << -1.to_i64
    screen << 0.to_i64
    screen << 2435.to_i64

    screen.score.should eq 2435.to_i64
  end
end

describe RepairDroidIO do
  it "goes N when possible" do
    robot = RepairDroidIO.new
    robot.visit(:N)
    dir = robot.shift
    dir.should eq 1
    robot << 1 #Did Move
    robot.x.should eq 0
    robot.y.should eq -1
  end

  it "does not goes N/S/E/W when a wall encountered" do
    robot = RepairDroidIO.new
    robot.visit(:W)
    dir = robot.shift
    dir.should eq 3
    robot << 0 #Did not
    robot.x.should eq 0
    robot.y.should eq 0
  end

  it "will choose to explore unexplored when asked for a move" do
    robot = RepairDroidIO.new
    robot.visited << {0,-1} #:N
    robot.visited << {-1,0} #:W
    robot.visited << {0, 1} #:S
    dir = robot.shift
    dir.should eq 4
  end

  it "will move back to previous location when no new neighbors to visit" do
    robot = RepairDroidIO.new
    robot.visited << {0,-1} #:N
    robot.visited << {-1,0} #:W
    robot.visited << {0, 1} #:S
    robot.visited << {1, 0} #:E
    robot.current_path = [{:E, {-1,0}}]
    dir = robot.shift
    dir.should eq 3
  end

  it "considered walls hit visited locations" do
    robot = RepairDroidIO.new
    robot.visit(:W)
    dir = robot.shift
    dir.should eq 3
    robot << 0 #Hit A Wall

    robot.visited?({-1,0}).should eq true
  end

  it "tracks unexplored neigbors" do
    robot = RepairDroidIO.new
    dir = robot.shift
    dir.should eq 4
    robot << 1 #Did

    robot.unexplored.should contain({0, -1})
    robot.unexplored.should contain({0,  1})
    robot.unexplored.should contain({-1, 0})
  end

  it "removes unexplored neigbors when visiting" do
    robot = RepairDroidIO.new
    robot.unexplored << {1,0}
    dir = robot.shift
    dir.should eq 4
    robot << 1 #Did

    robot.unexplored.should_not contain({1, 0})
  end

  it "it tracks the current path" do
    robot = RepairDroidIO.new
    robot.visit(:E)
    dir = robot.shift
    dir.should eq 4
    robot << 1 #Did Move

    robot.visited?({1,0}).should eq true
    robot.current_path.should eq [{:E, {0,0}}]
  end

  it "it does not add to the current path when reverting" do
    robot = RepairDroidIO.new
    robot.reverting = true
    robot.visit(:E)
    dir = robot.shift
    dir.should eq 4
    robot << 1 #Did Move

    robot.current_path.should_not eq [{:E, {0,0}}]
    robot.reverting.should eq false
  end

  it "it recognise when target found" do
    robot = RepairDroidIO.new
    robot.visit(:E)
    dir = robot.shift
    dir.should eq 4
    robot << 1 #Did Move
    robot.found.should eq false
    robot.visit(:E)
    robot << 2 #Moved and FOUND
    robot.found.should eq true
    robot.current_path.should eq [{:E, {0,0}}, {:E, {1, 0}}]
  end
end

describe RobotIO do
  it "paints location when receiving a color" do
    robot = RobotIO.new
    robot << 1
    robot.color(0,0).should eq 1
  end

  it "reads current color from location" do
    robot = RobotIO.new
    robot << 0
    color = robot.shift
    color.should eq 0
    color = robot.shift
    color.should eq 0
  end

  it "supports left turn after painting" do
    robot = RobotIO.new
    robot << 0
    robot << 0
    robot.loc.should eq({-1,0})
    robot.facing.should eq :W
  end

  it "supports left turn after painting" do
    robot = RobotIO.new
    robot << 0
    robot << 1
    robot.loc.should eq({1,0})
    robot.facing.should eq :E
  end
end
