require "./src/puzzle"

puzzle = Puzzle.new
string = File.read("input")

amps = [] of Puzzle
5.times do 
  amp = Puzzle.new
  amp.process(string)
  amp.save_memory
  amps << amp
end

sequence = [5,6,7,8,9]
sequence.permutations.each do |seq|
  print "SEQ: #{seq}"
  inputs = [] of Tuple(IOPipe, Puzzle)
  seq.each_with_index do |phase, idx|
    pipe = IOPipe.new
    pipe << phase
    amp = amps[idx]
    amp.restore_memory
    inputs << {pipe, amp}
  end
  #Feed 0 signal to first amp
  results = Channel(IOPipe).new(5)

  inputs.first[0] << 0
  inputs.each_with_index do |input, idx|
    outsig, amp = input
    insig = if idx == 0
      pipe, _ = inputs.last
      pipe
    else
      pipe, _ = inputs[idx-1]
      pipe
    end
    #puts "#{insig} -> #{outsig}"
    #Spawn Amp Chain
    spawn do
      results.send(amp.execute(insig, outsig))
    end
  end
  5.times do |ampid|
    outs = results.receive
  end
  #Complete, what is in last IO pipe
  final = inputs.first[0].shift
  puts " -> #{final}"

end
