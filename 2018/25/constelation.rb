class Constelation
  attr_reader :constelations

  def initialize
    @constelations = []
  end

  def add(string)
    star = parse_string(string)
    constelation = find_constelation(star)
    constelation << star
  end

  private

  def find_constelation(star)
    if @constelations.empty?
      new_constelation
    else
      links = @constelations.select do |constelation|
        linked_to?(constelation, star)
      end
      if links.count == 1
        links.first
      elsif links.count > 1
        merged = []
        links.each do |link|
          @constelations.delete link
          merged += link
        end
        @constelations << merged
        merged
      else
        new_constelation
      end
    end
  end

  def linked_to?(constelation, star)
    constelation.any? do |constelation_star|
      distance(constelation_star, star) <= 3
    end
  end
  
  def distance(star1, star2)
    x1, y1, z1, t1 = star1
    x2, y2, z2, t2 = star2
    (x2-x1).abs + (y2-y1).abs + (z2-z1).abs + (t2-t1).abs
  end

  def new_constelation
    constelation = []
    @constelations << constelation
    constelation
  end

  def parse_string(string)
    string.split(",").map &:to_i
  end
end
