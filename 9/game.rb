class Game

  class Node
    attr_accessor :left, :right, :value
  end

  attr_reader :circle, :scores

  def initialize
    node = Node.new
    node.value = 0
    node.left = node
    node.right = node
    @head = node
    @first = node
    @next_marble = 1
  end

  def current
    @head.value
  end

  def place(marble)
    cw_rotate(1)
    next_node = @head.right

    node = Node.new
    node.value = marble
    node.left = @head
    node.right = next_node
    @head.right = node
    next_node.left = node
    @head = node
  end

  def remove_head
    removed = @head
    prev_node = @head.left
    next_node = @head.right
    prev_node.right = next_node
    next_node.left = prev_node
    @head = next_node
    removed.value
  end

  def ccw_rotate(n)
    n.times do
      @head = @head.left
      #puts "CCW:> #{zero_dump}"
    end
  end

  def cw_rotate(n)
    n.times do
      @head = @head.right
    end
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
        #puts "#{player} #{zero_dump}"
        removed = remove_head

        @scores[player] += removed
      else
        place(@next_marble)
      end
      @next_marble += 1
      @players.rotate!
      #§puts "#{player} #{zero_dump}"
    end
  end

  def include?(value)
    current = @first
    begin
      return true if current.value == value
      current = current.right
    end while current != @first
    false
  end

  def size
    current = @first
    size = 0
    begin
      current = current.right
      size += 1
    end while current != @first
    size
  end

  def zero_dump
    str = ""
    current = @first
    begin
      str += if current == @head
        "(%2s)" % current.value
      else
        " %2s " % current.value
      end
      current = current.right
    end while current != @first
    str
  end
end
