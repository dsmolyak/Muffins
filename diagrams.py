import fms
from fractions import Fraction
from bigrun import lcm
import sys


def make_common_frac(fracs):
    univ_lcm = fracs[0].denominator
    for frac in fracs:
        univ_lcm = lcm(univ_lcm, frac.denominator)

    return ['\\ob{%d}' % int(frac.numerator * (univ_lcm / frac.denominator)) for frac in fracs], univ_lcm


def data_to_latex(share_strs, frac_strs, ob):
    result = '\\renewcommand{\\ob}[1]{\\frac{#1}{%d}}\n\n' \
             '\\[\n \\begin{array}{%s} \n' % (ob, 'c' * (len(frac_strs) * 2 - 1))
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

    frac_strs, univ_lcm = make_common_frac([ans, g, h, 1 - ans]) if g != h else make_common_frac([ans, g, 1 - ans])
    sv_str = '\hbox{%d %d-shs}' % (V * sv, V)
    sv1_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V - 1)

    result = data_to_latex([sv_str, sv1_str], frac_strs, univ_lcm) + '\n\n'

    if g <= Fraction(1, 2) <= h:
        g = 1 - h if g > 1 - h else g
        h = 1 - g if h < 1 - g else h

        sv_str = '\hbox{%d %d-shs}' % (V * sv, V)
        sv1_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V - 1)

        if g == h:
            frac_strs, univ_lcm = make_common_frac([ans, h, 1 - ans])
            result += data_to_latex([sv_str, sv1_str], frac_strs, univ_lcm)
        else:
            frac_strs, univ_lcm = make_common_frac([ans, g, h, 1 - ans])
            result += data_to_latex([sv_str, sv1_str], frac_strs, univ_lcm)

    if g > Fraction(1, 2):

        sv_low_str_sl = '\hbox{%d S%d-shs}' % ((V - 1) * sv1, V)
        sv_low_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V)
        sv_high_str_sl = '\hbox{%d L%d-shs}' % (V * sv - (V - 1) * sv1, V)
        sv_high_str = '\hbox{%d %d-shs}' % (V * sv - (V - 1) * sv1, V)
        sv1_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V - 1)

        if g == h:
            frac_strs, univ_lcm = make_common_frac([ans, 1 - g, g, 1 - ans])
        else:
            frac_strs, univ_lcm = make_common_frac([ans, 1 - h, 1 - g, g, h, 1 - ans])

        result += data_to_latex([sv_low_str, sv_high_str, sv1_str], frac_strs, univ_lcm) + \
            '\n\n' + data_to_latex([sv_low_str_sl, sv_high_str_sl, sv1_str], frac_strs, univ_lcm)

    elif h < Fraction(1, 2):

        sv_str = '\hbox{%d %d-shs}' % (V * sv, V)
        sv1_low_str_sl = '\hbox{%d S%d-shs}' % ((V - 1) * sv1 - V * sv, V - 1)
        sv1_low_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1 - V * sv, V - 1)
        sv1_high_str_sl = '\hbox{%d L%d-shs}' % (V * sv, V - 1)
        sv1_high_str = '\hbox{%d %d-shs}' % (V * sv, V - 1)

        if g == h:
            frac_strs, univ_lcm = make_common_frac([ans, g, 1 - g, 1 - ans])
        else:
            frac_strs, univ_lcm = make_common_frac([ans, g, h, 1 - h, 1 - g, 1 - ans])

        result += data_to_latex([sv_str, sv1_low_str, sv1_high_str], frac_strs, univ_lcm) + \
            '\n\n' + data_to_latex([sv_str, sv1_low_str_sl, sv1_high_str_sl], frac_strs, univ_lcm)

        # if V == 3:
        #     result += '\n\n'

    return result


if __name__ == '__main__':
    m = int(sys.argv[1])
    s = int(sys.argv[2])
    try:
        ans = fms.f(m, s)[0] if len(sys.argv) == 3 \
            else Fraction(int(sys.argv[3].split('/')[0]), int(sys.argv[3].split('/')[1]))
        print(make_diagram(m, s, ans))
    except ValueError:
        print('Incorrect arguments.')
