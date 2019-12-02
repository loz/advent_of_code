require "spec"
require "./spec_helper"

describe Puzzle do

  it "parses maps" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    H => HO
    O => HH

    HOH
    EOF

    puzzle.maps("H").should eq ["HO"]
    puzzle.maps("O").should eq ["HH"]
  end

  it "parses all maps for src" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    H => HO
    H => OH
    O => HH

    HOH
    EOF
    puzzle.maps("H").should eq ["HO", "OH"]
  end

  it "parses the medicine" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    H => HO
    H => OH
    O => HH

    HOH
    EOF

    puzzle.medicine.should eq "HOH"
  end

  it "generates uniq molecules" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    H => HO
    H => OH
    O => HH

    HOH
    EOF

    mols = puzzle.molecules
    mols.size.should eq 4
    mols.should contain "HOOH"
    mols.should contain "HOHO"
    mols.should contain "OHOH"
    mols.should contain "HHHH"
  end

  it "generates with multi char maps" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    HO => XX
    H => OH
    O => HH

    HOH
    EOF

    mols = puzzle.molecules
    mols.size.should eq 4
    mols.should contain "XXH"
    mols.should contain "HOOH"
    mols.should contain "OHOH"
    mols.should contain "HHHH"
  end
end
