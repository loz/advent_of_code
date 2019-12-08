class Puzzle
  property presents = [] of Int32

  def process(str)
    str.lines.each do |line|
      @presents << line.to_i
    end
  end

  def permutations
    max_weight = presents.sum /  3
    best = presents.size

    puts "Max Group Weight: #{max_weight}"
    options, best = gen_options([] of Int32, [] of Int32, [] of Int32, presents.dup, max_weight, best)
    options
  end

  def gen_bags
    max_weight = presents.sum /  4
    best_q = 9999999999999
    gen_sub(presents.reverse, [] of Int32, max_weight, presents.size, best_q)
  end

  def gen_sub(available, used, max_weight, best, best_q)
    return {best, best_q} if available.empty?
    used_weight = used.sum
    cur_size = used.size
    if used_weight == max_weight
      if cur_size <= best
        best = used.size
        q = qe(used)
        if best_q > q
          best_q = q
          puts "Found: #{used} -> #{q}"
        end
      end
      return {best, best_q}
    elsif cur_size > best
      return {best, best_q} #No Good
    else
      available.each do |present|
        if used_weight + present <= max_weight
          b, q = gen_sub(available - [present], used + [present], max_weight, best, best_q)
          best = b if b < best
          best_q = q if q < best_q
          return {best, best_q} if best <= cur_size
        end
      end
    end
    return {best, best_q}
  end

  def gen_options(group1, group2, group3, packages, max_weight, best)
    options = [] of Tuple(Array(Int32),Array(Int32),Array(Int32))

    #Cull too large a weight
    if group1.sum > max_weight || group2.sum > max_weight || group3.sum > max_weight
      #print 'W'
      return {options, best}
    end

    #Cull where all groups larger than/equal to  best small
    if group1.size >= best && group2.size >= best && group3.size >= best
      #print 'C'
      return {options, best}
    end

    if packages.empty?
      #We found A permutation
      unless group1.empty? || group2.empty? || group3.empty?
        perm = {group1, group2, group3}
        #puts "Found #{perm}"

        (best = group1.size) && print "B(#{best})" if group1.size < best
        (best = group2.size) && print "B(#{best})" if group2.size < best
        (best = group3.size) && print "B(#{best})" if group3.size < best

        options << {group1, group2, group3}
      end
    else
      package = packages.shift
      o, b = gen_options(group1 + [package], group2, group3, packages.dup, max_weight, best)
      (best = b) && print "B(#{best})" if b < best
      options += o

      o, b = gen_options(group1, group2 + [package], group3, packages.dup, max_weight, best)
      (best = b) && print "B(#{best})" if b < best
      options += o

      o, b = gen_options(group1, group2, group3 + [package], packages.dup, max_weight, best)
      (best = b) && print "B(#{best})" if b < best
      options += o
    end
    {options, best}
  end

  def valid?(configuration)
    group1, group2, group3 = configuration
    group1.sum == group2.sum == group3.sum
  end

  def passenger(configuration)
    group1, group2, group3 = configuration
    if group1.size < group2.size
      return group1 if group1.size < group3.size
      return group3
    else
      return group2 if group2.size < group3.size
      return group3
    end
  end

  def qe(group)
    value : UInt64
    value = 1
    group.each do |val|
      value = val.to_u64 * value
    end
    value
  rescue
    99999
  end

  def result
    gen_bags
  end

end
