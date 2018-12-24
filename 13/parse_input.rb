require_relative './railway'

railway = Railway.new
track_file = File.open("input")
track = track_file.read

railway.load(track)

print "Running Trains"
print "\e[2J\e[f"
railway.dump
begin
  while railway.trains.count > 1
    #railway.console_plot_trains
    #railway.dump_trains
    railway.tick
    #railway.clear_crashes
    #print  '.'
    #sleep 0.01
  end
rescue => e
  puts "======ERROR======="
  p e
  railway.dump_trains
  puts "==========="
end
#railway.console_plot_trains
railway.dump_trains
