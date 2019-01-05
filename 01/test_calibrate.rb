require 'minitest/autorun'
require_relative './device'

describe Device do
  before do
    @device = Device.new
  end

  it "increases frequency with positive lines" do
    string = <<-EOF
+12
+1
    EOF
    @device.calibrate(string)
    @device.frequency.must_equal 13
  end

  it "decreases frequency with negative lines" do
    string = <<-EOF
+10
-4
    EOF
    @device.calibrate(string)
    @device.frequency.must_equal 6
  end

  it "locks frequency when repeated" do
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
    @device.calibrate(string, :lock => true)
    @device.frequency.must_equal 4
  end

  it "repeats input when lock required to find a lock" do
    string = <<-EOF
+3
-4
+5
    EOF
    @device.calibrate(string, :lock => true)
    @device.frequency.must_equal 3
  end

end
