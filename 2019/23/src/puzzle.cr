require "./intcode"
require "./networkio"

class Puzzle
  @instructions = ""
  
  def process(str)
    @instructions = str
  end

  def part_one
    net = NetworkIO.new
    print "Booting"
    50.times do |n|
      print "."
      node = net.node(n)
      machine = Intcode.new
      machine.process(@instructions)
      spawn do
        machine.execute(node, net)
      end
    end
    while true
      sleep 1
    end
  end

  def part_two
    net = NetworkIO.new
    print "Booting"
    50.times do |n|
      print "."
      node = net.node(n)
      machine = Intcode.new
      machine.process(@instructions)
      spawn do
        machine.execute(node, net)
      end
    end
    while true
      sleep 0.01
      net.nat.monitor(net)
    end
  end

  def debug
    net = NetworkIO.new
    node = net.node(35)
    machine = Intcode.new
    machine.process(@instructions)
    machine.execute(node, net)
  end

  def result
    part_two
  end
end
