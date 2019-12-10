class Puzzle

  ROT = "abcdefghijklmnopqrstuvwxyz" * 2


  property sector_sum = 0

  def process(str)
    str.each_line do |line|
      if valid?(line)
        room, sector = parse(line)
        @sector_sum += sector
        puts "#{decode(room,sector)} => #{sector}"
      end
    end
  end

  def checksum(room)
    room = room.gsub(/[^a-z]+/, "")
    freq = Hash(Char,Int32).new(0)
    room.each_char do |c|
      freq[c] += 1
    end
    pairs = freq.map {|k,v| {k,v} }
    sorted = pairs.sort do |a, b|
      #p "#{a}, #{b}, #{a <=> b}"
      if b[1] == a[1]
        a[0] <=> b[0]
      else
        b[1] <=> a[1]
      end
    end

    sum = ""
    5.times { |n| sum += sorted[n][0] }
    sum
  end

  def valid?(room)
    parts = room.match(/(.+)\[(.+)]/)
    if parts
      room = parts[1]
      csum = parts[2]
      checksum(room) == csum
    else
      false
    end
  end

  def parse(line)
    data = line.match(/(.+)-(\d+)\[.+\]/)
    if data
      {data[1],data[2].to_i}
    else
      {"",0}
    end
  end

  def sector(room)
    sec = room.match(/\d+/)
    if sec
      sec[0].to_i
    else
      0
    end
  end

  def decode(str, rot)
    newstr = ""
    str.each_char do |char|
      loc = ROT.index(char)
      if loc
        newloc = (loc + rot) % 26
        newstr += ROT[newloc]
      else
        newstr += char
      end
    end
    newstr
  end

  def result
    puts "Sector Sum: #{sector_sum}"
  end

end
