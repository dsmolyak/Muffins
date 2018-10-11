from fractions import Fraction
import math
from fms import f


def floor_ceiling(m, s):
    small = Fraction(m, s * math.ceil(Fraction(2 * m, s)))
    large = 1 - Fraction(m, s * math.floor(Fraction(2 * m, s)))
    result = max(Fraction(1,3), min(small, large))
    # if result == small:
    #     print("small")
    # elif result == large:
    #     print("large")
    return result


def fc_type(m, s):
    small = Fraction(m, s * math.ceil(Fraction(2 * m, s)))
    large = 1 - Fraction(m, s * math.floor(Fraction(2 * m, s)))
    result = max(Fraction(1, 3), min(small, large))
    if result == small:
        return 'small'
    elif result == large:
        return 'large'
    return 'third'


def factor(n):
    # returns a list containing factors that aren't 1 or n
    # e.g. factor(12) returns [2, 3, 4, 6]
    res = []
    high = int(math.ceil(math.sqrt(n)))
    for i in range(2, high + 1):
        div = n / i
        if div - math.floor(div) == 0.0:
            res.append(i)
            if div != i:
                res.append(int(div))
    return res


def intersect(l1, l2):
    for item in l1:
        if l2.__contains__(item):
            return True
    return False


def fc_pattern(d, s):
    if not intersect(factor(s),factor(s + d)):
        type = 'third'
        k = 1
        _, q_type = f(s * k + d, s)
        while type == 'third' or q_type != 'FC':
            type = fc_type(s * k + d, s)
            _, q_type = f(s * k + d, s)
            k += 1
        # print(type)
        denom = str(2 * s) + 'k'
        numer = str(s) + 'k'
        if type == 'small':
            numer += '+' + str(d)
            if 2 * d > s:
                denom += '+' + str(2 * s)
            else:
                denom += '+' + str(s)
        elif type == 'large':
            if 2 * d >= s:
                denom += '+' + str(s)
                numer += ('-' if s - d < 0 else '+') + str(s - d)
            else:
                numer += '-' + str(d)
        return numer, denom
    else:
        return None, None



if __name__ == '__main__':
    print(floor_ceiling(107, 13))

    # s = 10
    # print(floor_ceiling(11,8))
    # for d in range(1, s):
    #     num, den = fc_pattern(d, s)
    #     if num:
    #         print(num + ' / ' + den)

