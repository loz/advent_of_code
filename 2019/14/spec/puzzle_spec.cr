require "spec"
require "./spec_helper"

describe Puzzle do

  it "can determine or when produces raw fuel" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    5 ORE => 1 FUEL
    EOF

    ingredients, _ = puzzle.refine(1)

    ingredients.should eq({"ORE" => 5})
  end

  it "can refine from multiple ingredients" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    1 ORE => 1 B
    1 ORE => 1 A
    1 A, 1 B => 1 FUEL
    EOF

    ingredients, _ = puzzle.refine(1)

    ingredients.should eq({"ORE" => 2})
  end

  it "can refine excess" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    10 ORE => 10 A
    7 A => 1 FUEL
    EOF

    ingredients, _ = puzzle.refine(1)

    ingredients.should eq({"ORE" => 10})
  end

  it "determines the most efficient refinement" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
    17 NVRVD, 3 JNWZP => 8 VPVL
    53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
    22 VJHF, 37 MNCFX => 5 FWMGM
    139 ORE => 4 NVRVD
    144 ORE => 7 JNWZP
    5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
    5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
    145 ORE => 6 MNCFX
    1 NVRVD => 8 CXFTF
    1 VJHF, 6 MNCFX => 4 RFSQX
    176 ORE => 6 VJHF
    EOF

    ingredients, waste = puzzle.refine(1)
    cost = ingredients["ORE"]
    waste, _ = puzzle.savings(waste)
    (cost - waste).should eq 180697
  end

  it "calculats the saveings from waste" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    157 ORE => 5 NZVS
    165 ORE => 6 DCFZ
    44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
    12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
    179 ORE => 7 PSHF
    177 ORE => 5 HKGWZ
    7 DCFZ, 7 PSHF => 2 XJWVT
    165 ORE => 2 GPVTF
    3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
    EOF

    savings, _ = puzzle.savings({"DCFZ" => 5, "KHKGT" => 3, "QDVJ" => 8, "NZVS" => 4, "GPVTF" => 2, "HKGWZ" => 5, "PSHF" => 3})
    savings.should eq (165 + 177)
  end

  it "refines first example, with waste calculated" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL
    EOF

    ingredients, waste = puzzle.refine(1)

    ingredients.should eq({"ORE" => 31})
    waste.should eq({"A" => 2})
  end

  it "refines second example" do
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

    ingredients, _ = puzzle.refine(1)

    ingredients.should eq({"ORE" => 165})
  end

  it "can calculate the max fuel for 13312/fuel" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    157 ORE => 5 NZVS
    165 ORE => 6 DCFZ
    44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
    12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
    179 ORE => 7 PSHF
    177 ORE => 5 HKGWZ
    7 DCFZ, 7 PSHF => 2 XJWVT
    165 ORE => 2 GPVTF
    3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
    EOF

    max, _ = puzzle.max_for(1_000_000_000_000)
    max.should eq 82892753
  end


end
