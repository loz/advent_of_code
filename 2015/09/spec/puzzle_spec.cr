require "spec"
require "./spec_helper"

describe Puzzle do

  it "povides destinations" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141
    EOF
    
    puzzle.destinations.size.should eq 3
    puzzle.destinations.should contain "London"
    puzzle.destinations.should contain "Dublin"
    puzzle.destinations.should contain "Belfast"
  end

  it "knows distances given" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141
    EOF
    
    puzzle.distance("London", "Dublin").should eq 464
  end

  it "kowns distances both directions" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141
    EOF
    
    puzzle.distance("Dublin", "London").should eq 464
  end

  it "can caclulate permutations for trips" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141
    EOF
    
    puzzle.possible_routes.size.should eq 6
    puzzle.possible_routes.should contain ["Dublin", "London", "Belfast"]
    puzzle.possible_routes.should contain ["Belfast", "London", "Dublin"]
  end

  it "can caclulate distance for a route" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141
    EOF
    
    puzzle.distance_for(["Belfast", "London", "Dublin"]).should eq 982
  end

  it "can calculate the shortest route" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141
    EOF
    
    path, length = puzzle.shortest
    path.should eq ["London", "Dublin", "Belfast"]
    length.should eq 605
  end

  it "can calculate the longest route" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141
    EOF
    
    path, length = puzzle.longest
    path.should eq ["Dublin", "London", "Belfast"]
    length.should eq 982
  end
end
