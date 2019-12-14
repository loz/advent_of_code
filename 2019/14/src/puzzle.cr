class Puzzle

  property ingredients = [] of Tuple(String, Int32)

  property recipes = {} of String => Tuple(Int32,Array(Tuple(String,Int32)))

  def process(str)
    str.each_line do |line|
      process_line(line)
    end
  end

  def process_line(line)
    source = [] of Tuple(String,Int32)
    ins, out = line.split(" => ")
    ins.split(", ").each do |ins|
      in_n, in_i = ins.split(" ")
      source << {in_i, in_n.to_i}
    end
    out_n, out_i = out.split(" ")
    @recipes[out_i] = {out_n.to_i,source}
  end

  def result
    res = refine(1)
    p res
  end

  def refine(nfuel)
    ingredients = {"FUEL" => nfuel}
    refine_r(ingredients)
  end

  def refine_r(ingredients)
    new_ingredients = {} of String => Int32
    ingredients.each do |name,count|
      if name == "ORE"
        new_ingredients = merge_ingredients(new_ingredients, {"ORE" => count})
      else
        recipe = @recipes[name]
        new_ingredients = merge_ingredients(new_ingredients, apply_recipe(recipe, count, name))
      end
    end
    if ingredients == new_ingredients
      new_ingredients = refine_remainder(ingredients)
    end
    if ingredients == new_ingredients
      raise "Unable To Refine!"
    end
    if only_ore?(new_ingredients)
      return new_ingredients
    else
      puts "GEN :> #{new_ingredients}"
      return refine_r(new_ingredients)
    end
  end

  def refine_remainder(ingredients)
    #puts "REFINING REMAINEDER"
    new_ingredients = {} of String => Int32
    ingredients.each do |k, v|
      if @recipes[k]?
        recipe = @recipes[k]
        needed, gives = recipe
        new_ingredients[k] = needed
      else #ORE
        new_ingredients[k] = v
      end
    end
    new_ingredients
  end

  def merge_ingredients(ingredientsa, ingredientsb)
    ingredientsb.each do |k,v|
      if ingredientsa[k]?
        ingredientsa[k] += v
      else
        ingredientsa[k] = v
      end
    end
    ingredientsa
  end

  def only_ore?(ingredients)
    ingredients.all? {|k,v| k == "ORE" || v == 0 }
  end

  def apply_recipe(recipe, remain, name)
    produced = {} of String => Int32
    #puts "Apply: #{recipe} to #{remain} x #{name}"
    consume, produce = recipe
    while remain >= consume
      #print ">"
      produce.each do |compound|
        comp, compn = compound
        if produced[comp]?
          produced[comp] += compn
        else
          produced[comp] = compn
        end
      end
      remain -= consume
    end
    if remain > 0
      produced[name] = remain
    end
    #print "> #{produced}"
    produced
  end

end
