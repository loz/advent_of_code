require 'minitest/autorun'
require_relative './instructor'

describe Instructor do
  before do
    @instructor = Instructor.new
    @steps = <<-EOF
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
    EOF
  end

  describe "#process" do
    it "records all dependant steps for each step" do
      @instructor.process(@steps)
      
      @instructor.dependant('A').must_equal ['C']
      @instructor.dependant('B').must_equal ['A']
      @instructor.dependant('C').must_equal []
      @instructor.dependant('D').must_equal ['A']
      @instructor.dependant('E').must_equal ['B', 'D', 'F']
      @instructor.dependant('F').must_equal ['C']
    end
  end

  describe "#perform_steps" do
    it "completes in dependency and alphabetical order" do
      @instructor.process(@steps)

      @instructor.perform_steps

      @instructor.order.must_equal "CABDFE"
    end
  end

  describe "#perform_with_workers" do
    it "completes the steps with given worker count and basetime" do
      @instructor.process(@steps)

      time = @instructor.perform_with_workers(2, 0)
      
      time.must_equal 15
      @instructor.order.must_equal "CABFDE"
    end
  end

  describe "#available_steps" do
    it "returns steps with no dependencies" do
      @instructor.process(@steps)

      steps = @instructor.available_steps
      steps.must_equal ['C']
    end

    it "does not return steps which are complete" do
      @instructor.process(@steps)
      
      @instructor.complete('C')

      steps = @instructor.available_steps
      steps.wont_include 'C'
    end

    it "returns steps will complete dependencies" do
      @instructor.process(@steps)
      
      @instructor.complete('C')
      @instructor.complete('A')

      steps = @instructor.available_steps
      steps.count.must_equal 3
      steps.must_include 'B'
      steps.must_include 'D'
      steps.must_include 'F'
    end

  end

end
