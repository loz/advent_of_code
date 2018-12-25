class Recipe
  def initialize
    @results = "37"
    @elf_positions = [1,2]
  end


  def mix
    digits = 0
    @elf_positions.each do |pos|
      digits += @results[pos-1].to_i
    end
    digits = digits.to_s
    digits.each_char do |digit|
      @results << digit
    end
  end

  def move_elves
    max_size = @results.length
    @elf_positions.map! do |current_position|
      new_position = current_position + (@results[current_position-1].to_i)
      new_position = (new_position % max_size) + 1
      new_position
    end
  end
  
  def elf_position(pos)
    @elf_positions[pos-1]
  end

  def to_string
    @results
  end

  def elves_to_string
    str = " " * @results.size
    @elf_positions.each do |pos|
      str[pos-1] = "^"
    end
    str
  end

  def at(loc)
    @results[loc]
  end

  def run
    mix
    move_elves
  end

  def index_of(str)
    @results.index str
  end

  def score_after(n, length)
    while @results.length < (n + length)
      run
    end
    @results[n, length]
  end
end
