require "spec"
require "./spec_helper"

describe NetworkIO do
  it "initializes nodes with their network id" do
    net = NetworkIO.new

    node = net.node(10)
    node.shift.should eq 10

    node = net.node(35)
    node.shift.should eq 35
  end

  describe NetworkIO::Node do
    it "is idle with not input" do
      node = NetworkIO::Node.new(12)
      node.idle?.should eq false
      node.shift #ID
      node.idle?.should eq true
    end
  end

  it "returns -1 when there is no packet for a node" do
    net = NetworkIO.new
    node = net.node(30)
    node.shift #remove network id
    result = node.shift
    result.should eq -1
  end

  it "routes a packet to the correct node" do
    net = NetworkIO.new
    node_a = net.node(30)
    node_b = net.node(20)
    node_a.shift
    node_b.shift

    net << 30
    net << 10
    net << 20

    node_b.shift.should eq -1 #No Packet

    node_a.shift.should eq 10  #X
    node_a.shift.should eq 20  #Y
    node_a.shift.should eq -1  #No More Packet
  end

  it "routes 255 to the NAT" do
    net = NetworkIO.new

    net << 255
    net << 35
    net << 40

    net.nat.packet.should eq({35,40})
  end
end
