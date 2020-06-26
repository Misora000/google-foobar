'''
Running with Bunnies
====================

You and your rescued bunny prisoners need to get out of this collapsing death trap of a space station - and fast! Unfortunately, some of the bunnies have been weakened by their long imprisonment and can't run very fast. Their friends are trying to help them, but this escape would go a lot faster if you also pitched in. The defensive bulkhead doors have begun to close, and if you don't make it through in time, you'll be trapped! You need to grab as many bunnies as you can and get through the bulkheads before they close. 

The time it takes to move from your starting point to all of the bunnies and to the bulkhead will be given to you in a square matrix of integers. Each row will tell you the time it takes to get to the start, first bunny, second bunny, ..., last bunny, and the bulkhead in that order. The order of the rows follows the same pattern (start, each bunny, bulkhead). The bunnies can jump into your arms, so picking them up is instantaneous, and arriving at the bulkhead at the same time as it seals still allows for a successful, if dramatic, escape. (Don't worry, any bunnies you don't pick up will be able to escape with you since they no longer have to carry the ones you did pick up.) You can revisit different spots if you wish, and moving to the bulkhead doesn't mean you have to immediately leave - you can move to and from the bulkhead to pick up additional bunnies if time permits.

In addition to spending time traveling between bunnies, some paths interact with the space station's security checkpoints and add time back to the clock. Adding time to the clock will delay the closing of the bulkhead doors, and if the time goes back up to 0 or a positive number after the doors have already closed, it triggers the bulkhead to reopen. Therefore, it might be possible to walk in a circle and keep gaining time: that is, each time a path is traversed, the same amount of time is used or added.

Write a function of the form solution(times, time_limit) to calculate the most bunnies you can pick up and which bunnies they are, while still escaping through the bulkhead before the doors close for good. If there are multiple sets of bunnies of the same size, return the set of bunnies with the lowest prisoner IDs (as indexes) in sorted order. The bunnies are represented as a sorted list by prisoner ID, with the first bunny being 0. There are at most 5 bunnies, and time_limit is a non-negative integer that is at most 999.

For instance, in the case of
[
  [0, 2, 2, 2, -1],  # 0 = Start
  [9, 0, 2, 2, -1],  # 1 = Bunny 0
  [9, 3, 0, 2, -1],  # 2 = Bunny 1
  [9, 3, 2, 0, -1],  # 3 = Bunny 2
  [9, 3, 2, 2,  0],  # 4 = Bulkhead
]
and a time limit of 1, the five inner array rows designate the starting point, bunny 0, bunny 1, bunny 2, and the bulkhead door exit respectively. You could take the path:

Start End Delta Time Status
    -   0     -    1 Bulkhead initially open
    0   4    -1    2
    4   2     2    0
    2   4    -1    1
    4   3     2   -1 Bulkhead closes
    3   4    -1    0 Bulkhead reopens; you and the bunnies exit

With this solution, you would pick up bunnies 1 and 2. This is the best combination for this space station hallway, so the answer is [1, 2].

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
Solution.solution({{0, 1, 1, 1, 1}, {1, 0, 1, 1, 1}, {1, 1, 0, 1, 1}, {1, 1, 1, 0, 1}, {1, 1, 1, 1, 0}}, 3)
Output:
    [0, 1]

Input:
Solution.solution({{0, 2, 2, 2, -1}, {9, 0, 2, 2, -1}, {9, 3, 0, 2, -1}, {9, 3, 2, 0, -1}, {9, 3, 2, 2, 0}}, 1)
Output:
    [1, 2]

-- Python cases --
Input:
solution.solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)
Output:
    [1, 2]

Input:
solution.solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)
Output:
    [0, 1]

Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
'''


def solution(times, times_limit):
    # Your code here
    sssp = gen_shortest_path_graph(times)

    # if a negative cycle exists, we can earn the time as much as possible
    # so that we can grab all bunnies.
    if has_negative_cycle(sssp) == True:
        return [b-1 for b in range(1, len(times)-1)]

    # list all possible route from source (0, 0) to destination (l-1, l-1)
    # try visiting all bunnies first. then try visiting n-1 bunnies if exceeds
    # the time limit. and so on until doesn'y visit any bunnies.
    for r in list_all_route(sssp):
        total_length = 0
        for i in range(1, len(r)):
            # path [0, 2, 4, 3] = [(0->2), (2->4), (4->3)]
            total_length += sssp[r[i-1]][r[i]]
        if total_length <= times_limit:
            ans = [r[b]-1 for b in range(1, len(r)-1)]
            ans.sort()
            return ans
    return []


def gen_shortest_path_graph(length):
    # use bellman-ford to find each shortest path between every nodes.
    for n in range(len(length)):
        for i in range(len(length)):
            for j in range(len(length)):
                length_via_k = length[i][n] + length[n][j]
                if length[i][j] > length_via_k:
                    length[i][j] = length_via_k
    return length


def has_negative_cycle(sssp):
    # in single source shortest path graph, a negative cycle exists if the
    # length i -> i  is less than zero.
    for i in range(len(sssp)):
        if sssp[i][i] < 0:
            return True
    return False


def list_all_route(sssp):
    bunnies = [b for b in range(1, len(sssp)-1)]
    sol = []
    # dfs([0, 1, 2], [], 2, sol)
    for l in range(len(bunnies)):
        dfs(bunnies, [], len(bunnies)-l, sol)

    route = []
    for s in sol:
        full_path = [0] + s + [len(sssp)-1]
        route.append(full_path)

    return route


def dfs(pool, stack, max_size, sol):
    # find all permutations by dfs.
    if len(pool) == 0:
        return

    for i in range(len(pool)):
        new_stack = stack[:]
        new_stack.append(pool[i])
        if len(new_stack) >= max_size:
            sol.append(new_stack)
            continue

        new_pool = pool[:]
        new_pool.pop(i)
        dfs(new_pool, new_stack, max_size, sol)
    return


print(solution([
    [0, 2, 2, 2, -1],
    [9, 0, 2, 2, -1],
    [9, 3, 0, 2, -1],
    [9, 3, 2, 0, -1],
    [9, 3, 2, 2, 0],
], 1))
print(solution([
    [0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0],
], 3))
