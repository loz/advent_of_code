require 'minitest/autorun'
require_relative './polymer'

describe Polymer do
  before do
    @polymer = Polymer.new
  end

  describe "#trigger" do
    it "does not shrink when no reaction is available" do
    	chain = "dabCBAcaDA"
      newchain = @polymer.trigger(chain)
      newchain.must_equal chain
    end

    it "breaks down the chain when adjacent present" do
      chain = "dabCBAcCcaDA"
      newchain = @polymer.trigger(chain)
      newchain.must_equal "dabCBAcaDA"
    end

    it "repeats breakdowns on new chain until no reaction" do
      chain = "dabAcCaCBAcCcaDA"
      newchain = @polymer.trigger(chain)
      newchain.must_equal "dabCBAcaDA"
    end

    it "does not breakdown non-opposite components" do
      chain = "abcDDeefg"
      newchain = @polymer.trigger(chain)
      newchain.must_equal chain
    end
  end

end
