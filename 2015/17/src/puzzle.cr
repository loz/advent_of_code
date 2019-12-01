class Puzzle

  property jars = [] of Int32

  def process(str)
    str.each_line do |line|
      @jars << line.to_i
    end
  end

  def result
    results = options(150)
    puts "Total: #{results.size}"
    least = results.min_by {|a| a.size }.size
    puts "Minimum: #{least}"
    mincount = 0
    results.each do |result|
      if result.size == least
        puts "-> #{result.inspect}"
        mincount +=1
      end
    end
    puts "Covers: #{mincount}"
  end

  def options(total)
    list = [] of Array(Int32)
    rest = @jars.dup
    prev = [] of Int32
    list = gen_options(list, prev, rest, total)
    list
  end

  def gen_options(list, prev, jar_options, target)
    return list if jar_options.empty?
    options = jar_options.dup
    current = options.shift
    #Generate Without Self
    list = gen_options(list, prev, options, target)
    #Try Generate With
    if current < target
      gen_options(list, prev + [current], options, target - current)
    elsif current == target
      #Complete
      puts "Found: #{prev + [current]}"
      list << prev + [current]
      list
    else
      list
    end
  end
end
