class Immune
  attr_accessor :good, :bad

  class Group
    attr_accessor :units, :hit_points, :weaknesses, :immunity, :damage,
        :damage_points, :initiative, :target, :target_damage

    def effective_power
      units * damage_points
    end

    def name
      "#{hit_points}/EP:#{effective_power}@#{initiative}"
    end

    def damage_to(enemy)
      if enemy.immunity.include? damage
        0
      elsif enemy.weaknesses.include? damage
        effective_power * 2
      else
        effective_power
      end
    end

    def fight!
      if target.nil?
        #puts "#{name} DOES NOT attack"
        return
      end
      if units == 0 #AM DEAD
        #puts "#{name} CANNOT attack"
        return
      end
      damage = damage_to(target)
      units_hit = [(damage / target.hit_points), target.units].min
      #puts "#{name} attacks #{target.name}, killing #{units_hit} units"
      target.units -= units_hit
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
      @bad.reject {|g| g.units == 0 }
    else
      @good.reject {|g| g.units == 0}
    end
  end

  def dump
    puts "-" * 20
    puts "Immune System:"
    good.each do |g|
      puts "#{g.name} contains #{g.units} units"
    end
    puts "Infection:"
    bad.each do |g|
      puts "#{g.name} contains #{g.units} units"
    end
    puts "-" * 20
  end

  def fight!
    establish_targets
    #puts "-" * 20
    attack_ordered.each do |attacker|
      attacker.fight!
    end
    @good.reject! {|g| g.units == 0 }
    @bad.reject! {|g| g.units == 0 }
  end

  def establish_targets
    targeted = []
    target_ordered.each do |attacker|
      attacker.target = nil
      #puts "Targeting: #{attacker.initiative} #{targeted.map &:initiative}"
      possible = enemies(attacker) - targeted
      #p possible.map &:name
      #p targeted.map &:name
      targets = possible.map do |enemy|
        damage = attacker.damage_to(enemy)
        min_damage = enemy.hit_points
        #;puts "#{attacker.name} would deal #{enemy.name} #{damage} damage"
        [enemy, damage, min_damage]
      end
      targets.reject! {|t| t[1] == 0 } #Drop non-targets
      #targets.reject! {|t| t[1] < t[2] } #Skip ineffective attacks
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
      #if attacker.initiative == 7
      #  puts "7------"
      #  p  targets.map {|t| "%s -> %s" % [t[1],t[0].name] }
      #  puts "======="
      #end
      if targets.first
        targeted << targets.first[0]
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
        g2.initiative <=> g1.initiative
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

    matches = string.match /.*\(.*immune to ([^;]+).*\) with/
    if matches
      group.immunity = matches[1].split(", ").map &:to_sym
    else
      group.immunity = []
    end

    matches = string.match /.*\(.*weak to ([^;]+).*\) with/
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
