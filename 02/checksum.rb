class Checksum

  def search(lines)
    matches = []
    lines = lines.split
    while !lines.empty? do
      code = lines.shift
      puts "Searching Matches For (%s)" % code
      lines.each do |line|
        if compare(code, line) == 1
          puts "Matched:", line
          matches << code
          matches << line
        end
      end
    end
    matches
  end

  def compare(first, second)
    differences = 0
    pairs = first.chars.zip(second.chars)
    pairs.each do |a, b|
      differences +=1 if a != b
    end
    differences
  end

  def sum(lines)
    twos, threes = sum_counter(lines)
    twos * threes
  end

  def sum_counter(lines)
    twos = 0
    threes = 0
    lines.each_line do |line|
      two, three = counter(line)
      twos += two
      threes += three
    end
    [twos, threes]
  end

  def counter(barcode)
    counts = {
      true => 1,
      false => 0
    }
    two = false
    three = false

    frequencies = Hash.new(0)
    barcode.each_char do |c|
      frequencies[c]+= 1
    end
    frequencies.each do |_,count|
      two = true if count == 2
      three = true if count == 3
    end
    #p frequencies
    [counts[two], counts[three]]
  end
end
