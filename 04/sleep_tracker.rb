require 'time'

class SleepTracker
  attr_reader :current_guard

  def initialize
    @asleep = false
    @sleep_counters = Hash.new { Array.new(60,0) }
  end

  def guards
    @sleep_counters.keys
  end

  def process_log_entries(logs)
    lines = logs.lines.sort
    lines.each do |log|
      process_log_entry(log)
    end
  end

  def sleepiest_guard
    doze = 0
    guard = nil
    @sleep_counters.each do |g, tracks|
      dozes = tracks.sum
      #p "Guard #{g} Dozed #{dozes}"
      if dozes > doze
        guard = g
        doze = dozes
      end
    end
    guard
  end

  def sleepiest_minute(track)
    largest = track.max
    track.index(largest)
  end

  def guard_asleep?
    @asleep
  end

  def process_log_entry(log)
    log.chomp!
    time, entry = split_log(log)
    if entry.start_with? "Guard"
      process_shift(entry)
    elsif entry == "falls asleep"
      fall_asleep(time)
    elsif entry == "wakes up"
      wake_up(time)
    end
  end

  def sleep_log_for_guard(guard)
    @sleep_counters[guard]
  end

  def sleep_for_guard(guard)
    @sleep_counters[guard].sum
  end

  def dump
    @sleep_counters.each do |guard, counter|
      print "%10s: " % guard
      counter.each do |m|
        if m.zero?
          print ".  |"
        else
          print "%3s|" % m
        end
      end
      puts ""
    end
  end

  def wake_up(time)
    sleep_at = minutes_past(@sleeptime)
    wake_at = minutes_past(time)
    length = wake_at-sleep_at
    puts "Guard: #{@current_guard} slept #{length}mins"
    counter = @sleep_counters[@current_guard]
    length.times do |m|
      min = sleep_at + m
      counter[sleep_at + m] += 1
    end
    @sleep_counters[@current_guard] = counter
  end

  def minutes_past(time)
    time[-2,2].to_i
  end

  def fall_asleep(time)
    @asleep = true
    @sleeptime = time
  end

  def split_log(log)
    time = log[1,16]
    entry = log[19,log.length]
    [time, entry]
  end

  def process_shift(entry)
    guard, id, rest = entry.split
    @current_guard = id.delete("#")
  end
end
