require 'minitest/autorun'
require_relative './fabric'

describe Fabric do
  before do
    @fabric = Fabric.new
  end

  describe "#parse_claim" do
    it "retrieves each portion of information for a claim" do
      claim = @fabric.parse_claim("#123 @ 3,2: 5x4")
      claim[:id].must_equal 123
      claim[:x].must_equal 3
      claim[:y].must_equal 2
      claim[:width].must_equal 5
      claim[:height].must_equal 4
    end
  end

  describe "#apply_claim" do
    it "has no overlapping squares when no claims are applied" do
      @fabric.overlapping_squares.must_equal 0
    end

    it "has no overlapping squares when only one claim is applied" do
      claim = {
        :id => "123",
        :x => 0,
        :y => 0,
        :width => 5,
        :height => 5
      }
      @fabric.apply_claim(claim)
      @fabric.overlapping_squares.must_equal 0
    end

    it "has overlapping squares for a claim when applied twice" do
      claim = {
        :id => "123",
        :x => 0,
        :y => 0,
        :width => 5,
        :height => 5
      }
      @fabric.apply_claim(claim)
      @fabric.apply_claim(claim)
      @fabric.overlapping_squares.must_equal 25
    end
  end

  describe "apply_claims" do
    it "applies all claims to the fabric" do
      claims = <<-EOF
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
      EOF
      @fabric.apply_claims(claims)
      @fabric.overlapping_squares.must_equal 4
      #@fabric.dump(10,10)
    end
  end

  describe "find_claim_shares" do
    it "finds all claim ids shared for each id" do
      claims = <<-EOF
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
      EOF
      @fabric.apply_claims(claims)

      shares = @fabric.find_claim_shares
      shares[1].sort.must_equal [1,2]
      shares[2].sort.must_equal [1,2]
      shares[3].must_equal [3]
    end
  end

  describe "find_unshared_claims" do
    it "finds the claim ids which do not share at all" do
      claims = <<-EOF
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
      EOF
      @fabric.apply_claims(claims)
      unshared = @fabric.find_unshared_claims
      unshared.count.must_equal 1
      unshared.must_include 3
    end
  end
end
