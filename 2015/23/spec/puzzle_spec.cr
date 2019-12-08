require "spec"
require "./spec_helper"

describe Puzzle do

  it "supports hlf register command" do
    puzzle = Puzzle.new
    puzzle.set_register("a", 10)
    puzzle.process("hlf a")

    puzzle.execute

    puzzle.get_register("a").should eq 5
  end

  it "supports tpl register command" do
    puzzle = Puzzle.new
    puzzle.set_register("a", 10)
    puzzle.process("tpl a")

    puzzle.execute

    puzzle.get_register("a").should eq 30
  end

  it "supports inc register command" do
    puzzle = Puzzle.new
    puzzle.process("inc a")

    puzzle.execute

    puzzle.get_register("a").should eq 1
  end

  it "supports jmp command" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    inc a
    jmp +2
    inc a
    inc a
    EOF

    puzzle.execute

    puzzle.get_register("a").should eq 2
  end

  it "supports jie command" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    inc a
    jie a, +2
    inc a
    jie a, +2
    inc a
    inc a
    EOF

    puzzle.execute

    puzzle.get_register("a").should eq 3
  end

  it "supports jio command" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    inc a
    jio a, +3
    inc a
    inc a
    inc a
    jio a, -1
    inc a
    EOF

    puzzle.execute

    puzzle.get_register("a").should eq 3
  end
end
