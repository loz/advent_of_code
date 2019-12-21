require "spec"
require "./spec_helper"

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
