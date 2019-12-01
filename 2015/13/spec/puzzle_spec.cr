require "spec"
require "./spec_helper"

describe Puzzle do

  it "it knows gains for people" do
    puzzle = Puzzle.new
    puzzle.process("Alice would gain 54 happiness units by sitting next to Bob.")

    puzzle.happiness("Alice", "Bob").should eq 54
  end

  it "it knows lose for people" do
    puzzle = Puzzle.new
    puzzle.process("Bob would lose 63 happiness units by sitting next to David.
")

    puzzle.happiness("Bob", "David").should eq -63
  end

  it "knows all the people at the table" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    Alice would gain 54 happiness units by sitting next to Bob.
    Alice would lose 79 happiness units by sitting next to Carol.
    Alice would lose 2 happiness units by sitting next to David.
    Bob would gain 83 happiness units by sitting next to Alice.
    Bob would lose 7 happiness units by sitting next to Carol.
    Bob would lose 63 happiness units by sitting next to David.
    Carol would lose 62 happiness units by sitting next to Alice.
    Carol would gain 60 happiness units by sitting next to Bob.
    Carol would gain 55 happiness units by sitting next to David.
    David would gain 46 happiness units by sitting next to Alice.
    David would lose 7 happiness units by sitting next to Bob.
    David would gain 41 happiness units by sitting next to Carol.
    EOF

    puzzle.people.size.should eq 4
    puzzle.people.should contain "Bob"
    puzzle.people.should contain "David"
  end

  it "can caluclate change based on seating" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    Alice would gain 54 happiness units by sitting next to Bob.
    Alice would lose 79 happiness units by sitting next to Carol.
    Alice would lose 2 happiness units by sitting next to David.
    Bob would gain 83 happiness units by sitting next to Alice.
    Bob would lose 7 happiness units by sitting next to Carol.
    Bob would lose 63 happiness units by sitting next to David.
    Carol would lose 62 happiness units by sitting next to Alice.
    Carol would gain 60 happiness units by sitting next to Bob.
    Carol would gain 55 happiness units by sitting next to David.
    David would gain 46 happiness units by sitting next to Alice.
    David would lose 7 happiness units by sitting next to Bob.
    David would gain 41 happiness units by sitting next to Carol.
    EOF

    puzzle.change(["David", "Alice", "Bob", "Carol"]).should eq 330
  end

  it "can insert a neutral self" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    Alice would gain 54 happiness units by sitting next to Bob.
    Alice would lose 79 happiness units by sitting next to Carol.
    Alice would lose 2 happiness units by sitting next to David.
    Bob would gain 83 happiness units by sitting next to Alice.
    Bob would lose 7 happiness units by sitting next to Carol.
    Bob would lose 63 happiness units by sitting next to David.
    Carol would lose 62 happiness units by sitting next to Alice.
    Carol would gain 60 happiness units by sitting next to Bob.
    Carol would gain 55 happiness units by sitting next to David.
    David would gain 46 happiness units by sitting next to Alice.
    David would lose 7 happiness units by sitting next to Bob.
    David would gain 41 happiness units by sitting next to Carol.
    EOF

    puzzle.insert_me
    puzzle.people.should contain "Me"

    puzzle.happiness("Bob", "Me").should eq 0
    puzzle.happiness("Me", "David").should eq 0

  end
end
