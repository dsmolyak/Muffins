import sys
from fms import f
from procedures import getProcedures
from bigrun import closer_bounds
from fractions import Fraction
import proof_prints

if __name__ == '__main__':
    if len(sys.argv) == 3:
        m = int(sys.argv[1])
        s = int(sys.argv[2])
        ub, ub_type = f(m, s)
        print('For m = %d and for s = %d, f(m,s) has an upper bound of %s.' % (m, s, ub))
        print('This is proven by the %s theorem.' % ub_type)

        proof_prints.gen_proof(m, s)
        print()

        if getProcedures(m, s, ub):
            getProcedures(m, s, ub, True)
            print('\nFor m = %d and s = %d, f(m,s) has lower bound %s, as there exists a '
                  'procedure for cutting m muffins for s students such that the smallest '
                  'piece is at least %s.' % (m, s, ub, ub))
            print('That procedure is shown above. ^')
        else:
            print('\nAttempting the following lower bounds:')
            lb = Fraction(ub.numerator - 1, ub.denominator)
            lb = lb if lb > Fraction(1, 3) else Fraction(1, 3)
            lb = closer_bounds(m, s, lb, ub)

            getProcedures(m, s, lb, True)
            print('\nFor m = %d and s = %d, f(m,s) has lower bound %s, as there exists a '
                  'procedure for cutting m muffins for s students such that the smallest '
                  'piece is at least %s.' % (m, s, lb, lb))
            print('That procedure is shown above. ^')

    if len(sys.argv) == 5:
        m_l = int(sys.argv[1])
        m_u = int(sys.argv[2])
        s_l = int(sys.argv[3])
        s_u = int(sys.argv[4])

        for s in range(s_l, s_u + 1):
            for m in range(m_l if m_l > s else s + 1, m_u + 1):
                ans, ans_type = f(m, s)
                print('For m = %d and for s = %d, f(m,s) has an upper bound of %s.' % (m, s, ans))
                print('This is proven by the %s theorem.' % ans_type)


