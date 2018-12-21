class Device
  attr_reader :frequency

  def initialize
    @observed_frequencies = [0]
    @frequency = 0
  end

  def calibrate(calibration_string, options = {})
    lock = options.fetch(:lock, false)
    locked = false
    puts "Calibrating.."
    loop do
      calibration_string.each_line do |line|
        val = line.to_i
        #print "Current frequency (%s), change of (%s);" % [@frequency, val]
        @frequency += val
        #puts "resulting frequency (%s)\n" % @frequency
        if @observed_frequencies.include?(@frequency) && lock
          locked = true
          break
        end
        @observed_frequencies << @frequency
        #puts "(%s) New frequency: %s, %s" % [val, @frequency, @observed_frequencies.inspect]
      end
      break if !lock || (lock && locked)
      print "."
    end
    puts "Frequency Lock: %s" % @frequency if locked

  end
end
