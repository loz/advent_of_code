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

    target = @medicine.dup
    puts "Generating #{@medicine}"
    options = ["e"]
    10000.times do |step|
      new_options = [] of String
      puts "Processing #{options.size} options"
      options.each do |opt|
        @medicine = opt
        new_mols = molecules
        new_mols.each do |mol|
          if mol == target
            puts "Found", step
            return
          end
        end
        new_options += new_mols
      end
      options = new_options
    end
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
