class Puzzle

  @scores = {} of Tuple(String, String) => Int32
  property people = [] of String

  def process(str)
    str.each_line do |line|
      process_line(line)
    end
  end

  def insert_me
    @people.each do |person|
      @scores[{person, "Me"}] = 0
      @scores[{"Me", person}] = 0
    end
    @people << "Me"
  end

  def happiness(forperson, nextto)
    @scores[{forperson,nextto}]
  end

  def change(seating)
    left = seating.last
    rotate = seating + [seating.first]
    total = 0
    while rotate.size > 1
      person = rotate.shift
      right = rotate.first
      total += happiness(person, left)
      total += happiness(person, right)
      left = person
    end
    total
  end

  def process_line(line)
    match = line.match /(.*) would (gain|lose) (\d+) happiness units by sitting next to (.*)\./
    if match
      person = match[1]
      direction = match[2]
      units = match[3].to_i
      nextto = match[4]
      if direction == "lose"
        units = 0-units
      end
      @scores[{person,nextto}] = units
      @people << person
      @people << nextto
    else
      puts "Failed To Parse! #{line}"
    end
    @people.uniq!
  end

  def result
    insert_me
    max = [] of String
    max_h = 0
    people.permutations.each do |seating|
      p_change = change(seating)
      if p_change > max_h
        max = seating
        max_h = p_change
      end
      puts "#{seating.inspect} -> #{p_change}"
    end
    puts "----"
    puts "Max", max, max_h
  end

end
