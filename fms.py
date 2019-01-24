from fractions import Fraction
import math
from pulp import *
import functools
from procedure import BuddyMatch


def calcSv(m, s):
    V = math.ceil(2 * m / s)
    sv = (2 * m) - (V * s) + s
    sv1 = (V * s) - (2 * m)
    return V, sv, sv1


def floor_ceiling(m, s):
    small = Fraction(m, s * math.ceil(Fraction(2 * m, s)))
    large = 1 - Fraction(m, s * math.floor(Fraction(2 * m, s)))
    result = max(Fraction(1, 3), min(small, large))
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


def find_dk(m, s):
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
    for k in range(0, V - 1):
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
    if (V - 1) * sv1 == V * sv:
        return 1
    if (V - 1) * sv1 > V * sv:
        alpha = 1 - Fraction(frac_ms - Fraction(1, 2), V - 2)  # sets y to 1/2
    else:
        alpha = Fraction(frac_ms - Fraction(1, 2), V - 1)  # sets x to 1/2
    alpha = alpha if alpha > Fraction(1, 3) else Fraction(1, 3)
    return alpha if vhalf(m, s, alpha) else 1


def poss_students(W, intervals, frac_ms, students, poss_studs):
    if len(students) == W:
        if intervals:
            small_total = 0
            big_total = 0
            for share in range(0, W):
                small_total += intervals[int(students[share]) - 1][1]
                big_total += intervals[int(students[share]) - 1][0]
            too_small = small_total <= frac_ms
            too_big = big_total >= frac_ms
            if not too_small and not too_big:
                poss_studs.append(students)
        else:
            poss_studs.append(students)
        return
    if not students or students[-1] == '1':
        poss_students(W, intervals, frac_ms, students + '1', poss_studs)
        poss_students(W, intervals, frac_ms, students + '2', poss_studs)
        poss_students(W, intervals, frac_ms, students + '3', poss_studs)
    elif students[-1] == '2':
        poss_students(W, intervals, frac_ms, students + '2', poss_studs)
        poss_students(W, intervals, frac_ms, students + '3', poss_studs)
    elif students[-1] == '3':
        poss_students(W, intervals, frac_ms, students + '3', poss_studs)


def create_polynomial(vars, poss_studs, interval):
    return functools.reduce(lambda a, b: a + b,
                            [var * coeff for (var, coeff) in zip(vars, [a.count(interval) for a in poss_studs])])


def vmid(m, s, alpha):
    V, sv, sv1 = calcSv(m, s)
    frac_ms = Fraction(m, s)
    if frac_ms * Fraction(1, V + 1) > alpha or 1 - frac_ms * Fraction(1, V - 2) > alpha:
        return False
    x = Fraction(m, s) - alpha * (V - 1)
    y = Fraction(m, s) - (1 - alpha) * (V - 2)
    if x > y:
        return False
    if y <= 0.5:
        intervals = [(y, Fraction(1, 2)),
                     (Fraction(1, 2), 1 - y),
                     (1 - x, 1 - alpha)]
        poss_studs = []
        poss_students(V - 1, intervals, frac_ms, '', poss_studs)
        if not poss_studs:
            return True
        x_vars = [LpVariable('x' + str(i), 0, sv1, LpContinuous) for i in range(len(poss_studs))]

        vars_1 = create_polynomial(x_vars, poss_studs, '1')
        vars_2 = create_polynomial(x_vars, poss_studs, '2')
        vars_3 = create_polynomial(x_vars, poss_studs, '3')

        prob = LpProblem('MID it up', LpMinimize)
        prob += vars_1 == vars_2
        prob += vars_3 == V * sv
        prob += vars_1 + vars_2 == 2 * m - 2 * V * sv
        prob += functools.reduce(lambda a, b: a + b, x_vars) == sv1
        status = prob.solve()
        return status != 1

    else:
        intervals = [(alpha, 1 - y),
                     (1 - x, Fraction(1, 2)),
                     (Fraction(1, 2), x)]
        poss_studs = []
        poss_students(V, intervals, frac_ms, '', poss_studs)
        if not poss_studs:
            return True
        x_vars = [LpVariable('x' + str(i), 0, sv, LpInteger) for i in range(len(poss_studs))]

        vars_1 = create_polynomial(x_vars, poss_studs, '1')
        vars_2 = create_polynomial(x_vars, poss_studs, '2')
        vars_3 = create_polynomial(x_vars, poss_studs, '3')

        prob = LpProblem('MID it up', LpMinimize)
        prob += vars_2 == vars_3
        prob += vars_1 == (V - 1) * sv1
        prob += vars_2 + vars_3 == 2 * m - 2 * (V - 1) * sv1
        prob += functools.reduce(lambda a, b: a + b, x_vars) == sv
        status = prob.solve()
        return status != 1


