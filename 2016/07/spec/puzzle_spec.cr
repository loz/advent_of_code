require "spec"
require "./spec_helper"

describe Puzzle do

  it "considers ABBA string tls" do
    puzzle = Puzzle.new

    puzzle.tls?("abba[mnop]qrst").should eq true
  end

  it "does not consider ABBA in [] tls" do
    puzzle = Puzzle.new

    puzzle.tls?("abcd[bddb]xyyx").should eq false
  end

  it "does not consider if ABBA *anywhere* in [] tls" do
    puzzle = Puzzle.new

    puzzle.tls?("xyyxcc[aassf][qwqwbddbqwqw]xyyx").should eq false
  end

  it "does not consider if AAAA in [] as invalid tls" do
    puzzle = Puzzle.new

    puzzle.tls?("xyyxcc[aassf][qwqwbbbbqwqw]xyyx").should eq true
  end

  it "does not consider AAAA string tls" do
    puzzle = Puzzle.new

    puzzle.tls?("aaaa[qwer]tyui").should eq false
  end

  it "does consider an ABBA which is part of AAAA" do
    puzzle = Puzzle.new

    puzzle.tls?("aaaabba[qwer]tyui").should eq true
  end

  it "does not onsider an ABBA which between [] .. [] invalid" do
    puzzle = Puzzle.new

    puzzle.tls?("a[xyx]bottoz[abc]pp").should eq true
  end

  it "does consider AAAA with another ABBA string tls" do
    puzzle = Puzzle.new

    puzzle.tls?("aaaa[qwer]tyuixyyxqwert").should eq true
  end
  it "considers ABA with no [BAB] not ssl" do
    puzzle = Puzzle.new

    puzzle.ssl?("aba[aba]xyz").should eq false
  end

  it "considers ABA [BAB] ssl" do
    puzzle = Puzzle.new

    puzzle.ssl?("aba[bab]xyz").should eq true
  end

  it "considers AAA not to be ssl" do
    puzzle = Puzzle.new

    puzzle.ssl?("aaa[aaa]xyz").should eq false
  end

  it "does not exclude overlaps by accident" do
    puzzle = Puzzle.new

    puzzle.ssl?("zazbz[bzb]cdb").should eq true
  end

  it "does not exclude overlaps by accident, with BAB before" do
    puzzle = Puzzle.new

    puzzle.ssl?("[bzb]zazbzcdb").should eq true
  end

  it "does not exclude overlaps of AAA with ABA" do
    puzzle = Puzzle.new

    puzzle.ssl?("[bzb]zzzbzcdb").should eq true
  end

  it "does not consider ABA wich is also in []" do
    puzzle = Puzzle.new

    puzzle.ssl?("[bzb]abcdef[zbz]").should eq false
  end

  it "does not match when ABA amd BAB in [] with ABA outside" do
    puzzle = Puzzle.new

    puzzle.ssl?("aba[xyzy]").should eq false

  end
end
