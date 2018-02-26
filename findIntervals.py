from sympy import *
import findQ2
from fractions import Fraction


def flippy_flip(Q, f, g):
    if g < 1 - g:
        small_interval = Interval(Q, f)
        large_interval = Interval(g, 1 - g).union(Interval(1 - f, 1 - Q))
    elif 1 - f < f:
        small_interval = Interval(Q, 1 - g).union(Interval(1 - f, f))
        large_interval = Interval(g, 1 - Q)
    elif 1 - f > g:
        small_interval = Interval(Q, f)
        large_interval = Interval(1 - f, 1 - Q)
    elif 1 - g < f:
        small_interval = Interval(Q, 1 - g)
        large_interval = Interval(g, 1 - Q)
    else:
        small_interval = Interval(Q, f)
        large_interval = Interval(g, 1 - Q)
    return small_interval, large_interval


def find_intervals(m, s):
    Q = Fraction(53, 130)
    print(Q)
    V, sv, sv1 = findQ2.calcSv(m, s)
    print("V: %s" % V)
    print("sv: %s" % sv)
    print("sv1: %s" % sv1)

    f = Fraction(m, s) - Q * (V - 1)
    g = Fraction(m, s) - V + 2 + Q * (V - 2)
    print("f(x) = " + str(f))
    print("1-f(x) = " + str(1-f))
    print("g(x) = " + str(g))
    print("1-g(x) = " + str(1-g))

    small_interval, large_interval = flippy_flip(Q, f, g)
    print("Small Interval: " + str(small_interval))
    print("Large Interval: " + str(large_interval))


if __name__ == '__main__':
    m = 23
    s = 13
    find_intervals(m, s)
