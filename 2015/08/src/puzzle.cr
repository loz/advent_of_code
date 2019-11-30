class Puzzle
  property string_length = 0
  property memory_length = 0

  def process(str)
    str.each_line do |line|
      @string_length += line.size
      memory = line.gsub(/(")|(\\")|(\\\\)|/,
        { "\\\"" => "\"",
          "\"" => "",
          "\\\\" => "\\"

        })
      memory = memory.gsub(/\\x../, ":")
      @memory_length += memory.size
    end
  end

  def result
    puts "Characters", string_length
    puts "Memory", memory_length
    puts "Difference", string_length - memory_length
  end

end
