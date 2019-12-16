class Bot
  property id : Int32

  getter low : Bot|Nil
  getter high : Bot|Nil
  property values = [] of Int32

  def initialize(@id); end

  def pass_values(to)
    if values.size == 2 
      v1, v2 = values
      #puts "Bot #{id} cmp #{v1}, #{v2}"
      if to == high
        if v1 < v2
          to.try { |b| b.give(v2) }
        else
          to.try { |b| b.give(v1) }
        end
      else #low
        if v1 < v2
          to.try { |b| b.give(v1) }
        else
          to.try { |b| b.give(v2) }
        end
      end
    end
  end

  def low=(bot)
    @low = bot
    pass_values(@low)
  end

  def high=(bot)
    @high = bot
    pass_values(@high)
  end


  def give(val)
    values << val
    pass_values(low) if low
    pass_values(high) if high
  end
end

class Output < Bot
end

class Puzzle

  property bots = {} of Int32 => Bot
  property outs = {} of Int32 => Bot

  def process(str)
    str.each_line do |line|
      process_line(line)
    end
  end

  def process_line(line)
    process_bot(line) ||
    process_value(line)
  end

  def fetch_bot(num, type)
    if type == "bot"
      unless @bots[num]?
        @bots[num] = Bot.new(num)
      end
      @bots[num]
    else #output
      unless @outs[num]?
        @outs[num] = Bot.new(num)
      end
      @outs[num]
    end
  end

  def process_value(line)
    matches = line.match /value (\d+) goes to bot (\d+)/
    if matches
      value = matches[1].to_i

      thebot = matches[2].to_i
      bot  = fetch_bot(thebot,  "bot")
      bot.give(value)
      return true
    else
      return false
    end
  end

  def process_bot(line)
    matches = line.match /bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)/
    if matches
      thisbot = matches[1].to_i
      low_type = matches[2]
      low_num = matches[3].to_i

      high_type = matches[4]
      high_num = matches[5].to_i

      bot  = fetch_bot(thisbot,  "bot")
      low  = fetch_bot(low_num,  low_type)
      high = fetch_bot(high_num, high_type)

      bot.low = low
      bot.high = high

      return true
    else
      return false
    end
  end

  def bot(n)
    fetch_bot(n, "bot")
  end

  def out(n)
    fetch_bot(n, "out")
  end


  def result
    outs.each do |_, out|
      puts "Output #{out.id} -> #{out.values}"
    end
  end

end
