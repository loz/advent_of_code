require "spec"
require "./spec_helper"

describe Puzzle do

  it "returns the most frequent letters for columns" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    ffff
    abcd
    abcd
    dcba
    abcd
    eeee
    EOF

    puzzle.code.should eq "abcd"

  end

  it "returns the lease frequent letters for columns" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    ffee
    abcd
    abcd
    abcd
    eeff
    EOF

    puzzle.least_code.should eq "ffee"

  end
end
