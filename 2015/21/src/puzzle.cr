class Puzzle
  @boss  = {0,0,0}

  WEAPONS = {
    "Dagger"    => {8,  4, 0},
    "Shortword" => {10, 5, 0},
    "Warhammer" => {25, 6, 0},
    "Longsword" => {40, 7, 0},
    "Greataxe"  => {74, 8, 0},
  }

  ARMOUR = {
    "None"       => {0,   0, 0},
    "Leather"    => {13,  0, 1},
    "Chainmail"  => {31,  0, 2},
    "Splintmail" => {53,  0, 3},
    "Bandedmail" => {75,  0, 4},
    "Platemail"  => {102, 0, 5},
  }

  RINGS = {
    "None"       => {0,   0, 0},
    "None2"      => {0,   0, 0},
    "Defense +1" => {20,  0, 1},
    "Damage +1"  => {25,  1, 0},
    "Defense +2" => {40,  0, 2},
    "Damage +2"  => {50,  2, 0},
    "Damage +3"  => {100, 3, 0},
    "Defense +3" => {80,  0, 3},
  }

  def process(str)
  end

  def boss(hit, damage, armour)
    @boss = {hit, damage, armour}
  end

  def fight(hit, damage, armour)
    boss_hit, boss_damage, boss_armour = @boss
    return true if armour > boss_damage
    boss_damage = boss_damage - armour
    damage = damage - boss_armour


    #Get to go first, so add 1 less hit
    #hit = hit + boss_damage - 1
    melive = (hit / boss_damage).ceil
    bosslive = (boss_hit / damage)
    #puts "----------------"
    #p melive
    #p bosslive
    #puts "----------------"

    if melive >= bosslive
      true
    else
      false
    end
  end

  def cheapest(myhits)
    choices = [] of String
    wincost = 9999999
    WEAPONS.each do |w, wstat|
      ARMOUR.each do |a, astat|
        RINGS.each do |r, rstat|
          RINGS.each do |or, orstat|
            next if r == or
            cost = wstat[0] + astat[0] + rstat[0] + orstat[0]
            damage = wstat[1] + astat[1] + rstat[1] + orstat[1]
            armour = wstat[2] + astat[2] + rstat[2] + orstat[2]
            win = fight(myhits, damage, armour)
            if win
              if cost < wincost
                wincost = cost
                choices = [w, a, r, or]
                puts "#{w},#{a},#{r},#{or} -> $$#{cost} -> #{damage}:#{armour}"
              end
            end
          end
        end
      end
    end
    {choices,wincost}
  end

  def worst(myhits)
    choices = [] of String
    losecost = 0
    WEAPONS.each do |w, wstat|
      ARMOUR.each do |a, astat|
        RINGS.each do |r, rstat|
          RINGS.each do |or, orstat|
            next if r == or
            cost = wstat[0] + astat[0] + rstat[0] + orstat[0]
            damage = wstat[1] + astat[1] + rstat[1] + orstat[1]
            armour = wstat[2] + astat[2] + rstat[2] + orstat[2]
            win = fight(myhits, damage, armour)
            if !win
              if cost > losecost
                losecost = cost
                choices = [w, a, r, or]
                puts "#{w},#{a},#{r},#{or} -> $$#{cost} -> #{damage}:#{armour}"
              end
            end
          end
        end
      end
    end
    {choices,losecost}
  end


  def result
    boss(103,9,2)
    items, cost = cheapest(100)
    p "Winning => ", items, cost
    items, cost = worst(100)
    p "Loosing => ", items, cost
  end

end
