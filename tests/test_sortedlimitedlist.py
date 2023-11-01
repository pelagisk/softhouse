from softhouse.winners import SortedLimitedList


def test_insertion_order():
    l = SortedLimitedList(n=3, key=(lambda line: line[1]))
    l.insert((0, 1))
    assert(l._list == [(0, 1)])
    l.insert((0, 9))
    assert(l._list == [(0, 9), (0, 1)])
    l.insert((0, 4))
    assert(l._list == [(0, 9), (0, 4), (0, 1)])
 
    l.insert((0, 7))
    assert(l._list == [(0, 9), (0, 7), (0, 4)])

def test_number_of_elements():

    for n in range(3, 7):
        l = SortedLimitedList(n=n, key=(lambda line: line[1]))

        for i in range(1, n):
            l.insert((0, 7*i))
            assert(l.len() == i)

        for i in range(n, n+10):
            l.insert((0, 7*i))
            assert(l.len() == n)

