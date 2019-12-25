class StdIOIO 
  property buffer =  [] of Char
  @buffer_read = true

  def <<(val)
    print val.chr
  end

  def shift
    if @buffer.empty?
      if @buffer_read
        input = gets("\n", 1000)
        if input
          @buffer = input.chars
          @buffer_read = false
        end
        if @buffer.empty?
          @buffer_read = true
          return '\n'.ord.to_i64 
        end
      else
        @buffer_read = true
        return '\n'.ord.to_i64
      end
    end
    ch = @buffer.shift
    ch.ord.to_i64
  end
end

