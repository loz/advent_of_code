class Puzzle
  
  property mapping = {} of String => Array(String)
  property medicine = ""

  def process(str)
    str.each_line do |line|
      process_line(line)
    end
  end

  def process_line(line)
    match = line.match /(.*) => (.*)/
    if match
      src = match[1]
      dest = match[2]
      mapping[src] ||= [] of String
      mapping[src] << dest
    else
      @medicine = line
    end
  end

  def maps(src)
    mapping[src]
  end

  def result
    #puts "Generating"
    #mols = molecules
    #puts "#{molecules.size} combinations"
    puts "Regressing"
    short = regress("e")
    p short
    p short.size
  end

  def molecules
    matches = [] of String
    mapping.each do |src, dests|
       dests.each do |dest|
        matches += replacements("", @medicine.dup, src, dest)   
       end
    end
    matches.uniq
  end

  def regress(target)
    reverse = {} of String => String
    mapping.each do |src, dests|
      dests.each { |dest| reverse[dest] = src }
    end
    paths = [] of Array(String)
    paths += gen_regress([] of String, @medicine.dup, reverse, target)
    shortest = paths.min_by { |path| path.size }
    shortest
  end

  def gen_regress(prior, current, maps, target)
    paths = [] of Array(String)
    if current == target
      puts "Solution @#{prior.size}"
      paths << prior
    else
      maps.each do |s, d|
        newchild = current.sub(s, d)
        if newchild != current
          step = prior + [current]
          paths += gen_regress(step, newchild, maps, target)
        end
      end
    end
    paths
  end

  def replacements(left, rest, src, dest)
    replaces = [] of String
    found = rest.index(src)
    if found
      before = rest[0,found] 
      after = rest[found+src.size,rest.size]
      newchain = left + before + dest + after
      #puts "#{left}:#{rest} #{src}->#{dest} (#{before}::#{after}) New: #{newchain}"
      replaces << newchain
      #Also look for further down the chain
      replaces += replacements(left + before + src, after, src, dest)
    end
    replaces
  end

end
