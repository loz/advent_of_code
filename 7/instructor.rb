class Instructor
  def initialize
    @completion = []
  end

  def process(steps)
    @deps = Hash.new { |h,k| h[k] = [] }

    steps.each_line do |line|
      step, dep = parse_step(line)
      @deps[dep] #force deps with no deps to be present
      @deps[step] << dep
      #puts "%s <- %s" % [step, dep]
    end
  end

  def complete(step)
    @completion << step
  end

  def dependant(step)
    @deps[step]
  end

  def perform_with_workers(worker_count, base_time)
    active = []
    workers = Array.new(worker_count, :inactive)

    steps = available_steps
    free_workers = workers
    timer = 0
    finished = false

    while !finished
      #Do Work
      workers.map! do |worker|
        if worker == :inactive
          worker
        else
          #puts "Work: #{worker.inspect}"
          left = worker[:remaining] -= 1
          if left == 0
            active.delete worker[:task]
            complete worker[:task]
            steps = available_steps
            :inactive  #return to pool
          else
            worker
          end
        end
      end

      #Resort workers so :inactive is at the end
      workers = workers.sort do |w1, w2| 
        if w1 == :inactive
          1
        else
          -1
        end
      end

      steps = steps - active
      steps.sort.each do |step|
        free_workers = available_workers(workers)
        #Assign work
        break if free_workers.empty?
        workers.pop
        work = {task: step, remaining: step_time(base_time, step)}
        active << step
        workers.unshift work
      end

      #complete(steps.sort.first)
      puts "#{timer} Complete: #{@completion}, Active: #{active}"
      #puts "    Workers: #{workers.inspect}"

      free_workers = available_workers(workers)
      if steps.empty? && (free_workers.count == worker_count)
        finished = true
      else
        timer += 1
      end
    end
    
    timer
  end

  def perform_steps
    steps = available_steps
    while !steps.empty?
      complete(steps.sort.first)
      steps = available_steps
    end
  end

  def order
    @completion.join ''
  end

  def available_steps
    avail = @deps.select do |step, deps|
      #puts "%s => %s" % [step, deps.inspect]
      remaining = deps - @completion
      remaining == []
    end
    avail.keys - @completion
  end

  private

  def available_workers(workerlist)
    workerlist.select { |w| w == :inactive }
  end

  def step_time(base_time, step)
    base_time + 1 + step.ord - 'A'.ord
  end
  
  def parse_step(line)
    matches = line.match /Step (.) must be finished before step (.) can begin/
    [matches[2],matches[1]]
  end
end
