from fractions import Fraction
import math

import sys

from procedure import BuddyMatch


def calcSv(m, s):
    V = math.ceil(2 * m / s)
    sv = (2 * m) - (V * s) + s
    sv1 = (V * s) - (2 * m)
    return V, sv, sv1


def floor_ceiling(m, s):
    small = Fraction(m, s * math.ceil(Fraction(2 * m, s)))
    large = 1 - Fraction(m, s * math.floor(Fraction(2 * m, s)))
    result = max(Fraction(1,3), min(small, large))
    return result


def find_dk_one(m, s, V, sv, sv1):
    m_s = Fraction(m, s)
    Q = []
    for k in range(0, V + 1):
        less_than = []
        greater_than = []

        less_than.append(1 - Fraction(m_s, V - 1))
        greater_than.append(Fraction(V - 2, 2 * V - 3))
        less_than.append(Fraction(m_s - Fraction(1, 2), V - 1))

        i = k - 1
        if i >= 0:
            greater_than.append(Fraction(m_s - (V - i) * (1 - m_s), i + (V - i) * (V - 1)))
        i = k + 1
        if i < V + 1:
            greater_than.append(Fraction(m_s * (V - 2 * i - 1) + i * (V - 1), V * V - i - V))

        min_less = min(less_than)
        max_greater = max(greater_than)
        Q.append(max_greater)
        if min_less < max_greater:
            Q[k] = 1
        elif k == 0:
            if (V - 1) * sv1 == 0 and (V - k) * sv == 2 * m:
                Q[k] = 1
        elif k == V:
            if 2 * m - 2 * (V - 1) * sv1 == 0 and k * sv == (V - 1) * sv1:
                Q[k] = 1
        elif (V - 1) * sv1 / k == sv and (V - 1) * sv1 / k == (2 * m - 2 * (V - 1) * sv1) / (V - k):
                Q[k] = 1

    return min(Q)


def find_dk_two(m, s, V, sv, sv1):
    m_s = Fraction(m, s)
    Q = []
    for k in range(0, V):
        less_than = []
        greater_than = []

        less_than.append(Fraction(m, s * V))
        greater_than.append(Fraction(V - 2, 2 * V - 3))
        less_than.append(Fraction(V - m_s - Fraction(3, 2), V - 2))

        i = k - 1
        if i >= 0:
            greater_than.append(Fraction((V - 1 - i) * (V - m_s - 1) - m_s + i, i + (V - 1 - i) * (V - 2)))
        i = k + 1
        if i < V:
            greater_than.append(Fraction(m_s - i * (1 - m_s) - (V - 1 - i) * (m_s - V + 2),
                                         i * (V - 1) + (V - 1 - i) * (V - 2)))

        min_less = min(less_than)
        max_greater = max(greater_than)
        Q.append(max_greater)
        if min_less < max_greater:
            Q[k] = 1
        elif k == 0:
            if V * sv == 0 and (V - 1) * sv1 == 2 * m:
                Q[k] = 1
        elif k == V - 1:
            if 2 * m - 2 * V * sv == 0 and k * sv1 == V * sv:
                Q[k] = 1
        elif V * sv / k == sv1 and V * sv / k == (2 * m - 2 * V * sv) / (V - 1 - k):
                Q[k] = 1

    return min(Q)


def find_dk(m,s):
    V, sv, sv1 = calcSv(m, s)
    dk_1 = find_dk_one(m, s, V, sv, sv1)
    dk_2 = find_dk_two(m, s, V, sv, sv1)
    return (dk_1, 'DK-ONE') if dk_1 < dk_2 else (dk_2, 'DK-TWO')


