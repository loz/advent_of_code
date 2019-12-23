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
      print node.id
      spawn do
        machine.execute(node, net)
      end
    end
    while true
      Fiber.yield
      sleep 1
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
    part_one
  end
end
