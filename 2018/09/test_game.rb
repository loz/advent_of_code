require 'minitest/autorun'
require_relative './game'

describe Game do
  before do
    @game = Game.new
  end

  describe "#place_marble" do
    it "places a marble in the circle" do
      @game.place(123)
      @game.current.must_equal 123
    end

    it "places one marble clockwise" do
      @game.place(123)
      @game.place(345)
      @game.current.must_equal 345
      @game.ccw_rotate(2)
      @game.current.must_equal 123
    end
  end

  describe "#play" do
    it "places all marbles working around each player" do
      @game.play(2, 5)
      @game.size.must_equal 6  #-0 1-1 2-2 1-3 2-4 1-5 => end
      @game.current_player.must_equal 2
    end

    it "does not place marbles which are multiples of 23" do
      @game.play(2, 47)
      @game.wont_include 23
      @game.wont_include 46
    end

    it "score the 23 multple marble for the current player, and the one 7 CCW left" do
      @game.play(2, 23)
      scores = @game.scores
      scores[1].must_equal 32
    end

    it "scores correctly for players" do
      @game.play(9, 25)
      @game.highest_score.must_equal 32
=begin
      game = Game.new
      game.play(10, 1618)
      game.highest_score.must_equal 8317

      game = Game.new
      game.play(13, 7999)
      game.highest_score.must_equal 146373
=end

    end
  end

end
