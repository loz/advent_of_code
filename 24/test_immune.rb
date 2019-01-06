require 'minitest/autorun'
require_relative './immune'

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

  describe "ordering" do
    before do
      @system = Immune.new

      group = Immune::Group.new
      group.initiative = 8
      group.units = 10
      group.damage_points = 10
      @system.good << group

      group = Immune::Group.new
      group.initiative = 2
      group.units = 10
      group.damage_points = 12
      @system.good << group

      group = Immune::Group.new
      group.initiative = 7
      group.units = 12
      group.damage_points = 12
      @system.bad << group

      group = Immune::Group.new
      group.initiative = 3
      group.units = 10
      group.damage_points = 12
      @system.bad << group
    end

    it "return groups in initiative order" do
      last = 999
      @system.groups.count.must_equal 4
      @system.groups.each do |g|
        (g.initiative < last).must_equal true
        last = g.initiative
      end
    end

    it "returns target_ordered in descresing order of effective power" do
      groups = @system.target_ordered

      groups[0].initiative.must_equal 7
      groups[1].initiative.must_equal 2
      groups[2].initiative.must_equal 3
      groups[3].initiative.must_equal 8
    end

    it "attack_ordered in descending order of initiative" do
      groups = @system.attack_ordered

      groups[0].initiative.must_equal 8
      groups[1].initiative.must_equal 7
      groups[2].initiative.must_equal 3
      groups[3].initiative.must_equal 2
    end

  end

  describe "attacking" do
    it "The attacking group chooses to target the group in the enemy army to which it would deal the most damage" do
      group =Immune::Group.new
      group.weaknesses = []
      group.immunity = []
      group.damage = :stuff
      group.damage_points = 100
      group.units = 10

      @system.good << group

      group =Immune::Group.new
      group.weaknesses = []
      group.immunity = [:stuff]
      group.damage = :bar
      group.damage_points = 100
      group.units = 10
      @system.bad << group

      group =Immune::Group.new
      group.weaknesses = [:stuff]
      group.immunity = []
      group.damage = :bar
      group.damage_points = 100
      group.units = 10
      @system.bad << group

      @system.establish_targets

      @system.good.first.target.must_equal @system.bad[1]

    end
    
    it "will prioritise a weakness to its damage as this deals double damage" do
      group =Immune::Group.new
      group.weaknesses = []
      group.immunity = []
      group.damage = :stuff
      group.damage_points = 100
      group.units = 10

      @system.good << group

      group =Immune::Group.new
      group.weaknesses = []
      group.immunity = []
      group.damage = :bar
      group.damage_points = 100
      group.units = 10
      @system.bad << group

      group =Immune::Group.new
      group.weaknesses = [:stuff]
      group.immunity = []
      group.damage = :bar
      group.damage_points = 100
      group.units = 10
      @system.bad << group

      @system.establish_targets

      @system.good.first.target.must_equal @system.bad[1]
    end

    describe "when two groups with equal damage" do
      it "chooses to target the defending group with the largest effective power" do
        group =Immune::Group.new
        group.weaknesses = []
        group.immunity = []
        group.damage = :stuff
        group.damage_points = 100
        group.units = 10

        @system.good << group

        group =Immune::Group.new
        group.weaknesses = []
        group.immunity = []
        group.damage = :bar
        group.damage_points = 100
        group.units = 10
        @system.bad << group

        group =Immune::Group.new
        group.weaknesses = []
        group.immunity = []
        group.damage = :bar
        group.damage_points = 100
        group.units = 20
        @system.bad << group

        @system.establish_targets

        @system.good.first.target.must_equal @system.bad[1]
      end

        describe "when there is still a tie" do
          it "chooses the defending group with the highest initiative" do
            group =Immune::Group.new
            group.weaknesses = []
            group.immunity = []
            group.damage = :stuff
            group.damage_points = 100
            group.units = 10
            group.initiative = 1

            @system.good << group

            group =Immune::Group.new
            group.weaknesses = []
            group.immunity = []
            group.damage = :bar
            group.damage_points = 100
            group.units = 10
            group.initiative = 2
            @system.bad << group

            group =Immune::Group.new
            group.weaknesses = []
            group.immunity = []
            group.damage = :bar
            group.damage_points = 100
            group.units = 10
            group.initiative = 3
            @system.bad << group

            @system.establish_targets

            @system.good.first.target.must_equal @system.bad[1]
          end
        end
    end
    describe "when it cannot deal any damage" do
      it "does not choose a target" do
        group =Immune::Group.new
        group.weaknesses = []
        group.immunity = []
        group.damage = :stuff
        group.damage_points = 100
        group.units = 10
        group.initiative = 1

        @system.good << group

        group =Immune::Group.new
        group.weaknesses = []
        group.immunity = [:stuff]
        group.damage = :bar
        group.damage_points = 100
        group.units = 10
        group.initiative = 2
        @system.bad << group

        group =Immune::Group.new
        group.weaknesses = []
        group.immunity = [:stuff]
        group.damage = :bar
        group.damage_points = 100
        group.units = 10
        group.initiative = 3
        @system.bad << group

        @system.establish_targets

        @system.good.first.target.must_equal nil
      end
    end
  end

  describe "dealing damage" do
    it "applies damage across full unit hitpoints" do
        agressor =Immune::Group.new
        agressor.weaknesses = []
        agressor.immunity = []
        agressor.damage = :stuff
        agressor.damage_points = 75
        agressor.units = 1
        agressor.initiative = 1

        defender =Immune::Group.new
        defender.weaknesses = []
        defender.immunity = []
        defender.hit_points = 10
        defender.units = 10
        defender.initiative = 3

        agressor.target = defender

        agressor.fight!

        defender.units.must_equal 3
    end

    it "removes all units when damage >= unit defence" do
        agressor =Immune::Group.new
        agressor.weaknesses = []
        agressor.immunity = []
        agressor.damage = :stuff
        agressor.damage_points = 75
        agressor.units = 1
        agressor.initiative = 1

        defender =Immune::Group.new
        defender.weaknesses = []
        defender.immunity = []
        defender.hit_points = 10
        defender.units = 5
        defender.initiative = 3

        agressor.target = defender

        agressor.fight!

        defender.units.must_equal 0
    end
  end

  describe "group" do
    before do
      @group = Immune::Group.new
    end

    it "has an effective power" do
      @group.units = 123
      @group.damage_points = 12

      @group.effective_power.must_equal (123*12)
    end
  end

  describe "fight!" do
    before do
      @system = Immune.new
      @system.good << @system.parse_group("17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2")
      @system.good << @system.parse_group("989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3")

      @system.bad << @system.parse_group("801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1")
      @system.bad << @system.parse_group("4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4")
      
      @system.fight!
    end

    it "deals damage for each unit against the target" do
      @system.good.last.units.must_equal 905
      @system.bad.first.units.must_equal 797
      @system.bad.last.units.must_equal 4434
    end

    it "removes depleated units" do
      @system.good.count.must_equal 1
    end
  end

end
