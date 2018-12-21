require_relative './device'

device = Device.new
calibration_file = File.open("input")
string = calibration_file.read
device.calibrate(string, :lock => true)
puts "Calibrated To: ", device.frequency
