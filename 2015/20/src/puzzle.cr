class Puzzle

  def presents(num)
    total = 0
    (1..num).each do |elf|
      if num % elf == 0
        total += (10*elf)
      end
    end
    total
  end

  def result
    target = 34_000_000
    max = (target / 10).to_i
    #Possible Houses
    counts = Array.new(max, 0)

    1.upto(max) do |n|
      counter = 0
      #Deliver present to every n house
      n.step(by: n, to: max-1) do |i|
        counts[i] += 11 * n
        counter += 1
        #Stop after 50
        break if counter == 50
      end
    end
    #Find First which is larger than goal
    puts counts.index { |c| c >= target }
  end

  def result1
    start = 460_000
    target = 34_000_000
    house = start
    100.times do |r|
    puts "Start: #{house} -> #{presents(house)}"
    50000.times do |t|
    #while true
      house += 1
      gifts = presents(house)
      if gifts >= target
        puts "Found #{house}"
        return
      end
    end
    puts "Not before #{house}"
    end
  end

end
