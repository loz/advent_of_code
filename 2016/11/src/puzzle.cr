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

  def result
    puts "Todo"
  end

end
