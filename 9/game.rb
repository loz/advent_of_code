class Game
  attr_reader :circle, :scores

  def initialize
    @circle = [0]
    @count = 1
    @head = 0
    @next_marble = 1
  end

  def current
    @circle[@head]
  end

  def place(marble)
    cw_rotate(2)

    @circle.insert @head, marble

    @count += 1
  end

  def remove_head
    @count -= 1

    @circle.delete_at @head
  end

  def ccw_rotate(n)
    @head = @head + @count - n
    @head = @head % @count
  end

  def cw_rotate(n)
    @head = (@head += n) % @count
  end

  def current_player
    @players.first
  end

  def highest_score
    scores.max
  end


  def play(players, marbles)
    #puts ''
    @players = (1..players).to_a
    @scores = Array.new(players+1,0)
    marbles
    ten_percent = marbles / 10
    ten_percent = 1 if ten_percent.zero?
    while @next_marble <= marbles do
      if @next_marble % ten_percent == 0
        print '#'
      end

      player = current_player
      if @next_marble % 23 == 0
        @scores[player] += @next_marble
        ccw_rotate(7)
        removed = remove_head
        @scores[player] += removed
      else
        place(@next_marble)
      end
      @next_marble += 1
      @players.rotate!
      #puts "#{player} #{zero_dump}"
    end
  end

  def zero_dump
    circle = @circle.dup
    head = circle.first
    while circle.first != 0
      circle.rotate!
    end
    mapped = circle.map do |c|
      if c == head
        "(%2s)" % c
      else
        " %2s " % c
      end
    end
    mapped.join
  end
end
