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

  it "can extract largest function below a given size" do
    robot = VacuumRobot.new
    route = ["R","8","R","8","R","4","R","4","R","8","L","6","L","2","R","4","R","4","R","8","R","8","R","8","L","6","L","2"]
    dict, rest, zipped = robot.zip_function(route.join(","), 15)
    dict.first.should  eq "R,8,R,8,R"
    zipped.should eq [0]
    rest = "4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2"
  end

  it "can compress known fn" do
    robot = VacuumRobot.new
    zipped = [0]
    dict = ["R,8"]
    rest = "R,8,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2"

    dict, rest, zipped = robot.zip_function(rest, 15, dict, zipped)

    zipped.should eq [0,0]
    rest = "4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2"
  end

  it "can limit to 3 functions" do
    robot = VacuumRobot.new
    route = "R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2"
    dict, zipped = robot.do_zip(route)

    dict.size.should eq 3
    zipped.should eq [0,1,0,2,0,0,0,]
  end

  #it "can extract remaining function from a frament set" do
  #  robot = VacuumRobot.new
  #  fragments = [
  #    ["R", "8", "R", "9"],
  #    ["L", "7", "R", "9"],
  #    ["L", "6", "L", "6"]
  #  ]
  #  functions = robot.remaining_functions(fragments)
  #  functions.should eq false
  #  fragments = [
  #    ["R","4","R","4","R","8","L","6","L","2","R","4","R","4","R","8"],
  #    ["L","6","L","2"]
  #  ]

  #  functions = robot.remaining_functions(fragments)
  #  b, c = functions
  #  b.should eq ["R", "4", "R", "4", "R", "8"]
  #  c.should eq ["L", "6", "L", "2"]
  #end
end
