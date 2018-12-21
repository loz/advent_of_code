class Fabric
  def parse_claim(line)
    id, at, loc, size = line.split
    x, y = loc.split(',')
    width, height = size.split('x')
    {
      :id => id,
      :x => x.to_i,
      :y => y.to_i,
      :width => width.to_i,
      :height => height.to_i,
    }
  end
end
