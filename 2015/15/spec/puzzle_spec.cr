require "spec"
require "./spec_helper"

describe Puzzle do

  it "can calculate score for recipe" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
    EOF
    
    recipe = {"Butterscotch" => 1, "Cinnamon" => 1}
    score, _ = puzzle.score(recipe)
    score.should eq (-1 + 2) * (-2 + 3) * (6 + -2) * (3 + -1)
  end

  it "can calculate score for example" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
    EOF
    
    recipe = {"Butterscotch" => 44, "Cinnamon" => 56}
    score, _ = puzzle.score(recipe)
    score.should eq 62842880
  end

  it "can scores zero when ingedient negative" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
    EOF
    
    recipe = {"Butterscotch" => 4, "Cinnamon" => 1}
    score, _ = puzzle.score(recipe)
    score.should eq 0
  end

  it "can calculate calories" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
    EOF
    
    recipe = {"Butterscotch" => 40, "Cinnamon" => 60}
    score, cals = puzzle.score(recipe)
    score.should eq 57600000
    cals.should eq 500
  end
end
