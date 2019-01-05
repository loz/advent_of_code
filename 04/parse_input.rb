require_relative './sleep_tracker'

tracker = SleepTracker.new
log_file = File.open("input")
lines = log_file.read
tracker.process_log_entries(lines)
tracker.dump
guard = tracker.sleepiest_guard
logs = tracker.sleep_log_for_guard(guard)
min = tracker.sleepiest_minute(logs)
puts "Sleepiest Guard: %s" % guard
puts "Sleepiest Guard Min: %s" % min
guards = tracker.guards
guards.each do |guard|
  print "%6s:" % guard
  logs = tracker.sleep_log_for_guard(guard)
  min = tracker.sleepiest_minute(logs)
  times = logs[min]
  print " Sleepiest Minute: %2s, %s times" % [min, times]
  puts ""
end
