require "spec"
require "./spec_helper"

describe Puzzle do

  it "wires up bots to outputs" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    bot 0 gives low to output 3 and high to output 7
    EOF

    bot = puzzle.bot(0)
    out1 = puzzle.out(3)
    out2 = puzzle.out(7)

    bot.give(3)
    bot.give(22)

    out1.values.should eq [3]
    out2.values.should eq [22]
  end

  it "wires up bots to bots" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    bot 0 gives low to bot 2 and high to bot 1
    bot 1 gives low to output 1 and high to output 2
    bot 2 gives low to output 3 and high to output 4
    EOF

    bot0 = puzzle.bot(0)
    bot1 = puzzle.bot(1)
    bot2 = puzzle.bot(2)
    out2 = puzzle.out(2)
    out4 = puzzle.out(4)

    bot0.give(19)
    bot0.give(42)

    bot1.values.should eq [42]
    bot1.give(5)
    out2.values.should eq [42]

    bot2.values.should eq [19]
    bot2.give(36)
    out4.values.should eq [36]
  end

  it "wires values to bots" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    value 5 goes to bot 9
    bot 9 gives low to output 3 and high to bot 4
    value 99 goes to bot 9
    EOF

    out = puzzle.out(3)
    bot = puzzle.bot(4)
    out.values.should eq [5]
    bot.values.should eq [99]
  end

  describe Bot do
    it "passes inputs to high and low outputs" do
      bot = Bot.new(1)
      out1 = Output.new(1)
      out2 = Output.new(2)
      bot.low = out1
      bot.high = out2

      bot.give(10)
      bot.give(8)
      
      out1.values.should eq [8]
      out2.values.should eq [10]
    end

    it "passes values if already has outputs" do
      out1 = Output.new(1)
      out2 = Output.new(2)

      bot = Bot.new(1)
      bot.give(10)
      bot.give(8)


      bot.low = out1
      bot.high = out2
      
      out1.values.should eq [8]
      out2.values.should eq [10]
    end
  end

end
