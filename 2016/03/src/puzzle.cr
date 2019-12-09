class Puzzle
  @triangles = [] of Tuple(Int32, Int32, Int32)

  def process(str)
    str.each_line do |line|
      @triangles << parse_line(line)
    end
  end

  def valid?(triangle)
    a, b, c = triangle
    (a+b) > c && (b + c) > a && (a+c) > b
  end

  def reslice
    new_triangles = [] of Tuple(Int32, Int32, Int32)
    (0..@triangles.size-2).step(3) do |n|
      one = @triangles[n]
      two = @triangles[n+1]
      three = @triangles[n+2]
      a1, a2, a3 = one
      b1, b2, b3 = two
      c1, c2, c3 = three
      new_triangles << {a1, b1, c1}
      new_triangles << {a2, b2, c2}
      new_triangles << {a3, b3, c3}
    end
    @triangles  = new_triangles
  end

  def parse_line(line)
    l = line.strip.lstrip
    a, b, c = l.split(/\s+/).map {|x| x.to_i }
    {a,b,c}
  end

  def result
    reslice

    total = 0
    @triangles.each do |t|
      if valid?(t)
        total += 1
        p t
      end
    end
    puts total
  end

end
