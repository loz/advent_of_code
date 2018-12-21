class Fabric

  def initialize
    @spaces = Array.new(1000) do
      Array.new(1000) do
        Array.new
      end
    end
  end

  def find_unshared_claims
    shares = find_claim_shares
    unshared = []
    shares.each do |id,share|
      if share.length == 1
        unshared << id
      end
    end
    unshared
  end

  def find_claim_shares
    shares = Hash.new { [] }
    @spaces.each do |row|
      row.each do |cell|
        cell.each do |claimid|
          shares[claimid] = (shares[claimid] + cell).uniq
        end
      end
    end
    shares
  end

  def overlapping_squares
    overlaps = 0
    @spaces.each do |row|
      row.each do |cell|
        overlaps += 1 if cell.count > 1
      end
    end
    overlaps
  end

  def apply_claims(lines)
    lines.each_line do |line|
      claim = parse_claim(line)
      apply_claim(claim)
    end
    #dump(10,10)
  end

  def apply_claim(claim)
    claim[:height].times do |row|
      claim[:width].times do |col|
        x = claim[:x] + col
        y = claim[:y] + row
        #puts "Claim: (%s, %s)" % [x, y]
        @spaces[x][y] << claim[:id]
      end
    end
  end

  def dump(width, height)
    height.times do |row|
      width.times do |col|
        claims = @spaces[row][col]
        if claims.empty?
          print '.'
        elsif claims.length == 1
          print claims[0]
        else
          print 'X'
        end
      end
      puts ''
    end
  end

  def parse_claim(line)
    id, at, location, size = line.split
    x, y = location.split(',')
    width, height = size.split('x')

    claim = {
      :id => id.delete("#").to_i,
      :x => x.to_i,
      :y => y.delete(":").to_i,
      :width => width.to_i,
      :height => height.to_i
    }
    claim
  end
end
