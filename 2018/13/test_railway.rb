require 'minitest/autorun'
require_relative './railway'

describe Railway do
  describe "#tick" do
    before do
      @track = <<-EOF
/-->--\\
|     |
^     v
|     |
\\--<--/
      EOF
      @railway = Railway.new
      @railway.load(@track)
    end

    it "moves trains around the track by 1 move" do
      @railway.tick
      @railway.track_string.must_equal <<-EOF
/--->-\\
^     |
|     |
|     v
\\-<---/
      EOF
    end

    it "moves trains around corners" do
      4.times { @railway.tick }
      @railway.track_string.must_equal <<-EOF
/->---\\
|     v
|     |
^     |
\\---<-/
      EOF
    end

    it "detects crashes" do
      track = <<-EOF
/->-\\        
|   |  /----\\
| /-+--+-\\  |
| | |  | v  |
\\-+-/  \\-+--/
  \\------/  
      EOF
      @railway = Railway.new
      @railway.load(track)
      
      13.times { @railway.tick }
      @railway.wont_be :crashed?

      @railway.tick
      @railway.must_be :crashed?

      @railway.crash_location.must_equal [7,3]
    end

    it "moves trains in order of top right to bottom left" do
      track = <<-EOF
  |      |
/-+----\\ |
| |    ^ |
\\<+----/ |
      EOF
      @railway = Railway.new
      @railway.load(track)
      
      6.times { @railway.tick }
      @railway.wont_be :crashed?
    end

    describe "#clear_crashes" do
      it "removes crashed train carts from the railway" do
        track =<<-EOF
/>-<\\  
|   |  
| /<+-\\
| | | v
\\>+</ |
  |   ^
  \\<->/
        EOF

        @railway = Railway.new
        @railway.load(track)
      
        
        @railway.dump_trains
        @railway.dump

        @railway.tick

        @railway.dump_trains
        @railway.dump

        @railway.must_be :crashed?
        @railway.trains.count.must_equal 3
        @railway.track_string.must_equal <<-EOF
/---\\  
|   |  
| v-+-\\
| | | |
\\-+-/ |
  |   |
  ^---^
        EOF
      end
    end

    it "does not crash into walls" do
      track = <<-EOF
v
|
+-+\\|  #BUG
  +++
      EOF
      railway = Railway.new
      railway.load(track)
      6.times { railway.tick }
      railway.track_string.must_equal <<-EOF
|
|
+-+\\|  #BUG
  +<+
      EOF
    end

    describe "intersections" do
      before do
        @track = <<-EOF
/-\\
| |
\\>+-\\
  | |
  \\-/
      EOF
        @railway = Railway.new
        @railway.load(@track)
      end
      
      it "turns LEFT at inersection" do
        @railway.tick
        @railway.tick
        @railway.track_string.must_equal <<-EOF
/-\\
| ^
\\-+-\\
  | |
  \\-/
        EOF
      end

      it "cycles throuth L-S-R through multiple intersections" do
        9.times { @railway.tick }
        @railway.track_string.must_equal <<-EOF
/-\\
| |
\\->-\\
  | |
  \\-/
        EOF
        8.times { @railway.tick }
        @railway.track_string.must_equal <<-EOF
/-\\
| |
\\->-\\
  | |
  \\-/
        EOF
        8.times { @railway.tick }
        @railway.track_string.must_equal <<-EOF
/-\\
| |
\\-<-\\
  | |
  \\-/
        EOF

        80.times { @railway.tick}
      end
    end
  end
end


