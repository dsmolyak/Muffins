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


def half(m, s):
    V, sv, sv1 = calcSv(m, s)
    frac_ms = Fraction(m, s)
    if (V-1) * sv1 == V * sv:
        print('equal shares!')
        return 1

    # Verify 1/3
    if V == 3:
        alpha = Fraction(1, 3)
        beta = frac_ms - (1 - alpha) * (V - 2)
        gamma = frac_ms - alpha * (V - 1)
        if beta >= gamma:
            if gamma >= Fraction(1, 2) and V * sv < (V - 1) * sv1:
                return Fraction(1, 3)
            elif beta <= Fraction(1, 2) and V * sv > (V - 1) * sv1:
                return Fraction(1, 3)

    alpha_1 = 1 - Fraction(frac_ms - Fraction(1, 2), V - 2)
    beta_1 = frac_ms - (1 - alpha_1) * (V - 2)
    gamma_1 = frac_ms - alpha_1 * (V - 1)
    if beta_1 < gamma_1:
        alpha_1 = 1
    alpha_2 = Fraction(frac_ms - Fraction(1, 2), V - 1)
    beta_2 = frac_ms - (1 - alpha_2) * (V - 2)
    gamma_2 = frac_ms - alpha_2 * (V - 1)
    if beta_2 < gamma_2:
        alpha_2 = 1

    return min(alpha_1, alpha_2)


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

    # if len(sys.argv) == 3:
    #     m = int(sys.argv[1])
    #     s = int(sys.argv[2])
    #     ans, ans_type = f(m, s)
    #     print('For m = %d and for s = %d, f(m,s) has an upper bound of %s.' % (m, s, ans))
    #     print('This is proven by the %s theorem.' % ans_type)
    #
    # if len(sys.argv) == 5:
    #     m_l = int(sys.argv[1])
    #     m_u = int(sys.argv[2])
    #     s_l = int(sys.argv[3])
    #     s_u = int(sys.argv[4])
    #
    #     for s in range(s_l, s_u + 1):
    #         for m in range(m_l if m_l > s else s + 1, m_u + 1):
    #             ans, ans_type = f(m, s)
    #             print('For m = %d and for s = %d, f(m,s) has an upper bound of %s.' % (m, s, ans))
    #             print('This is proven by the %s theorem.' % ans_type)
