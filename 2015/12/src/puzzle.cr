require "json"

class Puzzle
  property sum = 0

  def process(str)
    json = JSON.parse(str)
    parse_json(json)
  end

  def result
    puts "Processed: #{sum}"
  end

  def parse_json(j)
    if j.as_h?
      items = j.as_h
      reds = items.any? {|k,v| v == "red" }
      if !reds
        items.each do |key, val|
          parse_json(val)
        end
      end
    elsif j.as_a?
      items = j.as_a
      items.each {|item| parse_json(item)}
    elsif j.as_i?
      @sum += j.as_i
    else
      puts "Other"
    end
  end
end
