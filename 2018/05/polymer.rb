class Polymer
  def trigger(chain)
    chars = "abcdefghijklmnopqrstuvwxyz"
    uchars = chars.upcase
    reactors = chars.chars.zip uchars.chars
    reactors += uchars.chars.zip chars.chars
    reactors = reactors.map {|r| r.join }
    reactors = reactors.join('|')
    exp = Regexp.new(reactors)

    chain
    begin
      #print chain.length
      #print "."
      triggered = false
      newchain = chain.gsub(exp, '')
      if chain != newchain
        triggered = true
        chain = newchain
      end
    end while triggered
    chain
  end
end
