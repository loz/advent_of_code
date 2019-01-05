class Immune
  attr_accessor :good, :bad

  class Group
    attr_accessor :units, :hit_points, :weaknesses, :immunity, :damage,
        :damage_points, :initiative, :target

    def effective_power
      units * damage_points
    end

    def damage_to(enemy)
      if enemy.immunity.include? damage
        0
      elsif enemy.weaknesses.include? damage
        damage_points * 2
      else
        damage_points
      end
    end
  end

  def initialize
    @good = []
    @bad = []
  end

  def groups
    all = good + bad
    all.sort! { |g1,g2| g2.initiative <=> g1.initiative }
  end

  def enemies(agressor)
    if @good.include? agressor
      @bad
    else
      @good
    end
  end

  def establish_targets
    target_ordered.each do |attacker|
      targets = enemies(attacker).map do |enemy|
        [enemy, attacker.damage_to(enemy)]
      end
      targets.reject! {|t| t[1] == 0 } #Drop non-targets
      targets.sort! do |t1,t2| 
        if t2[1] == t1[1]
          if t2[0].effective_power == t1[0].effective_power
            t2[0].initiative <=> t1[0].initiative
          else
            t2[0].effective_power <=> t1[0].effective_power
          end
        else
          t2[1] <=> t1[1]
        end
      end
      if targets.first
        attacker.target = targets.first[0]
      else
        attacker.target = nil
      end
    end
  end

  def target_ordered
    all = good + bad
    all.sort! do |g1,g2|
      if g1.effective_power == g2.effective_power
        g1.initiative <=> g2.initiative
      else
        g2.effective_power <=> g1.effective_power
      end
    end
  end

  def attack_ordered
    all = good + bad
    all.sort! do |g1,g2|
      g2.initiative <=> g1.initiative
    end
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
