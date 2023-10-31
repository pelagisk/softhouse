from softhouse.winners import SortedLimitedList


def test_sortedlimitedlist():
    l = SortedLimitedList(n=3, key=(lambda line: line[1]))
    l.insert((0, 1))
    assert(l._list == [(0, 1)])
    l.insert((0, 9))
    assert(l._list == [(0, 9), (0, 1)])
    l.insert((0, 4))
    assert(l._list == [(0, 9), (0, 4), (0, 1)])
    l.insert((0, 7))
    assert(l._list == [(0, 9), (0, 7), (0, 4)])