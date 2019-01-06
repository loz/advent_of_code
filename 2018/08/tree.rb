class Tree
  attr_reader :children, :metadata

  def initialize
    @children = []
    @metadata = []
  end

  def checksum
    sum = @metadata.inject &:+
    @children.each do |child|
      sum += child.checksum
    end
    sum
  end

  def value
    if @children.empty?
      checksum
    else
      val = 0
      @metadata.each do |key|
        next if key == 0
        key = key -1
        child = @children[key]
        if child
          val += child.value
        end
      end
      val
    end
  end

  def from_key(key)
    parts = key.split.map {|n| n.to_i }
    from_parts(parts)
  end

  def from_parts(parts)
    child_count = parts.shift
    meta_count = parts.shift
    #Pull Children
    child_count.times do
      child = Tree.new
      child.from_parts(parts)
      @children << child
    end
    #Pull Meta
    meta_count.times do
      @metadata << parts.shift
    end
  end
end
