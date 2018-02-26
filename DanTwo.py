from fractions import Fraction
import findQ2
import DanOne


def statement_one(m, s, V, sv, sv1):
    m_s = Fraction(m, s)
    Q = []
    for k in range(0, V):
        less_than = []
        greater_than = []

        less_than.append(1 - Fraction(m_s, V - 1))
        greater_than.append(Fraction(V - 2, 2 * V - 3))
        less_than.append(Fraction(m_s - Fraction(1, 2), V - 1))

        for i in range(0, k):
            greater_than.append(Fraction(m_s - (V - i) * (1 - m_s), i + (V - i) * (V - 1)))
        for i in range(k + 2, V + 1):
            greater_than.append(Fraction(m_s * (V - 2 * i - 1) + i * (V - 1), V * V - i - V))

        min_less = min(less_than)
        max_greater = max(greater_than)
        Q.append(max_greater)
        if min_less < max_greater:
            Q[k] = 1
        if (1 + k) * sv - (V - 1) * sv1 >= 0 and (V - 1) * sv1 - k * sv >= 0:
            Q[k] = 1

    # print("Stat1 Q list: %s" % str(Q))
    return min(Q)


def statement_two(m, s, V, sv, sv1):
    m_s = Fraction(m, s)
    Q = []
    for k in range(0, V-1):
        less_than = []
        greater_than = []

        less_than.append(Fraction(m, s * V))
        greater_than.append(Fraction(V - 2, 2 * V - 3))
        less_than.append(Fraction(V - m_s - Fraction(3, 2), V - 2))

        for i in range(0, k):
            greater_than.append(Fraction((V - 1 - i) * (V - m_s - 1) - m_s + i, i + (V - 1 - i) * (V - 2)))
        for i in range(k + 2, V):
            greater_than.append(Fraction(m_s - i * (1 - m_s) - (V - 1 - i) * (m_s - V + 2),
                                         i * (V - 1) + (V - 1 - i) * (V - 2)))

        min_less = min(less_than)
        max_greater = max(greater_than)
        Q.append(max_greater)
        if min_less < max_greater:
            Q[k] = 1
        if (1 + k) * sv1 - V * sv >= 0 and V * sv - k * sv1 >= 0:
            Q[k] = 1

    # print("Stat2 Q list: %s" % str(Q))
    return min(Q)


def findDanTwo(m,s):
    V, sv, sv1 = findQ2.calcSv(m, s)
    # print(str([V, sv, sv1]))
    Q_V = statement_one(m, s, V, sv, sv1)
    # print("Min Stat1: %s" % str(Q_V))
    Q_V1 = statement_two(m, s, V, sv, sv1)
    # print("Min Stat2: %s" % str(Q_V1))
    return (Q_V, 'Stat1') if Q_V < Q_V1 else (Q_V1, 'Stat2')
    # return min(Q_V, Q_V1)


if __name__ == '__main__':
    # print(findDanTwo(41, 33))
    count = 0
    for s in range(6, 50):
        for m in range(s + 1, 50):
            QD1, type1 = DanOne.findDanOne(m, s)
            QD2, type2 = findDanTwo(m, s)
            QI, _ = findQ2.findQ(m, s, False)
            same1 = QD1 == QD2
            same2 = QD2 <= QI
            if QD2 != 1: #and same and type == 'Stat2':
                print('%s, %s, %s, %s, %s, %s' % (str(m), str(s), str(QD2), str(QD1), str(QI), str(same2)))
                print(type2)
                if same2:
                    count += 1
    print(count)

