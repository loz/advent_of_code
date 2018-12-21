require 'minitest/autorun'
require_relative './checksum'

describe Checksum do
  before do
    @checksum = Checksum.new
  end

  describe "#compare" do
    it "returns 0 for identical strings" do
      result = @checksum.compare("abcdef", "abcdef")
      result.must_equal 0
    end

    it "returns 1 for 1 different letter" do
      result = @checksum.compare("abcdef", "abccef")
      result.must_equal 1
    end

    it "returns 2 for 2 different letters" do
      result = @checksum.compare("abcdef", "abccea")
      result.must_equal 2
    end
  end

  describe "#search" do
    it "returns barcodes which differ only by 1" do
      lines = <<-EOF
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
      EOF
      result = @checksum.search(lines)
      result.must_include "fghij"
      result.must_include "fguij"
      result.count.must_equal 2
    end
  end

  describe "#sum" do
    it "multiplies the sum of two and three counts" do
      lines = <<-EOF
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
      EOF
      sum = @checksum.sum(lines)
      sum.must_equal 12
    end
  end

  describe "#sum_counter" do
    it "sums up the checksums for given lines" do
      lines = <<-EOF
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
      EOF
      two, three = @checksum.sum_counter(lines)
      two.must_equal 4
      three.must_equal 3
    end
  end
  describe "#counter" do
    it "gives 0, 0 for no repeated letters" do
      two, three = @checksum.counter("abcdef")
      two.must_equal 0
      three.must_equal 0
    end

    it "gives 1, 0 for letters repeated exactly twice" do
      two, three = @checksum.counter("abbcde")
      two.must_equal 1
      three.must_equal 0
    end

    it "gives 0, 1 for letters repeated exactly thrice" do
      two, three = @checksum.counter("abcccd")
      two.must_equal 0
      three.must_equal 1
    end

    it "gives 1, 1 for repeat of 2 letters and a repeat of 3 letters" do
      two, three = @checksum.counter("bababc")
      two.must_equal 1
      three.must_equal 1
    end

    it "counts 1 for repeat of 2 letters even if there are two or more" do
      two, three = @checksum.counter("aabcdd")
      two.must_equal 1
      three.must_equal 0
    end

    it "counts 1 for repeat of 3 letters even if there are two or more" do
      two, three = @checksum.counter("ababab")
      two.must_equal 0
      three.must_equal 1
    end
  end
end
