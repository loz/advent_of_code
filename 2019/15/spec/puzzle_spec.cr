require "spec"
require "./spec_helper"

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
