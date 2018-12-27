require 'minitest/autorun'
require_relative './battle'

describe Battle do
  before do
    @battle = Battle.new
  end

  describe "Decision Rules" do
    before do
      @map = <<-EOF
#######
#E..G.#
#...#.#
#.G.#G#
#######
      EOF
      @battle.set_map(@map)
    end

    describe "#define_targets" do
      it "identifies targets for each unit" do
        @battle.define_targets

        elf = @battle.elves[0]
        elf.targets.length.must_equal 3
        elf.targets[0].pos.must_equal [4,1]
        elf.targets[1].pos.must_equal [2,3]
        elf.targets[2].pos.must_equal [5,3]
      end
    end

    describe "#determine_range" do
      it "identifies locations in range of enemy units" do
        @battle.define_targets

        elf = @battle.elves[0]
        elf.determine_range(@battle.map)

        elf.locations.length.must_equal 6
        elf.locations.must_include [3,1]
        elf.locations.must_include [5,1]
        elf.locations.must_include [2,2]
        elf.locations.must_include [5,2]
        elf.locations.must_include [1,3]
        elf.locations.must_include [3,3]
      end
    end

    describe "#filter_reachable" do
      it "removes locations which cannot be reached" do
        @battle.define_targets

        elf = @battle.elves[0]
        elf.determine_range(@battle.map)
        elf.filter_reachable(@battle.map)

        elf.locations.length.must_equal 4
        elf.locations.must_include [3,1]
        elf.locations.must_include [2,2]
        elf.locations.must_include [1,3]
        elf.locations.must_include [3,3]
      end
    end

    describe "#filter_nearest" do
      it "retains locations which are closest" do
        @battle.define_targets

        elf = @battle.elves[0]
        elf.determine_range(@battle.map)
        elf.filter_reachable(@battle.map)
        elf.filter_nearest(@battle.map)

        elf.locations.length.must_equal 3
        elf.locations.must_include [3,1]
        elf.locations.must_include [2,2]
        elf.locations.must_include [1,3]
        elf.distance([3,1]).must_equal 2
      end
    end

    describe "#select_target" do
      it "picks the nearest in reading order" do
        @battle.define_targets

        elf = @battle.elves[0]
        elf.determine_range(@battle.map)
        elf.filter_reachable(@battle.map)
        elf.filter_nearest(@battle.map)
        elf.select_target

        elf.target.must_equal [3,1]
      end
    end

    describe "#turn" do
      it "moves each unit in turn order" do
        map = <<-EOF
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########
        EOF
        @battle.set_map(map)
        @battle.define_targets
        @battle.turn

        @battle.map_string.must_equal <<-EOF
#########
#.G...G.#
#...G...#
#...E..G#
#.G.....#
#.......#
#G..G..G#
#.......#
#########
        EOF
      end

      it "removes each defeated unit" do
        map= <<-EOF
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
        EOF
        @battle.set_map(map)
        @battle.define_targets

        22.times { @battle.turn }
        puts @battle.map_string

        @battle.map_string.must_equal <<-EOF
#######
#...G.#
#..GEG#
#.#.#G#
#...#E#
#.....#
#######
        EOF
        @battle.turn

        puts @battle.map_string
        @battle.map_string.must_equal <<-EOF
#######
#...G.#
#..G.G#
#.#.#G#
#...#E#
#.....#
#######
        EOF

      end
    end

    describe "#move_step" do
      it "selects first step from shortests in reading order" do
        map = <<-EOF
#######
#.....#
#....G#
#.E...#
#######
        EOF
        @battle.set_map(map)
        @battle.define_targets

        elf = @battle.elves[0]
        elf.determine_range(@battle.map)
        elf.filter_reachable(@battle.map)
        elf.filter_nearest(@battle.map)
        elf.select_target

        elf.target.must_equal [4,2]

        dest = elf.move_step
        dest.must_equal [2,2]
      end
    end
  end

end
