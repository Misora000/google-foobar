def solution(map):
    # Your code here

    min_track = [[[65535]*len(map[0]) for _ in range(len(map))],
                 [[65535]*len(map[0]) for _ in range(len(map))]]
    track = []

    _, min_length = move(map, track, min_track, 0, 0, 65535, 0, 0)
    return min_length


def move(map, track, min_track, wall, curr_length, min_length, x, y):
    # is out of map
    if x < 0 or y < 0 or x > len(map)-1 or y > len(map[0])-1:
        return False, curr_length

    curr_length += 1
    # more than the best solution before, no need to walk down
    # if curr_length >= min_length:
    #     print('more than best sol')
    #     return False, curr_length

    # more than one of the previous case, no need to walk down
    # if curr_length > min_track[wall][x][y]:
    #     return False, curr_length
    # min_track[wall][x][y] = curr_length

    # reach the escape
    if x == len(map)-1 and y == len(map[0])-1:
        return True, curr_length

    # is loop
    for i in range(len(track)):
        if (x, y) == track[i]:
            return False, curr_length

    # is wall
    if map[x][y] == 1:
        wall += 1

    # through double wall, failed
    if wall > 1:
        return False, curr_length

    track.append((x, y))

    back_from_goal = False

    # down, right, up, left
    next_way = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]

    for i in range(len(next_way)):
        next_x, next_y = next_way[i]
        goal, length = move(map, track, min_track, wall,
                            curr_length, min_length, next_x, next_y)
        if goal == True:
            back_from_goal = True
            if length == len(map)+len(map[0])-1:
                # is the best solution (minimal path length)
                return True, length
            if length < min_length:
                min_length = length

    track.pop()
    return back_from_goal, min_length


# print(solution([
#     [0, 1, 1, 0],
#     [0, 0, 0, 1],
#     [1, 1, 0, 0],
#     [1, 1, 1, 0],
# ]))
# print(solution([
#     [0, 0, 0, 0],
#     [0, 0, 1, 0],
#     [1, 1, 0, 0],
#     [1, 0, 0, 1],
# ]))
# print(solution([
#     [0, 1, 0, 0],
#     [0, 0, 1, 0],
# ]))
# print(solution([
#     [0, 1],
#     [0, 0],
#     [0, 0],
# ]))
# print(solution([
#     [0, 1, 1, 0, 0, 0],
#     [0, 1, 1, 0, 0, 0],
#     [0, 1, 1, 0, 1, 0],
#     [0, 0, 0, 1, 1, 0],
#     [1, 1, 1, 1, 1, 0],
#     [1, 1, 1, 1, 1, 0],
# ]))
# print(solution([
#     [0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0, 0],
#     [0, 1, 1, 1, 1, 1],
#     [0, 1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0],
# ]))
# print(solution([
#     [0, 1, 1, 0, 0, 0, 0],
#     [0, 1, 1, 0, 1, 1, 0],
#     [0, 1, 1, 0, 1, 1, 0],
#     [0, 1, 1, 0, 1, 1, 0],
#     [0, 1, 1, 0, 1, 1, 0],
#     [0, 1, 1, 0, 1, 1, 0],
#     [0, 0, 0, 0, 1, 1, 0],
# ]))
# print(solution([
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# ]))
print(solution([
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 1, 0],
]))
