require_relative './computer'

computer = Computer.new
sample_file = File.open("input.sample")
samples = sample_file.read
samples = samples.split("\n\n")
known_opcodes = {}
while !samples.empty? do
  sample = samples.shift
  #"Before: [0, 0, 2, 2]\n9 2 3 0\nAfter:  [4, 0, 2, 2]"
  matches = sample.match /Before: \[(.*)\]\n(.*)\nAfter:  \[(.*)\]/
  before = matches[1]
  instructions = matches[2]
  after = matches[3]
  if computer.identify_opcodes(before, instructions, after, known_opcodes)
    puts "#{before} > #{instructions} > #{after} FOUND: #{known_opcodes}"
  end
end

computer.set_opcodes(known_opcodes)
computer.set_register(0,0)
computer.set_register(1,0)
computer.set_register(2,0)
computer.set_register(3,0)

code_file = File.open("input.program")
code = code_file.read

code.each_line do |line|
  line.chomp!
  print "#{computer.registers} + #{line} => "
  computer.execute(line)
  puts "#{computer.registers}"
end

