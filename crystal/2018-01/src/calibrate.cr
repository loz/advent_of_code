# TODO: Write documentation for `Calibrate`
module Calibrate
  VERSION = "0.1.0"

  class Device
    property frequency

    def initialize()
      @frequency = 0 
      @observed = {} of Int32 => Bool
    end

    def calibrate(str, lock = false)
      locked = false 
      while !locked
        str.each_line do |line|
          val = line.to_i
          @frequency += val
          if @observed[@frequency]?
            locked = true
            break
          end
          @observed[@frequency]= true
        end
        locked ||= !lock
      end
    end
  end
end
