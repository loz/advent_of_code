# TODO: Write documentation for `Calibrate`
module Calibrate
  VERSION = "0.1.0"

  class Device
    property frequency

    def initialize()
      @frequency = 0 
      @observed = [] of Int32
    end

    def calibrate(str)
      str.each_line do |line|
        val = line.to_i
        @frequency += val
        if @observed.includes? @frequency
          break
        end
        @observed << @frequency
      end
    end
  end
end
