from findQ2 import findQ
from DanOne import findDanOne
from DanTwo import findDanTwo

if __name__ == '__main__':
    other_ans_types = ['Q7', 'Q8', 'FC']
    for s in range(7, 60):
        for m in range(s + 1, 100):
            QD1, type1 = findDanOne(m, s)
            QD2, type2 = findDanTwo(m, s)
            Q, ANS_type = findQ(m, s, False)
            if ANS_type not in other_ans_types:
                if QD1 != Q and QD2 != Q:
                    print(m, s, ANS_type)
