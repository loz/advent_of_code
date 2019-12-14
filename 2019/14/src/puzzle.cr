class Puzzle

  property ingredients = [] of Tuple(String, UInt64)

  property recipes = {} of String => Tuple(UInt64,Array(Tuple(String,UInt64)))

  def process(str)
    str.each_line do |line|
      process_line(line)
    end
  end

  def savings(wastes)
    saving = 0.to_u64
    leftover = Hash(String,UInt64).new(0.to_u64)

    wastes.each do |ing, amt|
      recipe = @recipes[ing]
      rneeds, gives = recipe
      if amt >= rneeds
        save = (amt.to_u64)//rneeds.to_u64
        rem = (amt.to_u64) % rneeds.to_u64
        gives.each do |item|
          ig, val = item
          if ig == "ORE"
            saving += save * val.to_u64
          else
            leftover[ig] += save * val.to_u64
          end
        end
        if rem != 0
          #"REMAINDER: #{rem}x#{ing}"
          leftover[ing] += rem
        end
        #p "#{ing}:#{amt} => #{rneeds} -> #{gives}"
      else
        leftover[ing] += amt
      end
    end
    if saving != 0
      save, left = savings(leftover)
      return {saving + save, left}
    else
      return {0.to_u64, leftover}
    end
  end

  def process_line(line)
    source = [] of Tuple(String,UInt64)
    ins, out = line.split(" => ")
    ins.split(", ").each do |ins|
      in_n, in_i = ins.split(" ")
      source << {in_i, in_n.to_u64}
    end
    out_n, out_i = out.split(" ")
    @recipes[out_i] = {out_n.to_u64,source}
  end

  def max_for(total_ore, givenwaste = {} of String => UInt64)
    res, waste = refine(1)
    cost = res["ORE"]
    save, waste = savings(waste)
    efficient = cost - save
    created = total_ore//efficient
    left = total_ore % efficient

    #now created , made created * waste 
    allwaste = Hash(String,UInt64).new(0.to_u64)
    givenwaste.each {|ing, amt| allwaste[ing] = amt}
    waste.each do |ing, amt|
      allwaste[ing] += amt * created
    end
    
    bonus, bwaste = savings(allwaste)
    remaining = left + bonus
    bonus, bwaste = savings(bwaste)
    remaining += bonus
    #p created, left, allwaste
    #p savings(allwaste)
    if remaining < efficient
      #p "REMAINING: #{remaining}"
      return {created, bwaste, remaining}
    else
      rmax, rwaste, rrem = max_for(remaining, bwaste)
      {rmax + created, rwaste, rrem}
    end
  end

  def result
    res, waste = refine(1)
    save, waste = savings(waste)
    best = res["ORE"] - save
    p "BEST: #{best}"

    tril, waste, rem = max_for(1_000_000_000_000)
    puts "1Tril: #{tril}, #{rem} left over"
    puts waste
    save, waste = savings(waste)
    p save, waste
    #p refine_r({"FUEL" => 1}, waste)
  end

  def refine(nfuel)
    ingredients = {"FUEL" => nfuel}
    waste = Hash(String,UInt64).new(0.to_u64)
    refine_r(ingredients, waste)
  end

  def refine_r(ingredients, waste)
    return {ingredients, waste} if only_ore?(ingredients)
    new_ingredients = {} of String => UInt64
    ingredients.each do |name, count|
      if name == "ORE"
        new_ingredients = merge_ingredients(new_ingredients, {"ORE" => count})
      else
        recipe = @recipes[name]
        new_ingredients = merge_ingredients(new_ingredients, apply_recipe(recipe, count, name))
      end
    end
    return {new_ingredients, waste} if only_ore?(new_ingredients)
    if ingredients == new_ingredients
      new_ingredients, waste = refine_remainder(ingredients, waste)
      #return explore_refinements(ingredients, best)
      #puts "HTL: #{ingredients}"
      #raise "Not Refinable"
    end
    #puts "GEN :> #{new_ingredients}"
    return refine_r(new_ingredients, waste)
  end

  def explore_refinements(ingredients, best)
    #puts "EXPLORE REFINE OF : #{ingredients}"
    ingredients.each do |ing,have|
        next if ing == "ORE"
        possible = ingredients.dup
        recipe = @recipes[ing]
        needed, gives = recipe
        if gives.first[0] == "ORE" 
          takes = gives.first[1]
          #Possible option is to refine into ORE
          possible["ORE"] = 0 unless possible["ORE"]?
          possible.delete ing
          if have % needed == 0
            possible["ORE"] += (have//needed) * takes
          else #Round Up
            rounded = (have//needed) + 1
            #p "#{(have/needed)} x #{takes} ORE (->#{needed}) -> #{have} #{ing} -> #{rounded}"
            possible["ORE"] += rounded * takes
          end
        else
          #Explore other refinement
          #puts "EXPLORE OTHER"
          #puts "I:#{ing}x#{have} -> #{needed} => #{gives}"
          #??? add in remainder ??
          possible.delete ing
          possible = merge_ingredients(possible, gives)
          #p possible
          #sleep 1
        end
        #puts "POSS: #{possible}"
        #puts "=" * 50
        if only_ore?(possible) 
          result = possible
        else
          result = refine_r(possible, best)
        end
        #puts "=" * 50
        #p result
        #puts "=" * 50
        total = result["ORE"]
        #raise "Result"
        if total < best
          #puts "NEW BEST:> #{total}"
          best = total
        end
    end
    {"ORE" => best}
  end

  def refine_remainder(ingredients, waste)
    #puts "REFINING REMAINEDER"
    #new_ingredients = {} of String => Int32
    #ingredients.each do |name,count|
    #  if name == "ORE"
    #    new_ingredients = merge_ingredients(new_ingredients, {"ORE" => count})
    #  else
    #    recipe = @recipes[name]
    #    new_ingredients = merge_ingredients(new_ingredients, apply_recipe(recipe, count, name))
    #  end
    #end
    #ingredients = new_ingredients
    new_ingredients = {} of String => UInt64
    ingredients.each do |ing, have|
      if ing == "ORE" #Does not refine
        new_ingredients[ing] = have.to_u64
      else
        #print "#{ing}x#{have} =>?"
        recipe = @recipes[ing]
        needed, gives = recipe
        #print " N:#{needed} => #{gives}"
        new_ingredients[ing] = needed
        #this is waste
        waste[ing] += (needed - have)
        #puts
      end
    end
    {new_ingredients, waste}
  end

  def merge_ingredients(ingredientsa, ingredientsb)
    ingredientsb.each do |k,v|
      if ingredientsa[k]?
        ingredientsa[k] += v.to_u64
      else
        ingredientsa[k] = v.to_u64
      end
    end
    ingredientsa
  end

  def only_ore?(ingredients)
    ingredients.all? {|k,v| k == "ORE" || v == 0 }
  end

  def apply_recipe(recipe, remain, name)
    produced = {} of String => UInt64
    #puts "Apply: #{recipe} to #{remain} x #{name}"
    consume, produce = recipe
    while remain >= consume
      #print ">"
      produce.each do |compound|
        comp, compn = compound
        #return {name => remain} if !allowore && comp == "ORE" #don't breakdown ORE until end
        if produced[comp]?
          produced[comp] += compn
        else
          produced[comp] = compn
        end
      end
      remain -= consume
    end
    if remain > 0
      produced[name] = remain.to_u64 #left over
    end
    #puts "> #{produced}"
    produced
 end

end
