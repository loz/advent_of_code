require "./src/calibrate"

device = Calibrate::Device.new
string = File.read("input")
device.calibrate(string, true)
puts "Calibrated To: ", device.frequency
