class Puzzle

  @ingredients = {} of String => Tuple(Int32, Int32, Int32, Int32, Int32)

  def process(str)
    str.lines.each do |line|
      process_line(line)
    end
  end

  def score(recipe)
    total = 0
    total_capacity = 0
    total_durability = 0
    total_flavor = 0
    total_texture = 0
    total_calories = 0
    recipe.each do |ingredient, spoons|
      capacity, durability, flavor, texture, calories = @ingredients[ingredient]
      total_capacity += (capacity * spoons)
      total_durability += (durability * spoons)
      total_flavor += (flavor * spoons)
      total_texture += (texture * spoons)
      total_calories += (calories * spoons)
    end
    if total_capacity < 1 ||  total_durability < 1 ||
       total_flavor < 1 || total_texture < 1
       total = 0
    else
      total = (total_capacity * total_durability * total_flavor * total_texture)
    end
    {total, total_calories}
  end

  def process_line(line)
    match = line.match /(.+): capacity (-*\d+), durability (-*\d+), flavor (-*\d+), texture (-*\d+), calories (-*\d+)/
    if match
      name = match[1]
      capacity = match[2].to_i
      durability = match[3].to_i
      flavor = match[4].to_i
      texture = match[5].to_i
      calories = match[6].to_i
      @ingredients[name] = {capacity, durability, flavor, texture, calories}
    else
      puts "Cannot Parse: ", line
    end
  end

  def result
    p @ingredients.keys
    best = {} of String => Int32
    best_score = 0
    max_spoons = 100
    generate_partial([] of Tuple(String,Int32), max_spoons, @ingredients.keys, best, best_score)
  end

  def generate_partial(part, spoons_left, rest, best, best_score)
    if rest.size == 1
      new_part = part.dup
      new_ingredient = rest.first
      new_part << {new_ingredient,spoons_left}
      recipe = new_part.to_h
      recipe_score, recipe_cals = score(recipe)
      if (recipe_score > best_score) && recipe_cals == 500
        puts "New Best: #{recipe}, #{recipe_score}"
        {recipe.dup, recipe_score}
      else
        {best, best_score}
      end
    else 
      total_rest = rest.size
      new_rest = rest.dup
      new_ingredient = new_rest.shift
      (1..(spoons_left-total_rest+1)).each do |ispoon|
        best, best_score = generate_partial(part + [{new_ingredient,ispoon}], spoons_left - ispoon, new_rest, best, best_score)
      end
      {best, best_score}
    end
  end

end
