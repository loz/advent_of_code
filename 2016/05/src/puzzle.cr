require "digest"

class Puzzle

  def process(str)
  end

  def result
    salt = "ojvtpuvg"
    digest = Digest::MD5
    idx = 1469590
    pass = "________"
    found = 0
    while found != 8
      d5 = ""
      d6 = ""
      d7 = ""
      d = ""
      while d5 != "00000"
        idx += 1
        d = digest.hexdigest(salt + idx.to_s)
        d5 = d[0,5]
        d6 = d[5]
        d7 = d[6]
      end
      puts "#{idx} => #{d}"
      if d6.to_i?
        pos = d6.to_i
        if pos < 8 && pass[pos] == '_'
          pass = pass.sub(pos, d7)
          found += 1
        end
      end
      puts "#{pass}, #{found} identified"
    end
    puts "Password: #{pass}"
  end

end
