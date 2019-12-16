require "./intcode"

class IOPipe 
  @buffer = Channel(Int64).new(2)

  def <<(val)
    @buffer.send(val)
  end

  def shift
    @buffer.receive
  end

  def first
    Channel.receive_first(@buffer)
  end
end

