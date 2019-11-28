# TODO: Write documentation for `Battle`
class Battle
  class Unit
    property targets = [] of Unit
    property pos : Tuple(Int32,Int32)
    property type : String
    property locations : Array(Tuple(Int32,Int32))

    def initialize(x, y, type : String)
      @type = type
      @pos = {x,y}
      @locations = [] of Tuple(Int32,Int32)
    end
    
    def determine_range(map)
      @locations = [] of Tuple(Int32,Int32)
      @targets.each do |target|
        tx, ty = target.pos
        @locations << {tx,ty-1} if map[ty-1][tx] == "."
        @locations << {tx-1,ty} if map[ty][tx-1] == "."
        @locations << {tx+1,ty} if map[ty][tx+1] == "."
        @locations << {tx,ty+1} if map[ty+1][tx] == "."
      end
    end
  end

  property units = [] of Unit
  property map

  def initialize
    @map = [] of Array(String)
  end

  def elves
    @units.select {|u| u.type == "E" }
  end

  def set_map(map_string)
    @round = 0
    @units = [] of Unit
    @map = [] of Array(String)
    find_units(map_string)
  end

  def define_targets
    @units.each do |unit|
      unit.targets = @units.select {|u| u.type != unit.type }
    end
  end

  def find_units(map_string)
    map_string.split("\n").each_with_index do |row, y|
      @map << [] of String
      row.split("").each_with_index do |cell, x|
        @map[y] << cell
        if cell == "E" || cell == "G"
          @units << Unit.new(x,y,cell)
        end
      end 
    end
  end
end
