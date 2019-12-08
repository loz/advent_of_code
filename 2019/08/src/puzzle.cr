class Puzzle

  property layers = [] of String
  property width = 0
  property height = 0

  def process(str, width, height)
    layersize = width*height
    @width = width
    @height = height
    puts "#{layersize} pixels per layer, chunk of #{str.size}"
    while str != "\n" && str != ""
      layer = str[0,layersize]
      @layers << layer
      str = str[layersize, str.size-layersize]
    end
  end

  def count_digit(digit, layer)
    total = 0
      layer.each_char do |c|
        total += 1 if c.to_i == digit
      end
    total
  end
  
  def compose(layer1, layer2)
    newlayer = layer2.dup
    layer1.each_char_with_index do |c, idx|
      newlayer = newlayer.sub(idx,c) if c != '2'
    end
    newlayer
  end

  def draw_image(image)
    str = image.gsub("0", ".").gsub("1", "#")
    height.times do
      row = str[0,width]
      puts row
      str = str[width, str.size-width]
    end
  end

  def result
    part1 = false
    if(part1)
      layers.each do |layer|
        zero = count_digit(0, layer)
        one = count_digit(1, layer)
        two = count_digit(2, layer)
        puts "#{layer} :: #{zero} -> #{one*two}"
      end
    else
      image = layers.shift
      layers.each do |layer|
        image = compose(image, layer)
      end
      draw_image(image)
    end
  end

end
