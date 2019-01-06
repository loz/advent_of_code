require_relative './program'

program = Program.new
code_file = File.open("input")
code = code_file.read
program.load(code)
program.machine.set_register(0, 1)

#Simulate after doing huge loop
program.machine.set_register(1, 5_275_644)
program.machine.set_register(2, 3 - 1)
program.machine.set_register(3, 10551288)
program.machine.set_register(4, 2)
program.machine.set_register(5, 1)
program.ip = 3 #PRE-JMP

#It sums the divisors of the target number!
target = 888
target = 10551288
sum = 0
(1..target).each do |n|
  if target % n == 0
    m = target / n
    sum += n
    puts "#{n} x #{m}"
  end
end
puts "Total #{sum}"

exit 1

#while !program.halted?
#  #program.execute(true)
#  program.execute()
#  if program.ip == 12
#    puts program.machine.registers.inspect
#  end
#end
#puts "HALTED!"

100.times { program.execute(true) }
p program.machine.registers
