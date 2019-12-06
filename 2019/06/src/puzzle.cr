class Puzzle

    property lookup = {} of String => Planet
  
  class Planet
    property parent : (Planet|Nil)
    property children = [] of Planet
    property name = ""

    def initialize(@name, @parent=nil)
    end
  end

  def process(str)
    str.each_line do |line|
      process_line(line)
    end
  end

  def process_line(line)
    parentname, childname = line.split(")")
    #print "P:#{parentname} -> #{childname}"
    parent = find_planet(parentname)
    #print " #{parent.name}:#{parent} -> "
    child = find_planet(childname, parent)
    child.parent = parent
    parent.children << child
    #puts " #{child.name}:#{child}"
  end

  def find_planet(name, parent=nil)
    if @lookup[name]?
      @lookup[name]
    else
      create_planet(name, parent)
    end
  end

  def orbits(node, parents=0)
    #puts "@#{node.name} (#{parents})"
    total = parents
    node.children.each do |child|
      total += orbits(child, parents+1)
    end
    total
  end

  def create_planet(name, parent=nil)
    planet = Planet.new(name, parent)
    @lookup[name] = planet
    planet
  end

  def planet(at)
    @lookup[at]
  end

  def result
    com = planet("COM")
    puts "Total Oribits:", orbits(com)
  end

end
