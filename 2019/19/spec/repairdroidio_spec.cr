require "spec"
require "./spec_helper"

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
