require 'minitest/autorun'
require_relative './tree'

describe Tree do
  before do
    @tree = Tree.new
    @key = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
  end

  describe "#from_key" do
    it "builds the nodes from the key" do
      @tree.from_key(@key)

      @tree.children.count.must_equal 2
      child = @tree.children[1]

      child.children.count.must_equal 1
    end

    it "includes metadata for the node" do
      @tree.from_key(@key)
      @tree.metadata.must_equal [1, 1, 2]
    end
  end

  describe "#checksum" do
    it "sums all metadata through the tree" do
      @tree.from_key(@key)

      @tree.checksum.must_equal 138
    end
  end

  describe "#value" do
    it "is the metadata sum for childless node" do
      @tree.from_key(@key)
      d = @tree.children[1].children[0]

      d.value.must_equal 99
    end

    it "is 0 when metadata references a child that doesn't exist" do
      @tree.from_key(@key)
      c = @tree.children[1]

      c.value.must_equal 0
    end

    it "is sum of children which do exist" do
      @tree.from_key(@key)

      @tree.value.must_equal 66
    end
  end
end
