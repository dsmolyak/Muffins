import fms
from fractions import Fraction
from bigrun import lcm


def make_common_frac(fracs):
    univ_lcm = fracs[0].denominator
    for frac in fracs:
        univ_lcm = lcm(univ_lcm, frac.denominator)

    result = []
    for frac in fracs:
        result.append('\\frac{%d}{%d}' % (int(frac.numerator * (univ_lcm / frac.denominator)), univ_lcm))

    return result


def make_diagram(m, s, ans):
    V, sv, sv1 = fms.calcSv(m, s)

    # G < H
    g = Fraction(m, s) - ans * (V - 1)
    h = Fraction(m, s) - V + 2 + ans * (V - 2)

    if g <= Fraction(1, 2) <= h:
        g = 1 - h if g > 1 - h else g
        h = 1 - g if h < 1 - g else h

        frac_strs = make_common_frac([ans, g, h, 1 - ans])
        sv_str = '\hbox{%d %d-shs}' % (V * sv, V)
        sv1_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V - 1)

        return '\\[\n \\begin{array}{ccccccc} \n' \
               '( & %s & )[ & 0 & ]( & %s & ) \\cr\n' \
               '%s & & %s & & %s & & %s \\cr\n' \
               '\\end{array} \n\\]' % (sv_str, sv1_str, frac_strs[0], frac_strs[1], frac_strs[2], frac_strs[3])

    if g > Fraction(1, 2):
        frac_strs = make_common_frac([ans, 1-h, 1-g, g, h, 1 - ans])
        sv_low_str = '\hbox{%d S%d-shs}' % ((V - 1) * sv1, V)
        sv_high_str = '\hbox{%d L%d-shs}' % (V * sv - (V - 1) * sv1, V)
        sv1_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V - 1)

        return '\\[\n \\begin{array}{ccccccccccc} \n' \
               '( & %s & )[ & 0 & ]( & %s & )[ & 0 & ]( & %s & ) \\cr\n' \
               '%s & & %s & & %s & & %s & & %s & & %s \\cr\n' \
               '\\end{array} \n\\]' % (sv_low_str, sv_high_str, sv1_str, frac_strs[0], frac_strs[1],
                                       frac_strs[2], frac_strs[3], frac_strs[4], frac_strs[5])

    elif h < Fraction(1, 2):
        frac_strs = make_common_frac([ans, g, h, 1 - h, 1 - g, 1 - ans])
        sv_str = '\hbox{%d %d-shs}' % (V * sv, V)
        sv1_low_str = '\hbox{%d S%d-shs}' % ((V - 1) * sv1 - V * sv, V - 1)
        sv1_high_str = '\hbox{%d L%d-shs}' % (V * sv, V - 1)

        return '\\[\n \\begin{array}{ccccccccccc} \n' \
               '( & %s & )[ & 0 & ]( & %s & )[ & 0 & ]( & %s & ) \\cr\n' \
               '%s & & %s & & %s & & %s & & %s & & %s \\cr\n' \
               '\\end{array} \n\\]' % (sv_str, sv1_low_str, sv1_high_str, frac_strs[0], frac_strs[1],
                                       frac_strs[2], frac_strs[3], frac_strs[4], frac_strs[5])


if __name__ == '__main__':
    m = 10
    s = 9
    print(make_diagram(m, s, fms.f(m, s)[0]))