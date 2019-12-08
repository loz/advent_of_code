require "spec"
require "./spec_helper"

describe Puzzle do

  it "supports hlf register command" do
    puzzle = Puzzle.new
    puzzle.set_register("a", 10)
    puzzle.process("hlf a")

    puzzle.get_register("a").should eq 5
  end

  it "supports tpl register command" do
    puzzle = Puzzle.new
    puzzle.set_register("a", 10)
    puzzle.process("tpl a")

    puzzle.get_register("a").should eq 30
  end

  it "supports inc register command" do
    puzzle = Puzzle.new
    puzzle.process("inc a")

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

    puzzle.get_register("a").should eq 2
  end
end
