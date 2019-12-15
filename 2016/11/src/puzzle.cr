class Puzzle

  INPUT = [
    [{:thulium, :generator}, {:thulium, :microchip}, {:plutonium, :generator}, {:strontium, :generator}],
    [{:plutonium, :microchip}, {:strontium, :microchip}],
    [{:promethium, :generator}, {:promethium, :microchip}],
    [] of Tuple(Symbol, Symbol)
  ]

# States
# E[] | AG, AC, BG, BC -> E[AG,BG] | AC,BC
#                      -> E[AC,BC] | AG,BC 

  def process(str)
  end

  def valid?(elevator, floor)
    superset = elevator + floor
    not_mixed_elevator?(elevator) && (
      all_microchip?(superset) ||
      all_generator?(superset) ||
      all_unpaired_same?(superset)
    )
  end

  def lift_can_move?(elevator, floor)
    empty = [] of Tuple(Symbol, Symbol)
    valid?(empty, floor) && valid?(empty, elevator)
  end

  def lift_can_visit?(elevator, floor)
    empty = [] of Tuple(Symbol, Symbol)
    valid?(empty, elevator + floor)
  end

  def generate_lifts(floor)
    options = [] of Array(Tuple(Symbol,Symbol))
    floor.each do |item|
      #just this in the lift
      option = [item]
      options << option if lift_can_move?(option, floor - option)

      #this plus another item
      floor.each do |otheritem|
        next if item == otheritem
        option = [item, otheritem]
        options << option if lift_can_move?(option, floor - option)
      end
    end
    uniq = [] of Array(Tuple(Symbol, Symbol))
    options.each do |option|
      if option.size == 1
        uniq << option
      else
        other = [option[1], option[0]]
        uniq << option unless uniq.includes?(other)
      end
    end
    uniq
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

  def not_mixed_elevator?(elevator)
    elevator.empty? ||
    all_microchip?(elevator) ||
    all_generator?(elevator)
  end

  def all_microchip?(set)
    set.all? {|i| i[1] == :microchip }
  end

  def all_generator?(set)
    set.all? {|i| i[1] == :generator }
  end

  def next_states(states, visited)
    newstates = [] of Array(Array(Tuple(Symbol,Symbol)))
    #We are visiting
    states.each { |s| visited[s] = true }
    generated = {} of Array(Array(Tuple(Symbol,Symbol))) => Bool

    states.each do |state|

      state.each do |floor|
        #puts floor
        options = generate_lifts(floor)
        options.each do |option|
          #puts "->#{option}"
          newstate = [] of Array(Tuple(Symbol,Symbol))
          state.each do |nextfloor|
            if nextfloor == floor
              #puts "|| => #{floor - option}"
              newstate << (floor-option)
            elsif lift_can_visit?(option,nextfloor)
              #puts "|| ?> #{nextfloor + option}" 
              newstate << (nextfloor + option)
            else
              #puts "||  > #{nextfloor}" 
              newstate << nextfloor
            end
          end
          #puts "=" * 50
          unless visited[newstate]? || generated[newstate]?
            generated[newstate] = true
            newstates << newstate 
          end
        end
      end
    end
    {newstates, visited}
  end

  def target?(state)
    state[0].empty? &&
    state[1].empty? &&
    state[2].empty?
  end

  def result
    state = INPUT.dup
    step = 0
    
    visited = {} of Array(Array(Tuple(Symbol,Symbol))) => Bool
    nextstates = [state]

    10.times do 
    nextstates, visited = next_states(nextstates,visited)
    step += 1
    puts "Step #{step} #{nextstates.size} new states, #{visited.keys.size} visited"
    if nextstates.any? {|s| target?(s) }
      puts "FOUND!"
      raise "STOP"
    else
      puts "LOOP"
    end
    end
  end

end
