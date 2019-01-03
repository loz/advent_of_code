require_relative './nanobots'

#bot_text = File.open("input.example") do |f|
bot_text = File.open("input") do |f|
  f.read
end
bots = Nanobots.new 
bot_text.each_line do |line|
  bots.add(line)
end
largest = bots.greatest_range
puts "Wideest Range: %s" % largest.pos.inspect

ranged = bots.nearest(largest)
puts "Ranged Count: %s" % ranged.count

=begin
def explore_children(bots, bbox, parent)
  divisions = bots.subdivide(bbox)
  options = divisions.map do |poss_bbox|
    poss_pos = bots.centre(poss_bbox)
    ranged = bots.nearest_to(poss_pos)
    poss = ranged.count
    [poss, poss_pos, poss_bbox, parent]
  end
  options
end

def explore(bots, bbox, depth=3)
  #puts "Exploring #{bbox.inspect}"
  all_bests = [[0, [0,0], bbox]]
  (depth+1).times do |d|
    new_bests = []
    all_bests.each do |option|
      _, _, bbox  = option
      #puts "@#{d}"
      bests = explore_children(bots, bbox, option)
      #bests.each do |b|
      #  puts "|> #{b.inspect}"
      #end
      new_bests += bests
    end
    #new_bests.sort! do |o1, o2|
    #  o2[0] <=> o1[0]
    #end
    #all_bests = new_bests[0,20+(20*depth)]
    all_bests = new_bests.uniq
  end
  all_bests.sort! do |o1, o2|
      o2[0] <=> o1[0]
  end
  all_bests[0,10]
end
=end

def explore_children(bots, bbox)
  divisions = bots.subdivide(bbox)
  options = divisions.map do |poss_bbox|
    in_box = bots.in_bbox(poss_bbox)
    [poss_bbox, in_box.count]
  end
  options.sort {|b1, b2| b2[1] <=> b1[1]}
end

def explore(bots, bbox, depth=3)
  puts "Exploring #{bbox.inspect}"
  bests = explore_children(bots, bbox)
  bests.reject! {|b| b[1] == 0 }
  bests.each do |b|
    cbox, ccount = b
    puts "|> #{cbox} (#{ccount})"
    if depth != 0
      explore(bots, cbox, depth-1)
    end
  end
  if depth == 0
    return bests
  end
  #if depth != 0
  #  explore(bots, bests.first[0], depth-1)
  #end
end

bbox = bots.bounding_box
=begin
p "Average Spot:"
p avg = bots.weighted_average
nearest = bots.nearest_to(avg)
p nearest.count
10.times do
  p avg = bots.weighted_average(nearest)
  nearest = bots.nearest_to(avg)
  p nearest.count
end
exit 1
=end
=begin
possible = bots.bots.map {|b| b.pos }
possible = possible.map do |loc|
  nearest = bots.nearest_to(loc)
  [loc, nearest.count, nearest]
end
3.times do 
  puts "Mapping..."
  new_set = possible.map do |option|
    loc, count, nearest = option
    avg = bots.weighted_average(nearest)
    nearest_a = bots.nearest_to(avg)
    #puts "#{loc} -> #{nearest.count} -> #{avg}-> #{nearest_a.count}"
    [avg, nearest_a.count,nearest_a]
  end
  new_set.sort! {|p1, p2| p2[1] <=> p1[1]}
  new_set[0,10].each {|s| puts "#{s[0]}, #{s[1]}" }
  possible = new_set
end
exit 1
=end

explore(bots, bbox, 4)

best1 = [32583975, 19654890, 50832967]
best2 = [32583976, 19654891, 50832968]
total = bots.nearest_to(best1) + bots.nearest_to(best2)
total.uniq
puts total.count

best = [31792800, 27128194, 50819731, 31792800, 27128194, 50819731]
centre = bots.centre(best)
total = bots.nearest_to(centre)
puts total.count


exit 1
2.times do |depth|
  bests = explore(bots, bbox, depth)
  bests.each do |best|
    score, pos, bbox = best
    puts "Best Score: #{pos}} #{score} @ #{depth}"
  end
end


#best = [31792800, 27128194, 50819731, 31792800, 27128194, 50819731]
#centre = bots.centre(best)