def mid(m, s):
    V, sv, sv1 = calcSv(m, s)
    frac_ms = Fraction(m, s)
    alphas = {1}
    all_studs = []
    W = V - 1 if sv1 * (V - 1) > sv * V else V
    poss_students(W, [], frac_ms, '', all_studs)
    for stud in all_studs:
        count_1 = stud.count('1')
        count_2 = stud.count('2')
        count_3 = stud.count('3')
        if W == V - 1:
            try:
                alphas.add(1 - ((frac_ms - count_1 * Fraction(1, 2) - count_2 + count_2 * frac_ms) /
                           (count_2 * (V - 2) + count_3)))
            except ZeroDivisionError:
                pass
            try:
                alphas.add(
                    (frac_ms * (1 - count_1 + count_3) - count_2 * Fraction(1, 2) + count_1 * (V - 2) - count_3) /
                    (count_1 * (V - 2) + count_3 * (V - 1)))
            except ZeroDivisionError:
                pass
        else:
            try:
                alphas.add(
                    (frac_ms * (1 + count_1 - count_3) - count_2 * Fraction(1, 2) - count_1 - count_1 * (V - 2)) /
                    (-1 * count_1 * (V - 2) - count_3 * (V - 1)))
            except ZeroDivisionError:
                pass
            try:
                alphas.add((frac_ms - count_3 * Fraction(1, 2) - count_2 + count_2 * frac_ms) /
                           (count_1 + count_2 * (V - 1)))
            except ZeroDivisionError:
                pass
    v_alphas = [alpha for alpha in alphas if vmid(m, s, alpha)]
    return min(v_alphas)


def fbm(m, s):
    V, sv, sv1 = calcSv(m, s)
    if V >= 4:
        return 1
    d = m - s
    k = int(s / (3 * d)) if s % (3 * d) != 0 else int(s / (3 * d)) - 1
    a = s - 3 * d * k
    if a >= 2 * d:
        return Fraction(1, 3)
    elif a <= a <= 2 * d - 1:
        X = min(Fraction(a, 2), Fraction(a + d, 4))
        return Fraction(d * k + X, 3 * d * k + a)
    elif a == 2 * d:
        return 1
    else:
        return 1


def cond(X, a, d):
    return Fraction(a, 3) <= X <= min(Fraction(a, 2), Fraction(a + d, 4))


def cbm(m, s):
    V, sv, sv1 = calcSv(m, s)
    if V >= 4:
        return 1
    d = m - s
    k = int(s / (3 * d)) if s % (3 * d) != 0 else int(s / (3 * d)) - 1
    a = s - 3 * d * k
    if a >= 2 * d:
        return 1
    y1 = max(Fraction(a + 2 * d, 6), Fraction(3 * a - 2 * d, 4), Fraction(2 * a - d, 3))
    x1 = y1 if cond(y1, a, d) else 1
    y2 = max(Fraction(2 * a - d, 3), Fraction(a + d, 5))
    x2 = y2 if cond(y2, a, d) and a != d else 1
    y3 = max(Fraction(3 * a - 2 * d, 4), Fraction(a + 2 * d, 6))
    x3 = y3 if cond(y3, a, d) and 5 * a != 7 * d else 1
    return Fraction(d * k + min(x1, x2, x3), 3 * d * k + a)


def f(m, s):
    fc = floor_ceiling(m, s)
    dk, dk_type = find_dk(m, s)
    dkp, dkp_type = find_dkp(m, s)
    h = half(m, s)
    mi = mid(m, s)
    fb = fbm(m, s)
    cb = cbm(m, s)
    bm = BuddyMatch.f(m, s) if calcSv(m, s)[0] == 3 else 1
    results = [fc, h, dk, dkp, mi, fb, bm]
    ans = min(results)
    result_types = ['FC', 'HALF', dk_type, dkp_type, 'MID', 'FBM', 'CBM', 'BM']
    ans_type = result_types[results.index(ans)]
    return ans, ans_type


if __name__ == '__main__':
    m = 69
    s = 25
    print(f(m, s))
