require "./intcode"
require "./stdioio"

class Puzzle

  TABLES = [
    "110100?1?",

    "10?111???",
    "10?110?1?",
    "10?110??1",
    "10?10??1?",
    #"0??111???",
    #"0??110??1",
    #"0??10??1?",
    "0????????" #could be too late, so who cares, couldn't prevent
   #"ABCDEFGHI"
  ]

  # Focus on ### dont
  #          ##   Maybe
  #          #    Maybe
  #    Is    #...##     Doable?
  #    Or    #...#...#  Doable?
  # D && 
  # !(A&B&C) &&
  # (H | E)

  #NOT A
  # OR
  #A AND NOT B
  #    D AND (H OR (E AND I) OR (E AND F))
  # OR
  #A AND B AND NOT C
  #    AND D AND NOT E AND NOT F AND H
"
  (
    !A ||
   ( A & D & !B & ( H ||   (E & (I || F)))) ||
   ( A & D &  B &  !H &    !E &      !F & !C )
  )

  (
    !A ||

   ( A & D & (
      ( !B & ( H ||   (E & (I || F)))) ||
      (  B &  !H &    !E &      !F & !C)
     )
   )
  )

  (
    !A ||

   ( A & D & (
      ( !B &  ( H ||   (E & (I || F)))) ||
      (  B &  !(H ||    E      || F ||  C) )
     )
   )
  )

           T &  F  &  F  &  F  &  F
  !A &  T
   T    F  F
   T    T  F
   F    F  F
   F    T  T
   A & !T     !T   /A
   T    F  T   F    T
   T    T  T   F    T
   F    F  F   T    T
   F    T  F   T    T
   A / !T     !T 
   T    F  T   F 
   T    T  T   F
   F    F  T   F
   F    T  F   T


  # !B && ...  (Single)
  NOT F T
  NOT T T
  OR I T
  AND E T
  OR H T
  NOT T T
  OR B T
  NOT T T

  # !B && ...  (Multi)
  NOT F J
  NOT T J
  OR I J
  AND E J
  OR H J
  NOT B T
  AND T J

  #B -> !(...C
  NOT C T
  NOT T T
  OR F T 
  OR E T
  OR H T
  NOT T T
  AND B T
 
  OR T J

  AND D J
  AND A J

  NOT D T
  OR T J
"

  property machine = Intcode.new
  
  def process(str)
    machine.process(str)
  end

  def gen_partial(pattern, prefix, table)
    bits = prefix
    pattern.each_char_with_index do |ch, idx|
      if ch == '?'
        #puts pattern
        #puts bits
        rest = pattern[idx+1, pattern.size]
        #puts "Rest: #{rest}"
        gen_partial(rest, bits + '0', table)
        gen_partial(rest, bits + '1', table)
        return
      else
        bits += ch
      end
    end
    table[bits] = true
  end

  def gen_truth_tables
    table = {} of String => Bool
    TABLES.each do |pattern|
      gen_partial(pattern, "", table)
    end
    #Now Gen The false
    512.times do |val|
      bits = ""
      9.times do |b|
        bits += val.bit(b).to_s
      end
      unless table[bits]?
        table[bits] = false
      end
    end
    table.each do |k,v|
      puts "#{k} -> #{v}"
    end
  end

  def manual_run
    #   @
    #  ##...#

    #   @
    #  ###..

    # If there is a cap on A|B|C and D is NOT a gap, then JUMP?
    io = StdIOIO.new
    machine.execute io, io
  end

  def run_steps(steps)
    io = StdIOIO.new
    io.buffer = steps.chars
    machine.execute io, io
  end

  def part_one
    steps = <<-EOF
    NOT D T
    NOT T J
    NOT A T
    NOT T T
    AND B T
    AND C T
    NOT T T
    AND T J
    WALK

    EOF
    run_steps(steps)
  end

  def part_two
    steps = <<-EOF
    OR A J
    AND B J  
    AND C J  
    NOT J J  
    AND D J  
    OR E T  
    OR H T  
    AND T J  
    RUN

    EOF
    run_steps(steps)
  end

  def result
    machine.save_memory
    #part_one
    part_two
    #manual_run
    #gen_truth_tables
  end
end
