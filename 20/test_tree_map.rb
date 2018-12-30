require 'minitest/autorun'
require_relative './tree_map'

describe TreeMap do

  describe "build" do
    it "builds sequences" do
      tree = TreeMap.build("^NSEW$")
      
      tree.must_be :start?
      tree = tree.next
      tree.token.must_equal 'N'
      tree = tree.next
      tree.token.must_equal 'S'
      tree = tree.next
      tree.token.must_equal 'E'
      tree = tree.next
      tree.token.must_equal 'W'
      tree.next.must_be :terminal?
    end

    it "builds branches" do
      tree = TreeMap.build("^N(S|E)W$")

      tree = tree.next  #=> N
      tree = tree.next

      tree.must_be :split?
      tree.parts[0].token.must_equal 'S'
      tree.parts[1].token.must_equal 'E'
      
      tree = tree.next
      tree.token.must_equal 'W'
    end


  end

  describe "tree" do
    it "has a depth equal to (shortest) deepest move" do
      tree = TreeMap.build("^NSEW$")
      tree.depth.must_equal 4

      tree = TreeMap.build("^(E|W|N)N$")
      tree.depth.must_equal 2

      tree = TreeMap.build("^(EEE|WWW|NN)N$")
      tree.depth.must_equal 4

      tree = TreeMap.build("^ENWWW(NEEE|SSE(EE|N))$")
      tree.depth.must_equal 10

      tree = TreeMap.build("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$")
      tree.depth.must_equal 18

      tree = TreeMap.build("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$")
      tree.depth.must_equal 23

      tree = TreeMap.build("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$")
      tree.depth.must_equal 31
    end

    it "has depths for all spaces" do
      tree = TreeMap.build("^NSEW$")
      depths = tree.depths
      depths.keys.count.must_equal 2
      depths[[0,0]].must_equal 0 #X

      depths[[0,-1]].must_equal 1 #N
      #Short out as S -> 0, 0 SEEN already

      tree = TreeMap.build("^(EEE|WWW|NN)NS$")
      puts("^(EEE|WWW|NN)NS$")
      depths = tree.depths
      depths.keys.count.must_equal 12
      depths[[0,0]].must_equal 0 #X>
      depths[[1,0]].must_equal 1 #E
      depths[[2,0]].must_equal 2 #EE
      depths[[3,0]].must_equal 3 #EEE
      depths[[3,-1]].must_equal 4 #EEEN

      depths[[-1,0]].must_equal 1 #W
      depths[[-2,0]].must_equal 2 #WW
      depths[[-3,0]].must_equal 3 #WWW
      depths[[-3,-1]].must_equal 4 #WWWN

      depths[[0,-1]].must_equal 1 #N
      depths[[0,-2]].must_equal 2 #NN
      depths[[0,-3]].must_equal 3 #NNN


      tree = TreeMap.build("^(EEE|WWW)(NN|)NS$")
      puts("^(EEE|WWW)(NN|)NS$")

      depths = tree.depths
      depths.keys.count.must_equal 13

      depths[[0,0]].must_equal 0 #X

      depths[[1,0]].must_equal 1 #E
      depths[[2,0]].must_equal 2 #EE
      depths[[3,0]].must_equal 3 #EEE
      depths[[3,-1]].must_equal 4 #EEEN
      depths[[3,-2]].must_equal 5 #EEENN
      depths[[3,-3]].must_equal 6 #EEENNN

      depths[[-1,0]].must_equal 1 #W
      depths[[-2,0]].must_equal 2 #WW
      depths[[-3,0]].must_equal 3 #WWW
      depths[[-3,-1]].must_equal 4 #WWWN
      depths[[-3,-2]].must_equal 5 #WWWNN
      depths[[-3,-3]].must_equal 6 #WWWNNN
    end
  end

  describe "map" do
    it "continues after branches to next at end of each branch" do
      tree = TreeMap.build("^(E|W|N)N$")
      #tree.dump
      #puts ""

      map = TreeMap.map(tree)

      #puts "*" * 10
      #puts map.visualise
      #puts "*" * 10

map.string.must_equal <<-EOF
#######
###.###
###-###
#.#.#.#
#-#-#-#
#.|X|.#
#######
      EOF
    end

    it "branches more than left and right? E|W|S" do
      tree = TreeMap.build("^(E|W|N|S)$")

      #tree.dump
      #puts ""

      map = TreeMap.map(tree)

      #puts "*" * 10
      #puts map.visualise
      #puts "*" * 10

map.string.must_equal <<-EOF
#######
###.###
###-###
#.|X|.#
###-###
###.###
#######
      EOF
    end


    it "builds a map from Node Tree" do
      tree = TreeMap.build("^ENWWW(NEEE|SSE(EE|N))$")

      map = TreeMap.map(tree)

      #puts "*" * 10
      #puts map.string
      #puts "*" * 10

      map.string.must_equal <<-EOF
#########
#.|.|.|.#
#-#######
#.|.|.|.#
#-#####-#
#.#.#X|.#
#-#-#####
#.|.|.|.#
#########
      EOF
    end

    it "maps all branches out fully" do
      tree = TreeMap.build("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$")

      map = TreeMap.map(tree)

      #puts "*" * 10
      #puts map.visualise
      #puts "*" * 10

      map.string.must_equal <<-EOF
###########
#.|.#.|.#.#
#-###-#-#-#
#.|.|.#.#.#
#-#####-#-#
#.#.#X|.#.#
#-#-#####-#
#.#.|.|.|.#
#-###-###-#
#.|.|.#.|.#
###########
      EOF
    end
  end
 
end
