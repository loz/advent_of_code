require 'minitest/autorun'
require_relative './recipe'

describe Recipe do
  before do
    @recipe = Recipe.new
  end

  describe "#mix" do
    it "mixes the next recipe(s)" do
      @recipe.mix

      @recipe.at(-1).must_equal "0"
      @recipe.at(-2).must_equal "1"
    end

    it "mixes using the elf positions" do
      3.times do
        @recipe.mix
        @recipe.move_elves
      end
      @recipe.to_string.must_equal "3710101"
    end
  end

  describe "#move_elves" do
    it "moves the elves to their new locations" do
      @recipe.mix
      @recipe.mix
      @recipe.move_elves

      @recipe.elf_position(1).must_equal 5
      @recipe.elf_position(2).must_equal 4
    end
  end

  describe "#score_after" do
    it "gives n digets after x recipes" do
      15.times do 
        @recipe.mix
        @recipe.move_elves
      end

      score = @recipe.score_after(9, 10)
      score.must_equal "5158916779"

      score = @recipe.score_after(5, 10)
      score.must_equal "0124515891"

      score = @recipe.score_after(18, 10)
      score.must_equal "9251071085"

      score = @recipe.score_after(2018, 10)
      score.must_equal "5941429882"
    end
  end

  describe "#index_of" do
    it "returns the index of a search score" do
      20.times { @recipe.run }
      index = @recipe.index_of("51589")
      index.must_equal 9
    end

    it "return nil if not found" do
      index = @recipe.index_of("59414")
      index.must_equal nil
    end
  end
end
