class NetworkIO

  class ErrorUnroutable < Exception
  end

  alias Packet = Tuple(Int64,Int64)

  class Nat
    property packet : Packet | Nil
    property seen = {} of Packet => Bool

    def monitor(net)
      net.each_node do |node|
        return unless node.idle?
      end
      packet.try do |pac|
        if @seen[pac]?
          puts "Repeating #{pac}"
          raise "Rep"
        end
        puts "Sending NAT Packet #{packet} -> Node 0"
        x, y = pac
        node0 = net.node(0)
        node0 << x
        node0 << y
        @seen[pac] = true
      end
    end
  end

  class Node
    
    @buffer = [] of Int64
    @id : Int64
    def id
      @id
    end

    def initialize(networkid)
      @id = networkid.to_i64
      @buffer = [@id]
    end

    def <<(val)
      @buffer << val
    end

    def idle?
      @buffer.empty?
    end

    def shift
      sleep 0.01
      if idle?
        #print ":#{@id}:" unless @id == 0
        -1
      else
        #print "<#{@id}>"
        @buffer.shift
      end
    end
  end

  @nodes = [] of Node
  @state = :waiting
  @target : Int64 
  @packet_x : Int64 

  property nat = Nat.new

  def initialize(numnodes = 50)
    @target = 0.to_i64
    @packet_x = 0.to_i64
    numnodes.times do |n|
      @nodes << Node.new(n)
    end
  end
  
  def each_node(&block)
    @nodes.each do |node|
      yield node
    end
  end

  def <<(val)
    case @state
      when :waiting
        @target = val.to_i64
        @state = :packet_x
      when :packet_x
        @packet_x = val.to_i64
        @state = :packet_y
      when :packet_y
        send_packet(@target, @packet_x, val.to_i64)
        @state = :waiting
    end
  end

  def send_packet(target, x, y)
    if target == 255.to_i64
      puts "NAT packet {#{x},#{y}}"
      nat.packet = {x, y}
    elsif @nodes[target]?
      puts "Sending #{target} with packet {#{x},#{y}}"
      thenode = node(target)
      thenode << x
      thenode << y
    else
      puts "Cannot Route To #{target} with packet {#{x},#{y}}"
    end
  end

  def node(number)
    @nodes[number]
  end

end

