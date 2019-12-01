class Puzzle
  property sum = 0

  def process(str)
    total = 0

    str.each_line do |line|
      a_module = line.to_i
      total = total + fuel(a_module)
    end
    @sum = total
  end

  def fuel(mass) : Int32
    base = (mass/3).to_i
    f = base-2
    if f < 0
      0
    else
      f + fuel(f)
    end
  end

  def result
    puts "Total Fuel: #{@sum}"
  end

end
