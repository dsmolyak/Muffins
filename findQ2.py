from fractions import Fraction
import math
import FloorCeiling


def calcSv(m, s):
    V = math.ceil(2 * m / s)
    sv = (2 * m) - (V * s) + s
    sv1 = (V * s) - (2 * m)
    return V, sv, sv1


def calcQ1(m, s, V, sv, sv1):
    share_avg_fl = math.floor(Fraction(V * sv, sv1))
    share_avg_ceil = math.ceil(Fraction(V * sv, sv1))
    muf_avg = Fraction(m, s)

    A = share_avg_fl + (V - 1 - share_avg_fl) * (V - muf_avg - 1) - muf_avg
    B = share_avg_fl + (V - 2) * (V - 1 - share_avg_fl)
    C = muf_avg - (V - 1 - share_avg_ceil) * (muf_avg - V + 2) - share_avg_ceil * (1 - muf_avg)
    D = share_avg_ceil * (V - 1) + (V - 1 - share_avg_ceil) * (V - 2)

    Q = 0
    if A <= 0:
        Q = 0
    elif C <= 0:
        Q = 0
    elif A > 0 and B > 0 and C > 0 and D > 0:
        Q = min(Fraction(A, B), Fraction(C, D))
    elif A > 0 and B > 0 and C > 0 and D <= 0:
        Q = Fraction(A, B)
    elif A > 0 and B <= 0 and C > 0 and D > 0:
        Q = Fraction(C, D)
    elif A > 0 and B <= 0 and C > 0 and D <= 0:
        Q = math.inf

    LHS = max(Fraction(V - 2, 2 * V - 3), Q)
    RHS = min(Fraction(m, s * V), Fraction(V - 1 - muf_avg, V - 1),
              Fraction(Fraction(1, 2) - muf_avg + V - 2, V - 2))

    return LHS if LHS <= RHS else 1


def calcQ2(m, s, V, sv, sv1):
    share_avg_fl = math.floor(Fraction((V - 1) * sv1, sv))
    share_avg_ceil = math.ceil(Fraction((V - 1) * sv1, sv))
    muf_avg = Fraction(m, s)

    A = muf_avg - (V - share_avg_fl) * (1 - muf_avg)
    B = share_avg_fl + (V - share_avg_fl) * (V - 1)
    C = share_avg_ceil * (V - muf_avg - 1) + (V - share_avg_ceil) * muf_avg - muf_avg
    D = share_avg_ceil * (V - 2) + (V - share_avg_ceil) * (V - 1)

    Q = 0
    if A <= 0:
        Q = 0
    elif C <= 0:
        Q = 0
    elif B > 0 and D > 0:
        Q = min(Fraction(A, B), Fraction(C, D))
    elif A > 0 and B > 0 and C > 0 and D <= 0:
        Q = Fraction(A, B)
    elif A > 0 and B <= 0 and C > 0 and D > 0:
        Q = Fraction(C, D)
    elif A > 0 and B <= 0 and C > 0 and D <= 0:
        Q = math.inf

    LHS = max(Fraction(V - 2, 2 * V - 3), Q)
    RHS = min(Fraction(m, s * V), Fraction(V - 1 - Fraction(m, s), V - 1),
              Fraction(Fraction(m, s) - Fraction(1, 2), V - 1))

    return LHS if LHS <= RHS else 1


def calcQ3Q4(m, s, V, sv, sv1):
    Q3 = Fraction((Fraction(m, s) - Fraction(1, 2)), (V - 1))
    Q4 = Fraction(V - Fraction(m, s) - Fraction(3, 2), V - 2)
    LHS = Fraction(V - 2, 2 * V - 3)
    RHS = min(Fraction(m, s * V), Fraction(V - 1 - Fraction(m, s), V - 1))
    Q3 = Q3 if LHS <= Q3 < RHS else 1
    Q4 = Q4 if LHS <= Q4 < RHS else 1
    return (Q3, Q4) if LHS <= RHS and V * sv != (V - 1) * sv1 else (1, 1)


def calcQ5(m, s, V, sv, sv1):
    LHS = Fraction(Fraction(m, s) - Fraction(1, 2))
    RHS = Fraction(m, s * V)
    return LHS if LHS <= RHS and V * sv > (V - 1) * sv1 else 1


