class Immune
  class Group
    attr_accessor :units, :hit_points, :weaknesses, :immunity, :damage,
        :damage_points, :initiative
  end

  def parse_group(string)
    group = Group.new
    #matches = string.match /(.+) units each with (.+) hit points \(weak to (.+)+(,(.+))*\) with an attack that does (.+) (.+) damage at initiative (.+)/
    matches = string.match /(.+) units each with (.+) hit points/
    group.units = matches[1].to_i
    group.hit_points = matches[2].to_i

    matches = string.match /.*\(immune to ([^;]+).*\) with/
    if matches
      group.immunity = matches[1].split(", ").map &:to_sym
    else
      group.immunity = []
    end

    matches = string.match /.*\(.*weak to (.+)\) with/
    if matches
      group.weaknesses = matches[1].split(", ").map &:to_sym
    else
      group.weaknesses = []
    end

    matches = string.match /.*that does (.+) (.+) damage at initiative (.+)/
    group.damage = matches[2].to_sym
    group.damage_points = matches[1].to_i
    group.initiative = matches[3].to_i

    group
  end
end
