import fms
from fractions import Fraction
from bigrun import lcm
import sys


def make_common_frac(fracs):
    univ_lcm = fracs[0].denominator
    for frac in fracs:
        univ_lcm = lcm(univ_lcm, frac.denominator)

    return ['\\frac{%d}{%d}' % (int(frac.numerator * (univ_lcm / frac.denominator)), univ_lcm) for frac in fracs]


def data_to_latex(share_strs, frac_strs):
    result = '\\[\n \\begin{array}{%s} \n' % ('c' * (len(frac_strs) * 2 - 1))
    if len(share_strs) < len(frac_strs) - 1:
        for share in share_strs:
            result += '( & %s & )[ & 0 & ]' % share
        result = result[:-9] + ' \\cr\n'
    else:
        for share in share_strs:
            result += '( & %s & )' % share
        result += ' \\cr\n'
    for frac in frac_strs:
        result += '%s & & ' % frac
    result = result[:-5] + ' \\cr\n'
    result += '\\end{array} \n\\]'
    return result


def make_diagram(m, s, ans):
    V, sv, sv1 = fms.calcSv(m, s)

    # G < H
    g = Fraction(m, s) - ans * (V - 1)
    h = Fraction(m, s) - V + 2 + ans * (V - 2)

    frac_strs = make_common_frac([ans, g, h, 1 - ans]) if g != h else make_common_frac([ans, g, 1 - ans])
    sv_str = '\hbox{%d %d-shs}' % (V * sv, V)
    sv1_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V - 1)

    pre_flip_str = data_to_latex([sv_str, sv1_str], frac_strs) + '\n\n'

    if g <= Fraction(1, 2) <= h:
        g = 1 - h if g > 1 - h else g
        h = 1 - g if h < 1 - g else h

        if g == h:
            frac_strs = make_common_frac([ans, h, 1 - ans])
            sv_str = '\hbox{%d %d-shs}' % (V * sv, V)
            sv1_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V - 1)

            return pre_flip_str + data_to_latex([sv_str, sv1_str], frac_strs)

        frac_strs = make_common_frac([ans, g, h, 1 - ans])
        sv_str = '\hbox{%d %d-shs}' % (V * sv, V)
        sv1_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V - 1)

        return pre_flip_str + data_to_latex([sv_str, sv1_str], frac_strs)

    if g > Fraction(1, 2):

        if g == h:
            frac_strs = make_common_frac([ans, 1 - g, g, 1 - ans])
            sv_low_str = '\hbox{%d S%d-shs}' % ((V - 1) * sv1, V)
            sv_high_str = '\hbox{%d L%d-shs}' % (V * sv - (V - 1) * sv1, V)
            sv1_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V - 1)

            return pre_flip_str + data_to_latex([sv_low_str, sv_high_str, sv1_str], frac_strs)

        frac_strs = make_common_frac([ans, 1-h, 1-g, g, h, 1 - ans])
        sv_low_str = '\hbox{%d S%d-shs}' % ((V - 1) * sv1, V)
        sv_high_str = '\hbox{%d L%d-shs}' % (V * sv - (V - 1) * sv1, V)
        sv1_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V - 1)

        return pre_flip_str + data_to_latex([sv_low_str, sv_high_str, sv1_str], frac_strs)

    elif h < Fraction(1, 2):
        if g == h:
            frac_strs = make_common_frac([ans, g, 1 - g, 1 - ans])
            sv_str = '\hbox{%d %d-shs}' % (V * sv, V)
            sv1_low_str = '\hbox{%d S%d-shs}' % ((V - 1) * sv1 - V * sv, V - 1)
            sv1_high_str = '\hbox{%d L%d-shs}' % (V * sv, V - 1)

            return pre_flip_str + data_to_latex([sv_str, sv1_low_str, sv1_high_str], frac_strs)

        frac_strs = make_common_frac([ans, g, h, 1 - h, 1 - g, 1 - ans])
        sv_str = '\hbox{%d %d-shs}' % (V * sv, V)
        sv1_low_str_sl = '\hbox{%d S%d-shs}' % ((V - 1) * sv1 - V * sv, V - 1)
        sv1_low_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1 - V * sv, V - 1)
        sv1_high_str_sl = '\hbox{%d L%d-shs}' % (V * sv, V - 1)
        sv1_high_str = '\hbox{%d %d-shs}' % (V * sv, V - 1)

        return pre_flip_str + data_to_latex([sv_str, sv1_low_str, sv1_high_str], frac_strs) + \
               data_to_latex([sv_str, sv1_low_str_sl, sv1_high_str_sl], frac_strs)


if __name__ == '__main__':
    m = int(sys.argv[1])
    s = int(sys.argv[2])
    try:
        ans = fms.f(m, s)[0] if len(sys.argv) == 3 \
            else Fraction(int(sys.argv[3].split('/')[0]), int(sys.argv[3].split('/')[1]))
        print(make_diagram(m, s, ans))
    except ValueError:
        print('Incorrect arguments.')
