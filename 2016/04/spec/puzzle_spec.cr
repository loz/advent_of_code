require "spec"
require "./spec_helper"

describe Puzzle do

  it "calculates checksums" do
    puzzle = Puzzle.new

    puzzle.checksum("aaaaa-bbb-z-y-x-123").should eq "abxyz"
    puzzle.checksum("a-b-c-d-e-f-g-h-987").should eq "abcde"
    puzzle.checksum("not-a-real-room-404").should eq "oarel"
    puzzle.checksum("totally-real-room-200").should_not eq "decoy"
  end

  it "can get sector from room" do
    puzzle = Puzzle.new

    puzzle.sector("abcdef-1234").should eq 1234
  end

  it "can check a valid room" do
    puzzle = Puzzle.new

    puzzle.valid?("aaaaa-bbb-z-y-x-123[abxyz]").should eq true
    puzzle.valid?("aaaaa-bbb-z-y-x-123[invalid]").should eq false
  end

  it "can sum valid room sectors" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    aaaa-bbb-z-y-x-123[abxyz]
    a-b-c-d-e-f-g-h-987[abcde]
    a-b-casdad-e-f-g-987[xxxxx]
    not-a-real-room-404[oarel]
    totally-real-room-200[decoy]
    EOF

    puzzle.sector_sum.should eq 1514

  end

  it "can translate a room code" do
    puzzle = Puzzle.new
    puzzle.decode("abcdefzz", 1).should eq "bcdefgaa"
    puzzle.decode("abcdefzz", 4+26).should eq "efghijdd"
  end
end
