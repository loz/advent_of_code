require 'minitest/autorun'
require_relative './imune'

describe Immune do
  before do
    @system = Immune.new
  end

  describe "parse_group" do
    it "captures given stats" do
      group = @system.parse_group("17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2")
 
      group.units.must_equal 17
      group.hit_points.must_equal 5390
      group.weaknesses.must_equal [:radiation, :bludgeoning]
      group.damage.must_equal :fire
      group.damage_points.must_equal 4507
      group.initiative.must_equal 2
    end

    it "captures when multiple weaknesses and immunities" do
      group = @system.parse_group("989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3")

      group.units.must_equal 989
      group.hit_points.must_equal 1274
      group.immunity.must_equal [:fire]
      group.weaknesses.must_equal [:bludgeoning, :slashing]
      group.damage.must_equal :slashing
      group.damage_points.must_equal 25
      group.initiative.must_equal 3
    end

    it "captures when only immunities" do
      group = @system.parse_group("1057 units each with 3791 hit points (immune to cold) with an attack that does 27 bludgeoning damage at initiative 5")

      group.immunity.must_equal [:cold]
      group.weaknesses.must_equal []
    end

    it "captures when no weakness or immunity" do
      group = @system.parse_group("330 units each with 4136 hit points with an attack that does 91 cold damage at initiative 6")

      group.immunity.must_equal []
      group.weaknesses.must_equal []
    end
  end
end
