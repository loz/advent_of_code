require_relative './instructor'

instructor = Instructor.new
instructions_file = File.open("input")
instructions = instructions_file.read

instructor.process(instructions)
#instructor.perform_steps
#puts "ORDER: #{instructor.order}"

puts "With Workers, 5 @ 60"

instructor.perform_with_workers(5, 60)
