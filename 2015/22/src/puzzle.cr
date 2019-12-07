class State
  property player = {0,0,0} 
  property boss = {0,0} 
  property effects = {} of String => Int32
  property manacost = 0

  def dump
    phit, pshield, pmana = player
    bhit, bdamage = boss
    puts "- Player has #{phit} hit points, #{pshield} armor, #{pmana} mana"
    puts "- Boss has #{bhit} hit points"
    effects.each do |e|
      puts e.inspect
    end
  end

  def ended?
    win? || loss?
  end

  def win?
    b, _ = boss
    b <= 0 && !loss?
  end

  def loss?
    p, _ = player
    p <= 0
  end

end

class Puzzle

  SPELLS = {
    #NAME => cost, damage, heal, shield, increase, effect_length|0
    "Magic Missile" => {53, 4, 0, 0, 0, 0},
    "Drain" => {73, 2, 2, 0, 0, 0},
    "Shield" => {113, 0, 0, 7, 0, 6},
    "Poison" => {173, 3, 0, 0, 0, 6},
    "Recharge" => {229, 0, 0, 0, 101, 5},
  }

  def possible_spells(state)
    spells = [] of String
    SPELLS.each do |spell, stats|
      next if (state.effects[spell]? && state.effects[spell] > 0)
      cost, _ = stats
      _, _, mana = state.player
      next if cost > mana
      spells << spell 
    end
    spells
  end

  def apply_hard_mode(state)
    new_state = state.dup
    phit, pshield, pmana = new_state.player

    phit -= 1
    new_state.player = {phit, pshield, pmana}
    new_state
  end

  def cast(state, spell)

    #puts "-- Player turn --"
    #state.dump 

    new_states = [] of State
    new_state = apply_hard_mode(state)
    new_state = apply_effects(new_state) unless new_state.ended?
    new_state = apply_spell(new_state, spell) unless new_state.ended?
    new_states << new_state
    #puts "Player casts #{spell}"

    #puts "-- Boss  turn --"
    #new_state.dump

    new_state = apply_effects(new_state) unless new_state.ended?
    new_state = boss_fight(new_state) unless new_state.ended?
    new_states << new_state
    #puts "Boss maybe deals damage"
    #puts "==== Player Wins ====" if state.win?
    new_states
  end

  def boss_fight(state)
    new_state = state.dup
    phit, pshield, pmana = new_state.player
    bhit, bdamage = new_state.boss

    phit -= (bdamage - pshield)
    new_state.player = {phit, pshield, pmana}
    new_state
  end

  def apply_effects(state)
    new_state = state.dup
    phit, pshield, pmana = new_state.player
    bhit, bdamage = new_state.boss

    effects = new_state.effects.dup
    effects.each do |spell,duration|
      #cost, damage, heal, shield, increase, effect_length|0
      _, damage, heal, shield, increase, _ = SPELLS[spell]
      #p spell, duration, damage, heal, increase
      bhit -= damage
      phit += heal
      pmana += increase
      if effects[spell] == 1
        effects.delete spell
        pshield -= shield
      else
        effects[spell] -= 1
      end
    end
    new_state.player = {phit, pshield, pmana}
    new_state.boss = {bhit, bdamage}
    new_state.effects = effects
    new_state
  end

  def apply_spell(state, spell)
    new_state = state.dup
    cost, damage, heal, shield, increase, effect_length = SPELLS[spell]
    phit, pshield, pmana = new_state.player
    bhit, bdamage = new_state.boss
    pmana -= cost
    spent = state.manacost + cost
    if effect_length == 0
      phit += heal
      bhit -= damage
    else
      if shield != 0
        pshield += shield
      end
      new_state.effects[spell] = effect_length
    end
    new_state.player = {phit, pshield, pmana}
    new_state.boss = {bhit, bdamage}
    new_state.manacost = spent
    new_state
  end

  def result
    state = State.new
    state.player = {50, 0, 500}
    state.boss = {55, 8}
  
    states = [state]
    allwins = [] of State
    cheapest = 999999
    20.times do |t|
      states = generation(states)
      print "Gen #{t}: #{states.size}"
      losses = states.select {|s| s.loss? }
      wins = states.select {|s| s.win? && !s.loss? }
      wins.each do |w|
        if w.manacost < cheapest
          cheapest = w.manacost
        end
      end
      allwins += wins
      print " -> #{losses.size} losses"
      print " -> #{wins.size} wins"
      states = states.select {|s| !s.loss? && !s.win? }
      print " -> #{states.size} in generation"
      states = states.select {|s| s.manacost < cheapest }
      puts " -> #{states.size} in cheaper than #{cheapest}"
      break if states.empty?
    end
    allwins.each do |w|
      p w
    end
    cost = allwins.min_by do |w|
      w.manacost
    end
    puts "Cheapest: #{cheapest}"
    puts "EG:", cost
  end

  def generation(states)
    newgen = [] of State
    states.each do |state|
      options = possible_spells(state)
      outcomes = options.map do |opt|
        #puts "=" * 40
        states = cast(state, opt)
        s1 = states.first
        s2 = states.last
        if s1.win? || s1.loss?
          s1
        else
          s2
        end
      end
      newgen = newgen + outcomes
    end
    newgen
  end

end
