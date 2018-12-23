require 'minitest/autorun'
require_relative './plants'

describe Plants do
  describe "#grow" do
    describe "when rule matches for a given pot" do
      it "has a plant the next time" do
        plants = Plants.new(".....")
        plants.add_rule(".....")

        plants.grow

        pots = plants.pots
        pots.must_equal "....#...."
      end

      it "grows to the right of the pots" do
        plants = Plants.new("..#..")
        plants.add_rule("..#..")
        plants.add_rule(".#...")

        plants.grow

        pots = plants.pots
        pots.must_equal "....##...."

        plants.centre.must_equal 2
      end

      it "grows to the left of the pots" do
        plants = Plants.new("..#..")
        plants.add_rule("..#..")
        plants.add_rule("....#")

        plants.grow

        pots = plants.pots
        pots.must_equal "....#.#...."
        plants.centre.must_equal 4
      end
    end

    describe "when no rule matches for a given pot" do
      it "has no plant next time" do
        plants = Plants.new("..#..")

        plants.grow

        pots = plants.pots
        pots.must_equal "........."
      end
    end

    describe ".from_lines" do
      before do
        @lines = <<-EOF
initial state: #..#.#..##......###...###

..... => .
#.... => .
..### => .
##..# => #
.###. => #
        EOF
      end

      it "sets initial state" do
        plants = Plants.from_lines(@lines)
        plants.pots.must_equal "....#..#.#..##......###...###...."
      end

      it "adds rules for new plants only" do
        plants = Plants.from_lines(@lines)
        plants.rules.count.must_equal 2
      end
    end
  end

  describe "#score" do
    it "scores plant before and after center" do
        plants = Plants.new("..#....#")
        plants.add_rule("....#")

        plants.grow
        plants.grow
        
        plants.score.must_equal 1
    end
  end

end
