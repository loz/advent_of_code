require 'minitest/autorun'
require_relative './sleep_tracker'

describe SleepTracker do
  before do
    @tracker = SleepTracker.new
  end

  def logs
      logs = <<-EOF
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-02 00:40] falls asleep
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:25] wakes up
[1518-11-01 00:55] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-02 00:50] wakes up
      EOF
  end

  describe "process_log_entries" do
    it "processes given entries in chronological order" do
      @tracker.process_log_entries(logs)
      @tracker.current_guard.must_equal "99"
      @tracker.sleep_for_guard("99").must_equal 10
      @tracker.sleep_for_guard("10").must_equal 45
    end
  end

  describe "sleepiest_guard" do
    it "returns the guard with most sleep logged" do
      @tracker.process_log_entries(logs)
      @tracker.sleepiest_guard.must_equal "10"
    end
  end

  describe "sleepiest_minute" do
    it "returns the minute within a log which has been sleeped in the most" do
      log = Array.new(60,0)
      log[13] = 12
      @tracker.sleepiest_minute(log).must_equal 13
      log[19] = 22
      @tracker.sleepiest_minute(log).must_equal 19
    end
  end

  describe "process_log_entry" do
    describe "Guard begins shift" do
      it "sets the current guard" do
        @tracker.process_log_entry("[1518-11-01 00:00] Guard #1234 begins shift")
        @tracker.current_guard.must_equal "1234"
      end
    end

    describe "Guard falls asleep" do
      before do
        @tracker.process_log_entry("[1518-11-01 00:00] Guard #1234 begins shift")
      end

      it "logs that the guard is asleep" do
        @tracker.guard_asleep?.must_equal false
        @tracker.process_log_entry("[1518-11-01 00:05] falls asleep")
        @tracker.guard_asleep?.must_equal true
      end
    end

    describe "Guard wakes up" do
      before do
        @tracker.process_log_entry("[1518-11-01 00:00] Guard #1234 begins shift")
        @tracker.process_log_entry("[1518-11-01 00:05] falls asleep")
      end

      it "logs sleep length for the current guard" do
        @tracker.process_log_entry("[1518-11-01 00:25] wakes up")
        @tracker.sleep_for_guard("1234").must_equal 20
      end
    end
  end
end
