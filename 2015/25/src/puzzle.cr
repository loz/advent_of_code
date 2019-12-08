class Puzzle

  def process(str)
  end

  def n(col, row)
    ((((row+col-1)*(row+col))/2)-(row-1)).to_i
  end

  def nth(n)
    code = 20151125.to_u64
    m = n-1
    m.times do
      code = code * 252533.to_u64
      code = code % 33554393.to_u64
    end
    code
  end

  def result
    row = 2978
    col = 3083
    qn = n(col, row)

    puts "#{qn}"
    puts "#{nth(qn)}"

  end

end
