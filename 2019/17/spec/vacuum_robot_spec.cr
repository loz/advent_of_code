require "spec"
require "./spec_helper"

describe VacuumRobot do

  it "recieves camera information" do
    robot = VacuumRobot.new
    robot << '#'.ord
    robot << '#'.ord
    robot << '#'.ord
    robot << '\n'.ord
    robot << '#'.ord
    robot << '.'.ord
    robot << '.'.ord

    robot.render.should eq <<-EOF
    ###
    #..
    EOF
  end

  it "can locate intersections" do
    robot = VacuumRobot.new
    map = <<-EOF
    ..#..........
    ..#..........
    #######...###
    #.#...#...#.#
    #############
    ..#...#...#..
    ..#####...^..
    EOF
    map.each_char {|ch| robot << ch.ord }
    
    intertections = robot.locate_intersections
    intertections.should contain({2,2})
    intertections.should contain({2,4})
    intertections.should contain({6,4})
    intertections.should contain({10,4})
  end

  it "can build traversal route" do
    robot = VacuumRobot.new
    map = <<-EOF
    #######...#####
    #.....#...#...#
    #.....#...#...#
    ......#...#...#
    ......#...###.#
    ......#.....#.#
    ^########...#.#
    ......#.#...#.#
    ......#########
    ........#...#..
    ....#########..
    ....#...#......
    ....#...#......
    ....#...#......
    ....#####......
    EOF
    map.each_char {|ch| robot << ch.ord }

    route = robot.build_route.join (",")
    route.should eq "R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2"
  end
end
