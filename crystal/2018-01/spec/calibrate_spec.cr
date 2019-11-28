require "spec"
require "./spec_helper"

describe Calibrate do

  it "increases frequency with positive lines" do
    device = Calibrate::Device.new
    string = <<-EOF
    +12
    +1
    EOF
    device.calibrate(string)
    device.frequency.should eq 13
  end

  it "decreases frequency with negative lines" do
    device = Calibrate::Device.new
    string = <<-EOF
    +10
    -4
    EOF
    device.calibrate(string)
    device.frequency.should eq 6
  end

  it "locks frequency when repeated" do
    device = Calibrate::Device.new
    string = <<-EOF
    +3
    -4
    +5
    -6
    +3
    +3
    -10
    -8
    +12
    EOF
    device.calibrate(string)
    device.frequency.should eq 4
  end

  it "repeats input when lock required to find a lock" do
    device = Calibrate::Device.new
    string = <<-EOF
    +3
    -4
    +5
    EOF
    device.calibrate(string, true)
    device.frequency.should eq 3
  end
end
