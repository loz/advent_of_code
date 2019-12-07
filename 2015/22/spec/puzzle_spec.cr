require "spec"
require "./spec_helper"


# Are there less finite number of possible prior steps than possible next steps?
# -- This should avoid infitire loops

# Initial prior steps
# -------------------
# The maximum possible damage is Missile whilst Poison in effect = 4+3 -> 7
# Boss can die on your turn, 0..-6 points, if prior hit points > 0
# Boss can die on boss turn, but only with Poison and 1..3 hitpoints
# Boss states can only have alternate values of effect remaining (only case on your turn)

#There are a finite amount of actions to take the other way, limited especially if
#there is no sufficient mana, or if effect in progress.
#This may not be a bad search space, especially if BREADTH first is taken


describe Puzzle do

  it "can generate spell options for a given state" do
    puzzle = Puzzle.new
    state = State.new
    state.player = {10, 0, 500}

    possible_spells = puzzle.possible_spells(state)
    possible_spells.should contain "Magic Missile"
    possible_spells.should contain "Drain"
    possible_spells.should contain "Shield"
    possible_spells.should contain "Poison"
    possible_spells.should contain "Recharge"
  end

  it "does not allow spell already in effect" do
    puzzle = Puzzle.new
    state = State.new
    state.player = {10, 0, 500}
    state.boss = {10, 8}
    state.effects = { "Recharge" => 10 } 

    possible_spells = puzzle.possible_spells(state)
    possible_spells.should_not contain "Recharge"
  end

  it "does allow spell with expired effect" do
    puzzle = Puzzle.new
    state = State.new
    state.player = {10, 0, 500}
    state.boss = {10, 8}
    state.effects = { "Recharge" => 0 } 

    possible_spells = puzzle.possible_spells(state)
    possible_spells.should contain "Recharge"
  end

  it "does not allow spell with insufficient mana" do
    puzzle = Puzzle.new
    state = State.new
    state.player = {10, 0, 150}
    state.boss = {10, 8}

    possible_spells = puzzle.possible_spells(state)
    possible_spells.should contain "Magic Missile"
    possible_spells.should contain "Shield"
    possible_spells.should_not contain "Poison"
    possible_spells.should_not contain "Recharge"
  end

  context "determining win" do
    it "is a win when boss health is <= 0" do
      puzzle = Puzzle.new
      state = State.new
      state.player = {10, 0, 150}
      state.boss = {0, 8}

      state.win?.should eq true
    end

    it "is a loss when player health is <= 0" do
      puzzle = Puzzle.new
      state = State.new
      state.player = {0, 0, 150}
      state.boss = {10, 8}

      state.win?.should eq false
      state.loss?.should eq true
    end

    it "is neither win or loss when both health > 0" do
      puzzle = Puzzle.new
      state = State.new
      state.player = {10, 0, 150}
      state.boss = {10, 8}

      state.win?.should eq false
      state.loss?.should eq false
    end
  end
  
  context "generating the next two states" do
    it "casts Magic Missile" do
      puzzle = Puzzle.new
      state = State.new
      state.player = {10, 0, 500}
      state.boss = {10, 8}

      newstates = puzzle.cast(state, "Magic Missile")

      n_state = newstates[0]
      n_state.player.should eq({10,0,500-53})
      n_state.boss.should eq({6,8})
    end

    it "applies active effects" do
      puzzle = Puzzle.new
      state = State.new
      state.player = {10, 0, 500}
      state.boss = {10, 8}
      state.effects = {
        "Poison" => 3
      }

      newstates = puzzle.cast(state, "Magic Missile")

      n_state = newstates[0]
      n_state.player.should eq({10,0,500-53})
      n_state.boss.should eq({3,8})
      n_state.effects.should eq({"Poison" => 2})

      m_state = newstates[1]
      m_state.boss.should eq({0,8})
      m_state.effects.should eq({"Poison" => 1})
    end

    it "removes expired effects" do
      puzzle = Puzzle.new
      state = State.new
      state.player = {10, 7, 500}
      state.boss = {10, 8}
      state.effects = {
        "Shield" => 2
      }

      newstates = puzzle.cast(state, "Magic Missile")

      n_state = newstates[0]
      n_state.player.should eq({10,7,500-53})
      n_state.effects.should eq({"Shield" => 1})

      m_state = newstates[1]
      m_state.player.should eq({2,0,500-53})
      m_state.effects.should eq({} of String => Int32)
    end

    it "casts Drain" do
      puzzle = Puzzle.new
      state = State.new
      state.player = {10, 0, 500}
      state.boss = {10, 8}

      newstates = puzzle.cast(state, "Drain")

      n_state = newstates[0]
      n_state.player.should eq({10+2,0,500-73})
    end

    it "casts Shield" do
      puzzle = Puzzle.new
      state = State.new
      state.player = {10, 0, 500}
      state.boss = {10, 8}

      newstates = puzzle.cast(state, "Shield")

      n_state = newstates[0]
      n_state.player.should eq({10,7,500-113})
      n_state.effects.should eq({"Shield" => 6})

      m_state = newstates[1]
      m_state.player.should eq({9,7,500-113})
      m_state.effects.should eq({"Shield" => 5})
    end

    it "casts Poison" do
      puzzle = Puzzle.new
      state = State.new
      state.player = {10, 0, 500}
      state.boss = {10, 8}

      newstates = puzzle.cast(state, "Poison")

      n_state = newstates[0]
      n_state.player.should eq({10,0,500-173})
      n_state.effects.should eq({"Poison" => 6})

      m_state = newstates[1]
      m_state.player.should eq({2,0,500-173})
      m_state.effects.should eq({"Poison" => 5})
      m_state.boss.should eq({7,8})
    end

    it "casts Recharge" do
      puzzle = Puzzle.new
      state = State.new
      state.player = {10, 0, 500}
      state.boss = {10, 8}

      newstates = puzzle.cast(state, "Recharge")

      n_state = newstates[0]
      n_state.player.should eq({10,0,500-229})
      n_state.effects.should eq({"Recharge" => 5})

      m_state = newstates[1]
      m_state.player.should eq({2,0,500-229+101})
      m_state.effects.should eq({"Recharge" => 4})
      m_state.boss.should eq({10,8})
    end
  end


#    puzzle = Puzzle.new
#    puzzle.set_boss(100, 8)
#
#    prior = puzzle.generate_possible_last_moves
#
#    prior.should contain {
#      "Turn" => "player", #Death on BOSS Turn
#      "bossleft" => 3,  # or 2, 1
#      "player" => {0, 0, 0}
#      "cast" => "Poison",
#      "Effects" => [
#        {"Poison", 6}
#      ]
#    }
#  end

end
