def apply(a, b, decksize, loops, position):
    def combine(a1, b1, a2, b2):
        print("Combining", a1, b1, a2, b2)
        b3 = (a1 * b2 + b1) % decksize
        a3 = (a1 * a2) % decksize
        return a3, b3

    finala, finalb = a, b
    totalCount = 1
    while totalCount < loops:
        aa, bb = a, b
        count = 1

        while 2*count <= loops - totalCount:
            aa, bb = combine(aa, bb, aa, bb)
            count *= 2

        finala, finalb = combine(aa, bb, finala, finalb)
        totalCount += count

    return (finala * position + finalb) % decksize

def solution(inp, decksize, loops, position):
    a, b = 1, 0

    for line in inp.splitlines():
        move, n = line.split(' ')[-2:]
        if move == "new":
            a = (-a) % decksize
            b = (-b - 1) % decksize
        elif move == "cut":
            b = (b - int(n)) % decksize
        elif move == "increment":
            a = (a * int(n)) % decksize
            b = (b * int(n)) % decksize

    print("a 1 -> ", a)  #What happens to 1?
    print("b 0 -> ", b)  #What happens to 0?
    return apply(a, b, decksize, loops, position)

print("Part 1:", solution(open("input").read(), 10007, 1, 2019))
print("Part 2:", solution(open("input").read(), 119315717514047, (119315717514047-1 - 101741582076661), 2020))
