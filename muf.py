import sys
from fms import f
from fms import calcSv
from procedures import getProcedures
from bigrun import closer_bounds
from bigrun import checkProc
import functools
from fractions import Fraction
from diagrams import make_diagram
from procedure import scott


def gen_proof(m, s, ans, ans_types):
    V, sv, sv1 = calcSv(m, s)
    for ans_type in ans_types:
        print('This upper bound is proven by the %s theorem.' % ans_type)
        ans_type = 'DK' if 'DK' in ans_type else ans_type
        if ans_type != 'FC':
            diagrams = ['HALF', 'DK', 'MID']
            if ans_type in diagrams:
                print('We first know s_%d = %d and s_%d = %d.' % (V, sv, V - 1, sv1))
                print('Then, the following diagram illustrates where these shares occur:')
                print(make_diagram(m, s, ans)[diagrams.index(ans_type)])
                print('\n')
            if 'BM' in ans_type:
                V, _, _ = calcSv(m, s)
                d = m - s
                k = int(s / (3 * d)) if s % (3 * d) != 0 else int(s / (3 * d)) - 1
                a = s - 3 * d * k
                print('We know that a = %d, and d = %d.' % (a, d))






if __name__ == '__main__':
    if len(sys.argv) == 3:
        m = int(sys.argv[1])
        s = int(sys.argv[2])
        findProc = bool(sys.argv[3]) if len(sys.argv > 3) else False
        ub, ub_types = f(m, s)

        if checkProc(findProc, m, s, ub):
            getProcedures(m, s, ub, True) if findProc else scott.f(m, s)

            print('\nFor m = %d and s = %d, f(m,s) has lower bound %s, as there exists a '
                  'procedure for cutting m muffins for s students such that the smallest '
                  'piece is at least %s.' % (m, s, ub, ub))
            print('That procedure is shown above. ^\n\n')

            print('For m = %d and for s = %d, f(m,s) has an upper bound of %s.' % (m, s, ub))
            gen_proof(m, s, ub, ub_types)

        else:
            print('\nAttempting the following lower bounds:')
            lb = Fraction(ub.numerator - 1, ub.denominator)
            lb = lb if lb > Fraction(1, 3) else Fraction(1, 3)
            lb, lb_type = closer_bounds(m, s, lb, ub, findProc)

            getProcedures(m, s, ub, True) if findProc else scott.f(m, s)
            print('\nFor m = %d and s = %d, f(m,s) has lower bound %s, as there exists a '
                  'procedure for cutting m muffins for s students such that the smallest '
                  'piece is at least %s.' % (m, s, lb, lb))
            print('That procedure is shown above. ^')

            if lb_type != 'Open':
                output = open('output.txt', 'r').read()
                print(output)

    if len(sys.argv) == 5:
        m_l = int(sys.argv[1])
        m_u = int(sys.argv[2])
        s_l = int(sys.argv[3])
        s_u = int(sys.argv[4])

        for s in range(s_l, s_u + 1):
            for m in range(m_l if m_l > s else s + 1, m_u + 1):
                ans, ans_types = f(m, s)
                ans_types_str = functools.reduce(lambda a, b: a + ',' + str(b), ans_types)
                print('For m = %d and for s = %d, f(m,s) has an upper bound of %s.' % (m, s, ans))
                print('This is proven by the %s theorem.' % ans_types_str)





