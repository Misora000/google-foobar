def solution(l):
    # Your code here
    quick_sort(l, 0, len(l)-1)
    return l


def quick_sort(l, head, tail):
    i = head
    j = tail
    if i >= j:
        return

    x = l[head]
    while i < j:
        while less_than(x, l[j]) and i < j:
            j -= 1
        l[i], l[j] = l[j], l[i]

        while less_than(l[i], x) and i < j:
            i += 1
        l[i], l[j] = l[j], l[i]

    quick_sort(l, head, j-1)
    quick_sort(l, j+1, tail)
    return


def less_than(s1, s2):
    n1 = s1.split('.')
    n2 = s2.split('.')

    for i in range(0, 3):
        # padding zero if not exists
        if i+1 > len(n1):
            c1 = '0'
        else:
            c1 = n1[i]

        if i+1 > len(n2):
            c2 = '0'
        else:
            c2 = n2[i]

        # different length can compare the length directly
        # ex: 33 v.s. 3
        if len(c1) != len(c2):
            return len(c1) < len(c2)

        # same length needs to covert to int
        if c1 != c2:
            return int(c1) < int(c2)

    # same value, compare the raw string length
    # ex: 3.0 v.s. 3.0.0
    return len(s1) < len(s2)


def selection_sort(l):
    for i in range(len(l)-1):
        mini = i
        for j in range(i+1, len(l)):
            if less_than(l[j], l[mini]):
                mini = j
        if i != mini:
            l[mini], l[i] = l[i], l[mini]

    return l


def str2int(e):
    magic = [100000, 1000, 10]
    output = 0
    slice = e.split('.')
    for i in range(len(slice)):
        # print(i, slice[i], magic[i])
        output += int(slice[i]) * magic[i]
    # print(e, "-->", output)
    return output + len(slice)


# print(compare('1.1398674068036832000000000000000000000000000000009', '2.4'))

print(solution(["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]))
print(solution(["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"]))
