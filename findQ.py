from fractions import Fraction
import math


def calcSv(m, s):
    V = math.ceil(2 * m / s)
    sv = (2 * m) - (V * s) + s
    sv1 = (V * s) - (2 * m)
    return V, sv, sv1


def calcABCD1(m, s, V, sv, sv1):
    share_avg_fl = math.floor(Fraction(V * sv, sv1))
    share_avg_ceil = math.ceil(Fraction(V * sv, sv1))
    muf_avg = Fraction(m, s)

    A = share_avg_fl + (V - 1 - share_avg_fl) * (V - muf_avg - 1) - muf_avg
    B = share_avg_fl + (V - 2) * (V - 1 - share_avg_fl)
    C = muf_avg - (V - 1 - share_avg_ceil) * (muf_avg - V + 2) - share_avg_ceil * (1 - muf_avg)
    D = share_avg_ceil * (V - 1) + (V - 1 - share_avg_ceil) * (V - 2)
    return A, B, C, D


def calcABCD2(m, s, V, sv, sv1):
    share_avg_fl = math.floor(Fraction((V - 1) * sv1, sv))
    share_avg_ceil = math.ceil(Fraction((V - 1) * sv1, sv))
    muf_avg = Fraction(m, s)

    A = muf_avg - (V - share_avg_fl) * (1 - muf_avg)
    B = share_avg_fl + (V - share_avg_fl) * (V - 1)
    C = share_avg_ceil * (V - muf_avg - 1) + (V - share_avg_ceil) * muf_avg - muf_avg
    D = share_avg_ceil * (V - 2) + (V - share_avg_ceil) * (V - 1)
    return A, B, C, D


def calcMIN(A, B, C, D):
    if A <= 0 and B == 0:
        return 0
    elif A > 0 and B == 0 and D > 0:
        return Fraction(C, D)
    elif C <= 0 and D == 0:
        return 0
    elif A > 0 and B == 0 and C > 0 and D == 0:
        return math.inf
    elif A > 0 and B == 0 and D < 0:
        return math.inf
    elif B < 0 < C and D == 0:
        return math.inf
    elif B > 0 > C and D == 0:
        return Fraction(A, B)
    elif B > 0 and D > 0:
        return min(Fraction(A, B), Fraction(C, D))


def checkMINONE(m, s, V, MINONE):
    if MINONE is None:
        return 1
    elif MINONE < (Fraction(1, 2) - Fraction(m, s) + V - 2) / (V - 2):
        return MINONE
    else:
        return 1


def checkMINTWO(m, s, V, MINTWO):
    if MINTWO is None:
        return 1
    elif MINTWO < (Fraction(m, s) - Fraction(1, 2)) / (V - 1):
        return MINTWO
    else:
        return 1


def checkMINFIVE(m, s, sv, sv1, V, MINFIVE):
    if V * sv > (V - 1) * sv1 and Fraction(Fraction(m,s) - Fraction(1,2), V - 1) <= MINFIVE < Fraction(m,sv):
        return MINFIVE
    else:
        return 1


def checkMINSIX(m, s, sv, sv1, V, MINSIX):
    g = Fraction(m, s) - V + 2 + MINSIX * (V - 2)
    if V * sv < (V - 1) * sv1 and MINSIX < Fraction(1,2) <= g < 1 - MINSIX:
        return MINSIX
    else:
        return 1


def calcQ3(m, s, V, sv, sv1):
    if V * sv != (V - 1) * sv1:
        return Fraction(V - Fraction(m, s) - Fraction(3, 2), (V - 2))
    else:
        return 1


def calcQ4(m, s, V, sv, sv1):
    return (Fraction(m, s) - Fraction(1, 2)) / (V - 1) if V * sv != (V - 1) * sv1 else 1


def initQ(Q, m, s, V, sv):
    return (V - 2) / (2 * V - 3) < Q < min(Fraction(m, sv), (V - 1 - Fraction(m, s)) / (V - 1))


def findQ(m, s, print_vars):
    V, sv, sv1 = calcSv(m, s)

    A1, B1, C1, D1 = calcABCD1(m, s, V, sv, sv1)
    MINONE = calcMIN(A1, B1, C1, D1)
    A2, B2, C2, D2 = calcABCD2(m, s, V, sv, sv1)
    MINTWO = calcMIN(A2, B2, C2, D2)
    MINFIVE = Fraction(Fraction(m,s) - Fraction(1,2),V-1)
    MINSIX = Fraction(V - Fraction(m,s) - Fraction(3,2), V-2)

    setQ = [checkMINONE(m, s, V, MINONE), checkMINTWO(m, s, V, MINTWO),
            calcQ3(m, s, V, sv, sv1), calcQ4(m, s, V, sv, sv1)]
    setQ = [x for x in setQ if initQ(x, m, s, V, sv)]
    setQ.append(checkMINFIVE(m, s, sv, sv1, V, MINFIVE))
    setQ.append(checkMINSIX(m, s, sv, sv1, V, MINSIX))
    Qv = min(setQ)
    Q_type = setQ.index(Qv)
    ANS = max(Fraction(1, 3), Fraction(m, s * (V + 1)), 1 - Fraction(m, s * (V - 2)), Qv)
    ANS_type = 'FC' if ANS != Qv else str(Q_type)

    if print_vars:
        print("V: %d" % V)
        print("sv (%d-shares): %d" % (V, sv))
        print("sv1 (%d-shares): %d\n" % (V - 1, sv1))
        print("A: %s\nB: %s\nC: %s\nD: %s" % (str(A1), str(B1), str(C1), str(D1)))
        print("MINONE: " + str(MINONE) + "\n")
        print("A: %s\nB: %s\nC: %s\nD: %s" % (str(A1), str(B1), str(C1), str(D1)))
        print("MINTWO: " + str(MINTWO) + "\n")
        print("MINFIVE: " + str(MINFIVE) + "\n")
        print("MINSIX: " + str(MINSIX) + "\n")
        print(setQ)
        print("Qv: " + str(Qv))
        print("ANS: " + str(ANS))
        print("ANS Type: " + ANS_type)

    return ANS, ANS_type


if __name__ == '__main__':
    # m = int(input("Number of muffins: "))
    # s = int(input("Number of students: "))
    m = 13
    s = 11
    # print(calcSv(m,s))
    findQ(m, s, True)