def calcQ6(m, s, V, sv, sv1):
    LHS = Fraction(V - Fraction(1, 2) - Fraction(m, s), V - 2)
    RHS = Fraction(V - Fraction(m, s) - 1, V - 1)
    return LHS if LHS <= RHS and V * sv < (V - 1) * sv1 else 1


def calcQ7(m, s, V, sv, sv1):
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


def calcQ8(m, s, V, sv, sv1):
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


def calcQ9(m, s, V, sv, sv1):
    LHS = Fraction(V - 2, 2 * V - 3)
    RHS = min(Fraction(m, s * V), Fraction(V - 1 - Fraction(m, s), V - 1),
              Fraction(Fraction(1, 2) - Fraction(m, s) + V - 2, V - 2))

    return LHS if (LHS <= RHS and V * sv) > m else 1


def calcQ10(m, s, V, sv, sv1):
    LHS = Fraction(V - 2, 2 * V - 3)
    RHS = min(Fraction(m, s * V), Fraction(V - 1 - Fraction(m, s), V - 1),
              Fraction(Fraction(m, s) - Fraction(1, 2), V - 1))

    return LHS if LHS <= RHS and (V - 1) * sv1 > m else 1


def findQ(m, s, printQs):
    V, sv, sv1 = calcSv(m, s)
    # print(str([V, sv, sv1]))
    if sv1 == 0:
        ANS = 1  # max(Fraction(1, 3), Fraction(m, s * (V + 1)), 1 - Fraction(m, s * (V - 2)))
        Q_type = 'N/A'

    else:
        Q1 = calcQ1(m, s, V, sv, sv1)
        Q2 = calcQ2(m, s, V, sv, sv1)
        Q3, Q4 = calcQ3Q4(m, s, V, sv, sv1)
        Q5 = calcQ5(m, s, V, sv, sv1)
        Q6 = calcQ6(m, s, V, sv, sv1)
        Q7 = calcQ7(m, s, V, sv, sv1)
        Q8 = calcQ8(m, s, V, sv, sv1)
        Q9 = calcQ9(m, s, V, sv, sv1)
        Q10 = calcQ10(m, s, V, sv, sv1)

        if printQs:
            print('Q1: ' + str(Q1))
            print('Q2: ' + str(Q2))
            print('Q3: ' + str(Q3))
            print('Q4: ' + str(Q4))
            print('Q5: ' + str(Q5))
            print('Q6: ' + str(Q6))
            print('Q7: ' + str(Q7))
            print('Q8: ' + str(Q8))
            print('Q9: ' + str(Q9))
            print('Q10: ' + str(Q10))

        setQ = [Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10]
        Q = min(setQ)
        Q_type = ''
        if Q == 1:
            Q = 1
            Q_type = 'N/A'
        else:
            Q_type = 'Q' + str(setQ.index(Q) + 1)
        ANS = max(Fraction(1, 3), Fraction(m, s * (V + 1)), 1 - Fraction(m, s * (V - 2)), Q)

    FC = FloorCeiling.floor_ceiling(m, s)
    if printQs:
        print('FC: ' + str(FC))
    ANS = FC if FC <= ANS else ANS
    ANS_type = 'FC' if ANS == FC else Q_type

    return ANS, ANS_type


def calcSet(m, s, V, Q):
    Q_set = {'Q': Q, '1-Q': 1 - Q, 'f': Fraction(m, s) - Q * (V - 1)}
    Q_set['1-f'] = 1 - Q_set['f']
    Q_set['g'] = Fraction(m, s) - V + 2 + Q * (V - 2)
    Q_set['1-g'] = 1 - Q_set['g']
    return Q_set


if __name__ == '__main__':
    # m = 283
    # s = 60
    # Q, ANS_type = findQ(m, s, True)
    # print('Q: ' + str(Q))
    # print('Min type: ' + ANS_type)
    #
    # V = math.ceil(2 * m / s)

    unused_qs = ['Q3', 'Q4', 'Q5', 'Q6']
    for s in range(7, 60):
        for m in range(s + 1, 100):
            Q, ANS_type = findQ(m, s, False)
            if ANS_type in unused_qs:
                print('Q: ' + str(Q))
                print('Min type: ' + ANS_type)

    # print(calcSet(m, s, V, Q))
