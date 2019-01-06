require 'minitest/autorun'
require_relative './particles'

describe Particles do
  before do
    @particles = Particles.new
    @lines = <<-EOF
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
    EOF
  end

  describe "#add_line" do
    it "adds a particle to the system" do
      @particles.add_line("position=< 9,  1> velocity=< 0,  2>")
      particle = @particles.particles[0]
      particle.x.must_equal 9
      particle.y.must_equal 1
      particle.dx.must_equal 0
      particle.dy.must_equal 2
    end
  end

  describe "#add_lines" do
    it "adds all particles in the lines" do
      @particles.add_lines(@lines)
      @particles.particles.count.must_equal 5

      particle = @particles.particles[4]
      particle.x.must_equal 2
      particle.y.must_equal -4
      particle.dx.must_equal 2
      particle.dy.must_equal 2
    end
  end

  describe "#move" do
    it "moves each particle by their vector" do
      @particles.add_lines(@lines)
      @particles.move

      particle = @particles.particles.first
      particle.x.must_equal 9
      particle.y.must_equal 3

      particle = @particles.particles.last
      particle.x.must_equal 4
      particle.y.must_equal -2

    end
  end

  describe "#bounds" do
    it "returns the outer bounds of the particle system" do
      @particles.add_lines(@lines)
      bounds = @particles.bounds
      bounds.must_equal [2,-4,9,10]
    end
  end

  describe "#scale_for" do
    it "gives x and y scale to fit a given size" do
      @particles.add_lines(@lines)
      scale = @particles.scale_for(640,480)
      scale.must_equal [640.0/7, 480.0/14]
    end
  end
end
