require "./spec_helper"

describe Battle do
  battle = Battle.new
  map1 = <<-EOF
  #######
  #E..G.#
  #...#.#
  #.G.#G#
  #######
  EOF

  describe "#define_targets" do
    it "identifies targets for each unit" do
      battle.set_map(map1)
      battle.define_targets

      elf = battle.elves[0]
      elf.targets.size.should eq(3)
      
      elf.targets[0].pos.should eq({4,1})
      elf.targets[1].pos.should eq({2,3})
      elf.targets[2].pos.should eq({5,3})
    end
  end

  describe "#determine_range" do
    it "identifies locations in range of enemy units" do
      battle.set_map(map1)
      battle.define_targets

      elf = battle.elves[0]
      elf.determine_range(battle.map)

      elf.locations.size.should eq(6)
      elf.locations.should contain({3,1})
      elf.locations.should contain({5,1})
      elf.locations.should contain({2,2})
      elf.locations.should contain({5,2})
      elf.locations.should contain({1,3})
      elf.locations.should contain({3,3})
    end
  end

  describe "#filter_nearest" do
    it "retains locations which are closest" do
      battle.set_map(map1)
      battle.define_targets

      elf = battle.elves[0]
      elf.determine_range(battle.map)
      elf.filter_nearest(battle.map)

      elf.locations.size.should eq 3
      elf.locations.should contain({3,1})
      elf.locations.should contain({2,2})
      elf.locations.should contain({1,3})
    end
  end
end
