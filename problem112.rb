def solve112(target_proportion)
    bouncy_proportion = 0
    total_bouncy = 0
    num = 0
    while bouncy_proportion < target_proportion
        num += 1
        increasing, decreasing = true, true
        current = num
        last = current % 10
        while current > 0
            current, digit = current.div(10), current % 10
            if digit > last
                #puts "decreasing from left to right#{digit} > #{last}"
                increasing = false
            elsif last > digit
                #puts "increasing left to right #{digit} < #{last}"
                decreasing = false
            end
            last = digit
        end

        if (!increasing && !decreasing)# || (increasing && decreasing)
            total_bouncy += 1
            bouncy_proportion = 1.0*total_bouncy/num
            #puts "#{num} bouncy #{bouncy_proportion}"
        end
    end
    puts target_proportion, num
end

def bouncy?(current)
        increasing, decreasing = true, true
        last = current % 10
        while current > 0
            current, digit = current.div(10), current % 10
            if digit > last
                increasing = false
            elsif last > digit
                decreasing = false
            end
            last = digit
        end

        if (!increasing && !decreasing)
            return true
        else
            return false
end
=begin
    for n in 0..max_num
        n.to_s.split.each do |digit|
            puts digit
        end
    end
=end


solve112(0.99)
