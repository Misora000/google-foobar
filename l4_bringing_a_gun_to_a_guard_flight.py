'''
Bringing a Gun to a Guard Fight
===============================

Uh-oh - you've been cornered by one of Commander Lambdas elite guards! Fortunately, you grabbed a beam weapon from an abandoned guard post while you were running through the station, so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the elite guard: its beams reflect off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know that if a beam hits a corner, it will bounce back in exactly the same direction. And of course, if the beam hits either you or the guard, it will stop immediately (albeit painfully). 

Write a function solution(dimensions, your_position, guard_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the guard's x and y coordinates in the room, and returns an integer of the number of distinct directions that you can fire to hit the elite guard, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite guard are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000.

For example, if you and the elite guard were positioned in a room with dimensions [3, 2], your_position [1, 1], guard_position [2, 1], and a maximum shot distance of 4, you could shoot in seven different directions to hit the elite guard (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite guard with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting the elite guard with a total shot distance of sqrt(5).

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
Solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
Solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9

-- Python cases --
Input:
solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9

Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
'''


def solution(dimensions, your_position, guard_position, distance):
    # Your code here
    w, h = dimensions
    sx, sy = your_position
    dx, dy = guard_position

    # direct shot is always the shortest.
    if (dx-sx)**2 + (dy-sy)**2 > distance**2:
        return 0

    # solutions list records the slope and direction of each shooting.
    sols = {}
    sols[slope((dx, dy), (sx, sy))] = True

    # record the mirrors of self.
    self_pos = {}
    for (x, y) in [(0, 0), (w, 0), (0, h), (w, h)]:
        self_pos[slope((x, y), your_position)] = (x-sx)**2 + (y-sy)**2

    # iterate the 1st quadrant and get the mirrors of other qaudrants at the
    # same time so that can get the points in short-to-long distance order.
    for i in range(0, 10000):
        _sols = len(sols)
        for j in range(0, 10000):
            m = get_mirrors(i, j, dimensions, guard_position)
            s = get_mirrors(i, j, dimensions, your_position)
            if j != 0:
                # the mirrors caused by x-axis
                m += get_mirrors(i, -1*j, dimensions, guard_position)
                s += get_mirrors(i, -1*j, dimensions, your_position)
            if i != 0:
                # the mirrors caused by y-axis
                m += get_mirrors(-1*i, j, dimensions, guard_position)
                s += get_mirrors(-1*i, j, dimensions, your_position)
            if i != 0 and j != 0:
                # the mirrors caused by (0,0)
                m += get_mirrors(-1*i, -1*j, dimensions, guard_position)
                s += get_mirrors(-1*i, -1*j, dimensions, your_position)

            # record the mirrors of self.
            for (x, y) in s:
                vector = slope((x, y), your_position)
                if vector not in s or self_pos[vector] > (x-sx)**2 + (y-sy)**2:
                    self_pos[vector] = (x-sx)**2 + (y-sy)**2

            count = 0
            for (x, y) in m:
                if (x, y) == (dx, dy):
                    # only the real position of the guard doesn't behind a
                    # wall so that consider it as a specail case and handle
                    # it individual at the begining of this function.
                    continue
                if (x-sx)**2 + (y-sy)**2 > distance**2:
                    continue
                count += 1
                if sx == x or sy == y:
                    # vertical against the wall
                    continue
                if hit_self(self_pos, your_position, (x, y)):
                    continue

                # records the slope and direction of each shooting.
                vector = slope((x, y), (sx, sy))
                if vector not in sols:
                    sols[vector] = True

            # no more new available solution find.
            # no need to increase j (y-axis).
            if count == 0:
                break

        # no more new available solution find. no need to increase i (x-axis).
        if len(sols) == _sols:
            break

    return len(sols)


# get_mirrors return 2x2=4 rooms which were fully mirrored witch each other.
#
#  +------------------+----------------------+
#  | 2iW+x, 2(j+1)H-y | 2(i+1)W-x, 2(j+1)H-y |
#  +------------------+----------------------+
#  | 2iW+x, 2jH+y     | 2(i+1)W-x, 2jH+y     |
#  +------------------+----------------------+   dimension = W * H
#
def get_mirrors(i, j, dimensions, pos):
    w, h = dimensions
    x, y = pos
    return [
        (2*i*w+x, 2*j*h+y),
        (2*i*w+x, 2*(j+1)*h-y),
        (2*(i+1)*w-x, 2*j*h+y),
        (2*(i+1)*w-x, 2*(j+1)*h-y),
    ]


# hit_self avoids the path via a corner or the mirrors of self
def hit_self(self_pos, src, dst):
    sx, sy = src
    dx, dy = dst
    vector = slope((dx, dy), (sx, sy))
    if vector in self_pos and self_pos[vector] < (dx-sx)**2 + (dy-sy)**2:
        return True
    return False


# slope returns (slope, direction)
def slope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 or y1 == y2:
        return (0, False)
    return (float(y1-y2)/(x1-x2), x1-x2 > 0)


# print(solution([3, 2], [1, 1], [2, 1], 4))
print(solution([3, 2], [1, 1], [2, 1], 7))
# print(solution([2, 3], [1, 1], [1, 2], 4))
# print(solution([3, 4], [1, 2], [2, 1], 7))
# print(solution([4, 4], [2, 2], [3, 1], 6))
# print(solution([300, 275], [150, 150], [185, 100], 500))
# print(solution([3, 4], [1, 1], [2, 2], 500))
