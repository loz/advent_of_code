class Puzzle

  INPUT = [
    Set.new([{:thulium, :generator}, {:thulium, :microchip}, {:plutonium, :generator}, {:strontium, :generator}]),
    Set.new([{:plutonium, :microchip}, {:strontium, :microchip}]),
    Set.new([{:promethium, :generator}, {:promethium, :microchip}]),
    Set.new([] of Tuple(Symbol, Symbol))
  ]

# States
# E[] | AG, AC, BG, BC -> E[AG,BG] | AC,BC
#                      -> E[AC,BC] | AG,BC 

  def process(str)
  end

  def valid?(elevator, floor)
    superset = elevator + floor
    not_invalid_elevator?(elevator) && (
      all_microchip?(superset) ||
      all_generator?(superset) ||
      all_unpaired_same?(superset)
    )
  end

  def lift_can_move?(elevator, floor)
    empty = Set.new([] of Tuple(Symbol, Symbol))
    valid?(empty, floor) && valid?(empty, elevator)
  end

  def lift_can_visit?(elevator, floor)
    empty = Set.new([] of Tuple(Symbol, Symbol))
    valid?(empty, elevator + floor)
  end

  def generate_lifts(floor,current)
    #options = [] of Tuple(Set.new([] of Set(Item)),Set.new([] of Set(Item)))
    options = [] of Tuple(Floor,Floor)

    empty = Set.new([] of Item)

    allfloor = floor + current
    
    #Empty Lift
    options << {empty,current}

    allfloor.each do |item|
      #just this in the lift
      option = Set{item}
      ofloor = floor - option
      if lift_can_move?(option, ofloor)
        left = current - ofloor
        options << {option, left}
      end

      #this plus another item
      floor.each do |otheritem|
        next if item == otheritem
        option = Set{item, otheritem}
        ofloor = floor - option
        if lift_can_move?(option, ofloor)
          left = current - ofloor
          options << {option, left}
        end
      end
    end
    options
  end

  def all_unpaired_same?(set)
    gens = set.select do |i|
      i[1] == :generator
    end.map {|i| i[0] }
    chips = set.select do |i|
      i[1] == :microchip
    end.map {|i| i[0] }
    (gens - chips).empty?  || (chips-gens).empty?
  end

  def not_invalid_elevator?(elevator)
    elevator.empty? ||
    all_microchip?(elevator) ||
    all_generator?(elevator) ||
    paired_items?(elevator)
  end

  def paired_items?(set)
    first = set.first
    set.all? {|i| i[0] == first[0] }
  end

  def all_microchip?(set)
    set.all? {|i| i[1] == :microchip }
  end

  def all_generator?(set)
    set.all? {|i| i[1] == :generator }
  end


  alias Item = Tuple(Symbol,Symbol)
  alias Floor = Set(Item)
  alias State = Tuple(Int32,Set(Item),Array(Set(Item)))

  def next_states(states, visited)
    newstates = [] of State
    #We are visiting
    states.each { |s| visited[s] = true }
    generated = {} of State => Bool

    states.each do |state|
      curfloor, lift, floors = state
      #p curfloor
      floor = floors[curfloor]
      #puts floor


      options = generate_lifts(floor, lift)
      options.each do |option|
        taken, left = option
        #puts "->#{option}"
        if curfloor >0 #Go DOWN
          newfloors = floors.dup
          newfloors[curfloor] -= taken
          newfloors[curfloor] += left

          newfloor = curfloor-1
          targetfloor = floors[newfloor]
          if valid?(Set.new([] of Item), newfloors[curfloor]) &&
             lift_can_visit?(taken, targetfloor)

            newstate = {newfloor, taken, newfloors}
            unless visited[newstate]? || generated[newstate]?
              newstates << newstate
              generated[newstate] = true
            end
          end
        end

        if curfloor <3 #Go UP
          newfloors = floors.dup
          newfloors[curfloor] -= taken
          newfloors[curfloor] += left

          newfloor = curfloor+1
          targetfloor = floors[newfloor]
          if valid?(Set.new([] of Item), newfloors[curfloor]) &&
             lift_can_visit?(taken, targetfloor)

            newstate = {newfloor, taken, newfloors}
            unless visited[newstate]? || generated[newstate]?
              newstates << newstate
              generated[newstate] = true
            end
          end
        end
      end
    end
    {newstates, visited}
  end

  def target?(state)
    floor, lift, floors = state
    floors[0].empty? &&
    floors[1].empty? &&
    floors[2].empty?
  end

  def dump_states(states)
    puts "="*50
    states.each do |state|
      dump_state(state)
      puts "="*50
    end
  end

  def dump_state(state)
    floor, elevator, floors = state
    floors.each_with_index do |f, idx|
      print "#{idx} || #{f}"
      if idx == floor
        puts " || #{elevator}"
      else
        puts
      end
    end
  end

  def result
    elevator = Set.new([] of Item) #empty

    state = {2, elevator, INPUT.dup } #Start on the 3rd Floor, empty elevator
    step = 0
    
    visited = {} of State => Bool
    nextstates = [state]

    20.times do 
      nextstates, visited = next_states(nextstates,visited)
      step += 1
      #dump_states(nextstates)
      #puts "|" * 50
      puts "Step #{step} #{nextstates.size} new states, #{visited.keys.size} visited"
      #puts "|" * 50
      if nextstates.any? {|s| target?(s) }
        puts "FOUND!"
        raise "STOP"
      end
    end
  end

end
