require "spec"
require "./spec_helper"

describe Puzzle do

  it "can determine or when produces raw fuel" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    5 ORE => 1 FUEL
    EOF

    ingredients = puzzle.refine(1)

    ingredients.should eq({"ORE" => 5})
  end

  it "can refine from multiple ingredients" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    1 ORE => 1 B
    1 ORE => 1 A
    1 A, 1 B => 1 FUEL
    EOF

    ingredients = puzzle.refine(1)

    ingredients.should eq({"ORE" => 2})
  end

  it "can refine excess" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    10 ORE => 10 A
    7 A => 1 FUEL
    EOF

    ingredients = puzzle.refine(1)

    ingredients.should eq({"ORE" => 10})
  end

  it "refines first example" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL
    EOF

    ingredients = puzzle.refine(1)

    ingredients.should eq({"ORE" => 31})
  end

  it "refines second example" do
    puts "\n\n=======================\n\n"
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    9 ORE => 2 A
    8 ORE => 3 B
    7 ORE => 5 C
    3 A, 4 B => 1 AB
    5 B, 7 C => 1 BC
    4 C, 1 A => 1 CA
    2 AB, 3 BC, 4 CA => 1 FUEL
    EOF

    ingredients = puzzle.refine(1)

    ingredients.should eq({"ORE" => 165})
  end
end
