#ProjectEuler.net Problem 112
#Sam Heinith
#August 10, 2012


=begin Problem Statement
Working from left-to-right if no digit is exceeded by the digit to its left
it is called an increasing number; for example, 134468.  Similarly if no
digit is exceeded by the digit to its right it is called a decreasing number;
for example, 66420.  We shall call a positive integer that is neither
increasing nor decreasing a "bouncy" number; for example, 155349.  Clearly
there cannot be any bouncy numbers below one-hundred, but just over half of
the numbers below one-thousand (525) are bouncy. In fact, the least number
for which the proportion of bouncy numbers first reaches 50% is 538.

Surprisingly, bouncy numbers become more and more common and by the time
we reach 21780 the proportion of bouncy numbers is equal to 90%.  Find the
least number for which the proportion of bouncy numbers is exactly 99%.
=end


=begin Notes
This problem involved testing each number for the bouncy property.  This was
done by comparing each digit of a number to the digit to its right.  The 
number is split into digits by using integer division and modulo.  This
process is repeated for all the digits in the number and used to test whether
the digits are increasing or decreasing.  If they are neither increasing nor
decreasing the number is bouncy.  The number of bouncy numbers is tracked and
used to find the bouncy proportion.
=end

def solve112(target_proportion)
    bouncy_proportion = 0
    total_bouncy = 0
    num = 0
    while bouncy_proportion < target_proportion
        num += 1
        if bouncy?(num)
            total_bouncy += 1
            bouncy_proportion = 1.0*total_bouncy/num
        end
    end
    puts target_proportion, num
end

def bouncy?(num)
        increasing, decreasing = true, true
        right_digit = num % 10
        while num > 0
            num, left_digit = num.div(10), num % 10
            if left_digit > right_digit
                increasing = false
            elsif right_digit > left_digit
                decreasing = false
            end
            right_digit = left_digit
        end
        return (!increasing && !decreasing)
end

solve112(0.99)

