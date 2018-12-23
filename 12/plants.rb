class Plants
  attr_reader :pots, :centre, :rules

  def initialize(state)
    @pots = state
    @centre = 0
    @rules = []
    expand_pots
  end

  def self.from_lines(lines)
    lines = lines.each_line.to_a
    init = lines.shift
    init.chomp!
    init.gsub!("initial state: ", "")
    plants = new(init) 
    lines.each do |line|
      rule = fetch_rule(line)
      plants.rules << rule if rule
    end
    plants
  end

  def self.fetch_rule(line)
    matches = line.match(/(.*) => #/)
    matches[1] if matches
  end

  def add_rule(rule)
    @rules << rule
  end

  def score
    sum = 0
    (0..@pots.length).each do |pos|
      score = pos - @centre
      content = @pots[pos]
      sum += score if content == "#"
      #puts "%s > %s" % [score, @pots[pos]]
    end
    sum
  end

  def expand_pots
    len = @pots.length
    @pots.gsub!(/^\.*#/,'....#')
    @centre += (@pots.length - len)
    if @centre < 0
      pad =  "." * @centre.abs
      @pots = pad + @pots
      @centre = 0
    end
    @pots.gsub!(/#\.*$/,'#....')
    puts "C: #{@centre}"
  end

  def grow
    gen1 = @pots.dup

    targets = @pots.length - 4 #+/- 2 on either side
    targets.times do |pos|
      pos = pos + 2
      sequence = gen1[pos-2,5]
      if @rules.include?(sequence)
        @pots[pos] = '#' #fill the pot
      else
        @pots[pos] = '.' #empty the pot
      end
    end
    expand_pots
  end

  def dump
    puts ":> " + @pots
    puts "   " + (" " * @centre) + "^ (#{score})"
  end
  
end