def find_dkp_one(m, s, V, sv, sv1):
    m_s = Fraction(m, s)
    Q = []
    for k in range(0, V):
        less_than = []
        greater_than = []

        less_than.append(1 - Fraction(m_s, V - 1))
        greater_than.append(Fraction(V - 2, 2 * V - 3))
        less_than.append(Fraction(m_s - Fraction(1, 2), V - 1))

        i = k - 1
        if i >= 0:
            greater_than.append(Fraction(m_s - (V - i) * (1 - m_s), i + (V - i) * (V - 1)))
        i = k + 2
        if i < V + 1:
            greater_than.append(Fraction(m_s * (V - 2 * i - 1) + i * (V - 1), V * V - i - V))

        min_less = min(less_than)
        max_greater = max(greater_than)
        Q.append(max_greater)
        if min_less < max_greater:
            Q[k] = 1
        if (1 + k) * sv - (V - 1) * sv1 >= 0 and (V - 1) * sv1 - k * sv >= 0:
            Q[k] = 1

    return min(Q)


def find_dkp_two(m, s, V, sv, sv1):
    m_s = Fraction(m, s)
    Q = []
    for k in range(0, V-1):
        less_than = []
        greater_than = []

        less_than.append(Fraction(m, s * V))
        greater_than.append(Fraction(V - 2, 2 * V - 3))
        less_than.append(Fraction(V - m_s - Fraction(3, 2), V - 2))

        i = k - 1
        if i >= 0:
            greater_than.append(Fraction((V - 1 - i) * (V - m_s - 1) - m_s + i, i + (V - 1 - i) * (V - 2)))
        i = k + 2
        if i < V:
            greater_than.append(Fraction(m_s - i * (1 - m_s) - (V - 1 - i) * (m_s - V + 2),
                                         i * (V - 1) + (V - 1 - i) * (V - 2)))

        min_less = min(less_than)
        max_greater = max(greater_than)
        Q.append(max_greater)
        if min_less < max_greater:
            Q[k] = 1
        if (1 + k) * sv1 - V * sv >= 0 and V * sv - k * sv1 >= 0:
            Q[k] = 1

    return min(Q)


def find_dkp(m, s):
    V, sv, sv1 = calcSv(m, s)
    dkp_1 = find_dkp_one(m, s, V, sv, sv1)
    dkp_2 = find_dkp_two(m, s, V, sv, sv1)
    return (dkp_1, 'DKp-ONE') if dkp_1 < dkp_2 else (dkp_2, 'DKp-TWO')


def vhalf(m, s, alpha):
    if alpha < Fraction(1, 3):
        return False
    V, sv, sv1 = calcSv(m, s)
    frac_ms = Fraction(m, s)
    if frac_ms * Fraction(1, V + 1) > alpha or 1 - frac_ms * Fraction(1, V - 2) > alpha:
        return False
    x = Fraction(m, s) - alpha * (V - 1)
    x = 1 - alpha if x > 1 - alpha else x
    y = Fraction(m, s) - (1 - alpha) * (V - 2)
    y = alpha if y < alpha else y

    if x <= Fraction(1, 2) and V * sv > m:
        return True
    if y >= Fraction(1, 2) and (V - 1) * sv1 > m:
        return True
    return False


def half(m, s):
    V, sv, sv1 = calcSv(m, s)
    frac_ms = Fraction(m, s)
    if (V-1) * sv1 == V * sv:
        return 1
    if (V-1) * sv1 > V * sv:
        alpha = 1 - Fraction(frac_ms - Fraction(1, 2), V - 2)  # sets y to 1/2
    else:
        alpha = Fraction(frac_ms - Fraction(1, 2), V - 1)  # sets x to 1/2
    alpha = alpha if alpha > Fraction(1, 3) else Fraction(1, 3)
    return alpha if vhalf(m, s, alpha) else 1


def f(m, s):
    fc = floor_ceiling(m, s)
    dk, dk_type = find_dk(m, s)
    dkp, dkp_type = find_dkp(m, s)
    h = half(m, s)
    bm = BuddyMatch.f(m, s) if calcSv(m, s)[0] == 3 else 1
    results = [fc, h, dk, dkp, bm]
    ans = min(results)
    ans_type = ''
    result_types = ['Floor-Ceiling', 'HALF', dk_type, dkp_type, 'BM']
    for i in range(0, len(results)):
        if results[i] == ans:
            ans_type = result_types[i]
            break
    return ans, ans_type


if __name__ == '__main__':
    print(f(23, 13))

