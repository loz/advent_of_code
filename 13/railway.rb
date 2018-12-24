class Railway
  attr_reader :track, :crash_location, :trains

  def self.dump_around(track,x,y)
    puts "***"
    line1 = track[y-1] || []
    line2 = track[y] || []
    line3 = track[y+1] || []
    [line1,line2,line3].each do |line|
      print line1[x-1]
      print line1[x]
      puts  line1[x+1]
    end
    puts "***"
  end

  TURNS = {
    "L" => {
      ">" => "^",
      "^" => "<",
      "<" => "v",
      "v" => ">"
    },
    "S" => {
      ">" => ">",
      "^" => "^",
      "<" => "<",
      "v" => "v"
    },
    "R" => {
      ">" => "v",
      "^" => ">",
      "<" => "^",
      "v" => "<"
    }
  }

  class Train
    attr_accessor :x, :y, :direction

    def initialize
      @sequence = ["L", "S", "R"]
    end

    def move(track, empty_track)
      #puts "[%s, %s]" % [x,y]
      track[y][x] = empty_track[y][x]
      apply_direction
      succeeds = orient_train(track)

      track[y][x] = direction
      succeeds
    end

    def orient_train(track)
      cell = track[y][x]
      #Redo with Hash->map->map newdir | same?
      case cell
      when '/'
        case direction
        when '^'
          self.direction = '>'
        when 'v'
          self.direction = '<'
        when '<'
          self.direction = 'v'
        when '>'
          self.direction = '^'
        end   
      when '\\'
        case direction
          when '>'
            self.direction = 'v'
          when '<'
            self.direction = '^'
          when '^'
            self.direction = '<'
          when 'v'
            self.direction = '>'
        end
      when '+'
        turn
      when '|','-'
      else #CRASH!
        return false 
      end
      true
    end

    def turn
      rotation = @sequence.first
      new_direction = TURNS[rotation][direction]
      self.direction = new_direction
      @sequence.rotate!
    end

    def apply_direction
      #Redo with Hash->map dx, dy?
      case direction
      when '>'
        self.x += 1
      when '<'
        self.x -= 1
      when '^'
        self.y -= 1
      when 'v'
        self.y += 1
      end
      if self.x < 0 || self.y < 0
        raise :ExitError
      end
    end
  end

  def load(track)
    @track = track.lines
    @empty_track = clear_track(track)
    @trains = locate_trains(track)
    resort_train_order
  end

  def track_string
    @track.join
  end

  def tick
    @crashed = false
    trains = @trains.dup

    trains.each do |train|
      next unless @trains.include? train
      unless train.move(@track, @empty_track)
        @crash_location = [train.x, train.y] unless @crashed
        @crashed = true
        clear_crashes 
      end
    end
    resort_train_order
    #dump
  end

  def crashed?
    @crashed
  end

  def clear_crashes
    locations = @trains.map {|train| [train.x, train.y]}
    crash_locations = locations.select{ |train| locations.count(train) > 1 }
    crash_locations.uniq!
    @trains.reject! do |train|
      crash_locations.include? [train.x,train.y]
    end
    #clear the actual track
    crash_locations.each do |location|
      x, y = location
      @track[y][x] = @empty_track[y][x]
    end
  end

  def dump
    puts @track
  end

  def dump_trains
    puts '*******'
    @trains.each do |t|
      p t
    end
    puts '*******'
  end

  def dump_around(x,y)
    Railway.dump_around(@track, x, y)
  end

  def console_plot_trains
    print "\e[0;0H"
    dump
    print "\e[1m"
    print "\e[32m" #Green
    @trains.each do |train|
      print "\e[%d;%dH" % [train.y+1, train.x+1]
      print train.direction
    end
    print "\e[0;0H"
    print "\e[0m"
  end

  private

  def resort_train_order
    @trains.sort! do |t1, t2|
      if t1.y < t2.y
        -1
      elsif t1.y > t2.y
        1
      else
        t1.x <=> t2.x
      end
    end
  end

  def clear_track(track)
    @empty_track = track.gsub('>','-').
                         gsub('<','-').
                         gsub('^','|').
                         gsub('v','|').
                         lines
  end

  def locate_trains(track)
    trains = []
    track.lines.each_with_index do |row,y|
      row.chars.each_with_index do |cell, x|
        case cell
          when '>','<','^','v'
            train = Train.new
            train.x = x
            train.y = y
            train.direction = cell
            trains << train
            #dump_around(x,y)
        end
      end
    end
    trains
  end
end
