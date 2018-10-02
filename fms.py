from fractions import Fraction
import math

import time

from JacobPrograms import BuddyMatch


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


def half_one(m, s):
    V, sv, sv1 = calcSv(m, s)
    if V * sv > m:
        return 1

    U = math.ceil(Fraction(V * sv, sv1))
    du1 = U * sv1 - V * sv
    if du1 == 0:
        return 1
    du = V * sv - (U - 1) * sv1
    Xu = math.floor(Fraction(m - V * sv, du))
    Xu1 = math.floor(Fraction(m - V * sv, du1))

    frac_ms = Fraction(m, s)
    A = frac_ms - (U + 1) * (1 - frac_ms) - (V - U - 2) * (frac_ms - V - 2)
    B = (U + 1) * (V - 1) + (V - U - 2) * (V - 2)

    Q7_2 = 0
    if A <= 0:
        Q7_2 = 0
    elif B > 0:
        Q7_2 = Fraction(A, B)
    elif A > 0 and B <= 0:
        Q7_2 = math.inf
    Q7_2 = 0 if U >= sv1 else Q7_2

    C = (U - 2) + (V - U + 1) * (-1 * frac_ms + V - 1) - frac_ms
    D = V ** 2 - U * V - V + 3 * U - 4

    Q7_3 = 0
    if C <= 0:
        Q7_3 = 0
    elif D > 0:
        Q7_3 = Fraction(C, D)
    elif C > 0 and D <= 0:
        Q7_3 = math.inf
    Q7_3 = 0 if U <= 1 else Q7_3

    E = frac_ms - Xu * (frac_ms - V + 2) - (V - 1 - U - Xu) * Fraction(1, 2) - U * (1 - frac_ms)
    F = Xu * (V - 2) + U * (V - 1)
    G = Xu1 * (1 - frac_ms + V - 2) + (V - U - Xu1) * Fraction(1, 2) + (U - 1) - frac_ms
    H = Xu1 * (V - 2) + U - 1

    Q7_5 = 0
    if E <= 0:
        Q7_5 = 0
    elif G <= 0:
        Q7_5 = 0
    elif E > 0 and F > 0 and G > 0 and H > 0:
        Q7_5 = min(Fraction(E, F), Fraction(G, H))
    elif E > 0 and F > 0 and G > 0 and H <= 0:
        Q7_5 = Fraction(E, F)
    elif E > 0 and F <= 0 and G > 0 and H > 0:
        Q7_5 = Fraction(G, H)
    elif E > 0 and F <= 0 and G > 0 and H <= 0:
        Q7_5 = math.inf

    LHS = max(Fraction(V - 2, 2 * V - 3), Q7_2, Q7_3, Q7_5)
    RHS = min(Fraction(m, s * V), Fraction(V - 1 - Fraction(m, s), V - 1),
              Fraction(Fraction(1, 2) - Fraction(m, s) + V - 2), V - 2)

    return LHS if LHS < RHS else 1


def half_two(m, s):
    V, sv, sv1 = calcSv(m, s)
    if (V - 1) * sv1 > m:
        return 1

    U = math.ceil(Fraction((V - 1) * sv1, sv))
    du1 = U * sv - (V - 1) * sv1
    if du1 == 0:
        return 1
    du = (V - 1) * sv1 - (U - 1) * sv
    Xu = math.floor(Fraction(m - (V - 1) * sv1, du))
    Xu1 = math.floor(Fraction(m - (V - 1) * sv1, du1))

    frac_ms = Fraction(m, s)
    A = (U + 1) * (V - frac_ms - 1) + (V - U - 1) * frac_ms - frac_ms
    B = (U + 1) * (V - 2) + (V - 1) * (V - U - 1)

    Q8_2 = 0
    if A <= 0:
        Q8_2 = 0
    elif B > 0:
        Q8_2 = Fraction(A, B)
    elif A > 0 and B <= 0:
        Q8_2 = math.inf
    Q8_2 = 0 if U >= sv else Q8_2

    C = frac_ms - (V - U + 2) * (1 - frac_ms)
    D = U - 2 + (V - U + 2) * (V - 1)

    Q8_3 = 0
    if C <= 0:
        Q8_3 = 0
    elif D > 0:
        Q8_3 = Fraction(C, D)
    elif C > 0 and D <= 0:
        Q8_3 = math.inf
    Q8_3 = 0 if U <= 1 else Q8_3

    E = (Xu - 1) * frac_ms + (V - U - Xu) * Fraction(1, 2) + U * (-1 * frac_ms + V - 1)
    F = Xu * (V - 1) + U * (V - 2)
    G = frac_ms - (V - U + 1 - Xu1) * Fraction(1, 2) - Xu1 * (1 - frac_ms)
    H = Xu1 * (V - 1) + (U - 1)

    Q8_5 = 0
    if E <= 0:
        Q8_5 = 0
    elif G <= 0:
        Q8_5 = 0
    elif E > 0 and F > 0 and G > 0 and H > 0:
        Q8_5 = min(Fraction(E, F), Fraction(G, H))
    elif E > 0 and F > 0 and G > 0 and H <= 0:
        Q8_5 = Fraction(E, F)
    elif E > 0 and F <= 0 and G > 0 and H > 0:
        Q8_5 = Fraction(G, H)
    elif E > 0 and F <= 0 and G > 0 and H <= 0:
        Q8_5 = math.inf

    LHS = max(Fraction(V - 2, 2 * V - 3), Q8_2, Q8_3, Q8_5)
    RHS = min(Fraction(m, s * V), Fraction(V - 1 - frac_ms, V - 1),
              Fraction(frac_ms - Fraction(1, 2), V - 1))

    return LHS if LHS <= RHS else 1


def f(m, s):
    fc = floor_ceiling(m, s)
    dk, dk_type = find_dk(m, s)
    dkp, dkp_type = find_dkp(m, s)
    h1 = half_one(m, s)
    h2 = half_two(m, s)
    bm = BuddyMatch.f(m, s) if calcSv(m, s)[0] == 3 else 1
    results = [fc, dk, dkp, h1, h2, bm]
    ans = min(results)
    ans_type = ''
    result_types = ['FC', dk_type, dkp_type, 'HALF-ONE', 'HALF-TWO', 'BM']
    for i in range(0, len(results)):
        if results[i] == ans:
            ans_type = result_types[i]
            break
    return ans, ans_type


if __name__ == '__main__':
    print(f(59, 33))
    # for s in range(0, 50):
    #     for m in range(s + 1, s*s):
    #         f(m, s)
