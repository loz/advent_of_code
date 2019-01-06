require_relative '../19/program'

program = Program.new
code_file = File.open("input")
code = code_file.read
program.load(code)
#program.machine.set_register(0, 1)

#Machine Loops Until [5] * 256 GT 65536
ip = 19
program.machine.set_register(1,10908048)
program.machine.set_register(2,ip -1)
program.machine.set_register(3,65536)
program.machine.set_register(4,256)
program.machine.set_register(5,257)
program.ip = ip

=begin
program.machine.set_register(1,2236409)
program.machine.set_register(2,ip -1)
program.machine.set_register(3,11350651)
program.machine.set_register(4,44338)
program.machine.set_register(5,44339)

#9346297, 17, 44338,

program.machine.set_register(1,9346297)
program.machine.set_register(2,ip -1)
program.machine.set_register(3,44338)
program.machine.set_register(4,173)
program.machine.set_register(5,174)

#ip=19 [0, 588934, 19, 14649954, 3, 4] muli 5 256 5 [0, 588934, 19, 14649954, 3, 1024]
program.machine.set_register(1,588934)
program.machine.set_register(2,ip -1)
program.machine.set_register(3,14649954)
program.machine.set_register(4,57226)
program.machine.set_register(5,57227)


program.machine.set_register(0, 14236869)
20.times { program.execute(true) }
puts "Skipping..."
program.ip = ip
n = program.machine.registers[1]
target = program.machine.registers[3]
m = target / 256
program.machine.set_register(1,n)
program.machine.set_register(2,ip -1)
program.machine.set_register(3,target)
program.machine.set_register(4,m)
program.machine.set_register(5,m+1)
=end

#program.machine.set_register(0, 11285115)
exits = []
100_100_000.times do 
  program.execute
  if program.ip == 18
    #puts "Skipping Loop: " + program.machine.registers.inspect
    #print "S"
    n = program.machine.registers[1]
    target = program.machine.registers[3]
    m = target / 256
    program.machine.set_register(1,n)
    program.machine.set_register(2,ip -1)
    program.machine.set_register(3,target)
    program.machine.set_register(4,m)
    program.machine.set_register(5,m+1)
    program.ip = ip
  elsif program.ip == 28
    possible = program.machine.registers[1]
    if exits.include? possible
      puts "Repetition: %s" % possible
      puts "Last: %s" % exits.last
      puts "Largest: %s" % exits.max
      puts "Smallest: %s" % exits.min
      exit
    end
    exits << possible
    #puts "Possible Exit Reached: [0]==%s" % 
    #print "."
  end
end
p program.machine.registers


#Have to get it to execut at 30, with [0] == [1]
#This then skips to 33 which HALTS
