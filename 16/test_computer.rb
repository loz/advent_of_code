require 'minitest/autorun'
require_relative './computer'

describe Computer do
  before do
    @computer = Computer.new
  end
  
  describe "Addition" do
    it "supports addr" do
      @computer.set_register(1, 12)
      @computer.set_register(2, 3)
      @computer.addr(1,2,3)
      @computer.register(3).must_equal 15

    end

    it "supports addi" do
      @computer.set_register(1, 12)
      @computer.addi(1,2,1)
      @computer.register(1).must_equal 14
    end
  end

  describe "Multiplication" do
    it "supports mulr" do
      @computer.set_register(1, 12)
      @computer.set_register(2, 3)
      @computer.mulr(1,2,3)
      @computer.register(3).must_equal 36
    end

    it "supports muli" do
      @computer.set_register(1, 3)
      @computer.muli(1,7,3)
      @computer.register(3).must_equal 21
    end
  end

  describe "Bitwise AND" do
    it "supports banr" do
      @computer.set_register(1, 123)
      @computer.set_register(2, 14)
      @computer.banr(1,2,3)
      @computer.register(3).must_equal 10
    end

    it "supports bani" do
      @computer.set_register(1, 12)
      @computer.bani(1,123,3)
      @computer.register(3).must_equal 8
    end
  end

  describe "Bitwise OR" do
    it "supports borr" do
      @computer.set_register(1, 123)
      @computer.set_register(2, 14)
      @computer.borr(1,2,3)
      @computer.register(3).must_equal (123 | 14)
    end

    it "supports bori" do
      @computer.set_register(1, 12)
      @computer.bori(1,123,3)
      @computer.register(3).must_equal (12 | 123)
    end
  end

  describe "Assignment" do
    it "supports setr" do
      @computer.set_register(1, 123)
      @computer.set_register(2, 14)
      @computer.setr(1,2,3)
      @computer.register(3).must_equal 123
    end

    it "supports seti" do
      @computer.seti(67,2,3)
      @computer.register(3).must_equal 67
    end
  end

  describe "Greater Than Testing" do
    it "supports gtir" do
      @computer.set_register(2, 14)

      @computer.gtir(20,2,3)
      @computer.register(3).must_equal 1

      @computer.gtir(14,2,3)
      @computer.register(3).must_equal 0
    end

    it "supports gtri" do
      @computer.set_register(1, 37)

      @computer.gtri(1,36,3)
      @computer.register(3).must_equal 1

      @computer.gtri(1,37,3)
      @computer.register(3).must_equal 0
    end

    it "supports gtrr" do
      @computer.set_register(1, 37)
      @computer.set_register(2, 12)

      @computer.gtrr(1,2,3)
      @computer.register(3).must_equal 1

      @computer.gtrr(2,1,3)
      @computer.register(3).must_equal 0
    end
  end

  describe "Equality Testing" do
    it "supports eqir" do
      @computer.set_register(2, 14)

      @computer.eqir(20,2,3)
      @computer.register(3).must_equal 0

      @computer.eqir(14,2,3)
      @computer.register(3).must_equal 1
    end

    it "supports eqri" do
      @computer.set_register(1, 37)

      @computer.eqri(1,36,3)
      @computer.register(3).must_equal 0

      @computer.eqri(1,37,3)
      @computer.register(3).must_equal 1
    end

    it "supports eqrr" do
      @computer.set_register(0, 12)
      @computer.set_register(1, 37)
      @computer.set_register(2, 12)

      @computer.eqrr(1,2,3)
      @computer.register(3).must_equal 0

      @computer.eqrr(0,2,3)
      @computer.register(3).must_equal 1
    end
  end

  describe "Match Opcodes" do
    it "returns list of opcodes which match execution output" do
      opcodes = @computer.match_opcodes("3, 2, 1, 1", "9 2 1 2", "3, 2, 2, 1")

      opcodes.count.must_equal 3

      opcodes.must_include :mulr
      opcodes.must_include :addi
      opcodes.must_include :seti
    end
  end

  describe "Exec" do
    it "executes using given instruction set" do
      opcodes = {
        8=>:mulr, 9=>:addr, 1=>:borr,
        0=>:muli, 10=>:bori, 6=>:addi,
        12=>:seti, 2=>:gtri, 4=>:gtrr,
        3=>:eqri, 5=>:eqir, 13=>:eqrr,
        15=>:gtir, 7=>:setr, 14=>:banr,
        11=>:bani
        }
      @computer.set_opcodes(opcodes)
      @computer.execute("12 8 0 0")  # [0] = 8
      @computer.execute("12 4 0 1")  # [1] = 4
      @computer.execute("7 1 0 2")   # [2] = [1]
      @computer.execute("9 0 2 3")   # [3] = [0] + [2]  => 12
      @computer.execute("4 3 0 1")   # [1] = [3] > [0]  => 1
      @computer.register(1).must_equal 1
    end
  end

end
