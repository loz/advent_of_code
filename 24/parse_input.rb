require_relative './immune'

#bot_text = File.open("input.example") do |f|
group_text = File.open("input") do |f|
  f.read
end
system = Immune.new 
@good = []
@bad = []

group_text.each_line do |line|
  case line
  when "Immune System:\n"
    puts "Parsing Immune"
    @current = @good
  when "Infection:\n"
    puts "Parsing Infection"
    @current = @bad
  when "\n"
  else
    @current << system.parse_group(line)
  end
end

puts "Good Groups:"
@good.each do |group|
  p group
end
puts "Bad Groups:"
@bad.each do |group|
  p group
end

