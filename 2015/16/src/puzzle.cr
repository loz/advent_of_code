class Puzzle
  property matchers = {
    "children" => 3,
    "cats" => 7,
    "samoyeds" => 2,
    "pomeranians" => 3,
    "akitas" => 0,
    "vizslas" => 0,
    "goldfish" => 5,
    "trees" => 3,
    "cars" => 2,
    "perfumes" => 1
  }

  def process(str)  
    str.each_line do |line|
      p match(line)
    end
  end

  def match(line)
    name, rest = line.split(":", 2)
    parts = rest.split(",")
    matches = true
    parts.each do |part|
     item, count = part.split(": ")
     item = item.lstrip.strip
     count = count.lstrip.strip.to_i
     if item == "cats" || item == "trees"
       return {false,name} if matchers[item] >= count
     elsif item == "pomeranians" || item == "goldfish"
       return {false,name} if matchers[item] <= count
     else
       return {false,name} if matchers[item] != count
     end
    end
    {matches, name}
  end

  def result
  end

end
