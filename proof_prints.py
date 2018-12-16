from fractions import Fraction
import fms
from bigrun import convert_den


def gen_proof(m, s):
    ans, ans_type = fms.f(m, s)
    V, sv, sv1 = fms.calcSv(m, s)
    print('s_%d = %d and s_%d = %d.' % (V, sv, V - 1, sv1))

    h = Fraction(m, s) - V + 2 + ans * (V - 2)
    g = Fraction(m, s) - ans * (V - 1)
    _, h_str = convert_den(ans, h)
    _, g_str = convert_den(ans, g)
    _, h1_str = convert_den(ans, 1 - h)
    _, g1_str = convert_den(ans, 1 - g)

    if 'ONE' in ans_type:
        V_int_str = '(%s,%s) and (%s,%s)' % (ans, h1_str, g1_str, g_str)
        V1_int_str = '(%s,%s)' % (h_str, 1 - ans)

        print('The %d-shares are in %s' % (V, V_int_str))
        print('The %d-shares are in %s' % (V - 1, V1_int_str))
        
    elif 'TWO' in ans_type:
        V_int_str = '(%s,%s)' % (ans, g_str)
        V1_int_str = '(%s,%s) and (%s,%s)' % (h_str, h1_str, g1_str, 1 - ans)

        print('The %d-shares are in %s' % (V, V_int_str))
        print('The %d-shares are in %s' % (V - 1, V1_int_str))

    elif 'HALF' == ans_type:
        print('beta = ')

