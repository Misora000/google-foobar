'''
Find the Access Codes
=====================

In order to destroy Commander Lambda's LAMBCHOP doomsday device, you'll need access to it. But the only door leading to the LAMBCHOP chamber is secured with a unique lock system whose number of passcodes changes daily. Commander Lambda gets a report every day that includes the locks' access codes, but only she knows how to figure out which of several lists contains the access codes. You need to find a way to determine which list contains the access codes once you're ready to go in. 

Fortunately, now that you're Commander Lambda's personal assistant, she's confided to you that she made all the access codes "lucky triples" in order to help her better find them in the lists. A "lucky triple" is a tuple (x, y, z) where x divides y and y divides z, such as (1, 2, 4). With that information, you can figure out which list contains the number of access codes that matches the number of locks on the door when you're ready to go in (for example, if there's 5 passcodes, you'd need to find a list with 5 "lucky triple" access codes).

Write a function solution(l) that takes a list of positive integers l and counts the number of "lucky triples" of (li, lj, lk) where the list indices meet the requirement i < j < k.  The length of l is between 2 and 2000 inclusive.  The elements of l are between 1 and 999999 inclusive.  The answer fits within a signed 32-bit integer. Some of the lists are purposely generated without any access codes to throw off spies, so if no triples are found, return 0. 

For example, [1, 2, 3, 4, 5, 6] has the triples: [1, 2, 4], [1, 2, 6], [1, 3, 6], making the answer 3 total.

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution([1, 1, 1])
Output:
    1

Input:
Solution.solution([1, 2, 3, 4, 5, 6])
Output:
    3

-- Python cases --
Input:
solution.solution([1, 2, 3, 4, 5, 6])
Output:
    3

Input:
solution.solution([1, 1, 1])
Output:
    1

Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
'''

'''
We expand each "who divides other" relationship in a map,
then sum the number of value > 1 and store as the last element in each row.

    0 | 1   2   3   4   5   6 | sum
    --+-----------------------+----
    1 | 1   2   3   4   5   6 |  5 <-- ignore
    2 |     1       2       3 |  2 <-- sum this
    3 |         1           2 |  1 <-- sum this
    4 |             1         |  0
    5 |                 1     |  0
    6 |                     1 |  0

we can easily figure that the count of [1, x, x] if sum[1]+sum[2]+sum[n]=3
and the count of [2, x, x] is sum[4]+sum[6]=0

so the process is iterate each row, if the value > 1, then add the sum

psuedo code:

count = 0
for i = 0 to len(l)-1
    for  j = i+1 to len(l-1)
        if l[i, j] != 0
            count += sum[j]

Beware in my implementation, remove the 1st row & columne from the above
example because that are not necessary during iterating the map, it can
use the input array:l directly.

'''


def solution(l):
    # Your code here
    count = 0
    m = gen_map(l)
    for i in range(len(m)-1):
        for j in range(len(m[i])-1):
            if m[i][j] == 1:
                count += m[j][-1]

    return count


'''
Gen a map like this:
    [0, 1, 1, 1, 1, 1, 5]
    [0, 0, 0, 1, 0, 1, 2]
    [0, 0, 0, 0, 0, 1, 1]
    [0, 0, 0, 0, 0, 0, 0]
    [0, 0, 0, 0, 0, 0, 0]
'''


def gen_map(l):
    m = []
    for i in range(len(l)):
        row = []
        count = 0
        for j in range(i+1):
            row.append(0)

        for j in range(i+1, len(l)):
            if l[j] % l[i] == 0:
                count += 1
                row.append(1)
            else:
                row.append(0)

        row.append(count)
        m.append(row)

    return m


print(solution([1, 2, 3, 4, 5, 6]))
print(solution([1, 1, 1]))
