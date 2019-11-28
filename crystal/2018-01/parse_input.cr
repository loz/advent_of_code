require "./src/calibrate"

device = Calibrate::Device.new
string = File.read("input")
device.calibrate(string)
puts "Calibrated To: ", device.frequency
