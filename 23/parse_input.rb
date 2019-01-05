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


def explore_children(bots, bbox, cur_depth = 0)
  divisions = bots.subdivide(bbox)
  options = divisions.map do |poss_bbox|
    in_box = bots.in_bbox(poss_bbox)
    #puts (" "*(cur_depth+1)) + "Child: #{poss_bbox} -> #{in_box.count}"
    [poss_bbox, in_box.count]
  end
  options.sort {|b1, b2| b2[1] <=> b1[1]}
end

def explore(bots, bbox, leaves, max_depth=3, cur_depth = 0)
  #puts (" "*cur_depth) + "Exploring #{bbox.inspect}"
  bests = explore_children(bots, bbox, cur_depth)

  max = bests.min {|r1, r2| r2[1] <=> r1[1]}
  bests.reject! {|r| r[1] != max[1]}

  #bests.reject! {|b| b[1] == 0 }
  bests.each do |b|
    cbox, ccount = b
    #puts "|> #{cbox} (#{ccount})" if depth == 0
    if ccount > 1
      if max_depth != 0
        explore(bots, cbox, leaves, max_depth-1, cur_depth + 1)
      else
        leaves << b
      end
    end
  end
end

def explore_best(bots, bbox, depth, n)
  #puts "Exploring #{bbox.inspect}"
  bests = explore_children(bots, bbox)
  bests.sort! {|b1, b2| b2[1] <=> b1[1] }
  bests = bests[0,n]
  all = []
  all = bests if depth == 0
  bests.each do |b|
    cbox, ccount = b
    #puts "|> #{cbox} (#{ccount})" if depth == 0
    if depth != 0
      results = explore_best(bots, cbox, depth-1, n)
      all += results
    end
  end
  return all
end

bbox = bots.bounding_box

#First run: [[37896166, 19919903, 44042359, 49469955, 26704177, 50819731], 955]
#bbox = [37896166, 19919903, 44042359, 49469955, 26704177, 50819731]

depth = 17

#Test one path of depth@17
bbox = [35364400, 23312041, 47646148, 35365812, 23312869, 47646975]
depth = 6

results = []

explore(bots, bbox, results, depth)
max= results.min {|r1, r2| r2[1] <=> r1[1]}
p results.count
#results.each {|r| p r }
puts "MAX: #{max}"
puts "%s @ MAX" % results.count {|r| r[1] == max[1]}
#results.each {|r|  puts r[0].inspect if r[1] == max[1]}
x1,y1,z1, x2,y2,z2 = max[0]
puts "Size at Depth #{depth}: #{x2-x1},#{y2-y1},#{z2-z1}"
puts "Any Point == Corner?"
x,y,z = max[0]
nbots = bots.nearest_to([x,y,z])
puts "Bots: #{nbots.count}"
puts "Distance -> 0,0,0 -> #{bots.distance([x,y,z],[0,0,0])}"


#results.each do |res|
#  bbox, _ = res
#  x, y, z = bbox
#  pos = [x,y,z]
#  puts "%s -> %s" % [pos, bots.nearest_to(pos).count]
#end

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

=begin
best = [31792800, 27128194, 50819731, 31792800, 27128194, 50819731]
puts "Total BBox"
puts bots.in_bbox(best).count
puts "Total BBox2"
puts bots.in_bbox2(best).count

exit 1
=end

#[[37584109, 19736982, 47431045, 37584286, 19737086, 47431148], 977]
#218504 @ MAX

#bbox = [37584109, 19736982, 47431045, 37584286, 19737086, 47431148]
#coord = centre = bots.centre(bbox)
#nearest = bots.nearest_to(coord)
#p nearest.count
#exit 1

#results = explore_best(bots, bbox, 1, 2)

=begin
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



=end
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
