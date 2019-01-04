import fms
from fractions import Fraction
from bigrun import lcm
import sys


def make_common_frac(fracs):
    univ_lcm = fracs[0].denominator
    for frac in fracs:
        univ_lcm = lcm(univ_lcm, frac.denominator)

    return ['\\ob{%d}' % int(frac.numerator * (univ_lcm / frac.denominator)) for frac in fracs], univ_lcm


def data_to_latex(share_strs, frac_strs, univ_lcm):
    result = '\\renewcommand{\\ob}[1]{\\frac{#1}{%d}}\n\n' \
             '\\[\n \\begin{array}{%s} \n' % (univ_lcm, 'c' * (len(frac_strs) * 2 - 1))
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


def split_to_latex(share_strs, frac_strs, univ_lcm, share_size, low):
    result = '\n\n\\bigskip\n\\bigskip\n\\bigskip\n\n' \
             'The following picture is just of the %d shares:\n\n' % share_size
    result += '\\renewcommand{\\ob}[1]{\\frac{#1}{%d}}\n\n' \
              '\[\n\\begin{array}{%s}\n' % (univ_lcm, 'c' * (len(frac_strs) * 2 - 1))
    ind = [0, 1, 1, 2, 2, 3]
    if low:
        if len(frac_strs) == 4:
            result += '( & %s & )( & %s & | & %s & )\\cr\n' % (share_strs[0], share_strs[1], share_strs[2])
        else:
            result += '( & %s & )[ & 0 & ]( & %s & | & %s & )\\cr\n' % (share_strs[0], share_strs[1], share_strs[2])
            ind = [0, 1, 2, 3, 3, 4]
    else:
        if len(frac_strs) == 4:
            result += '( & %s & | & %s & )( & %s & )\\cr\n' % (share_strs[0], share_strs[1], share_strs[2])
        else:
            result += '( & %s & | & %s & )[ & 0 & ]( & %s & )\\cr\n' % (share_strs[0], share_strs[1], share_strs[2])
            ind = [0, 1, 1, 2, 3, 4]
    for frac in frac_strs:
        result += '%s & & ' % frac
    result = result[:-5] + ' \\cr\n'
    result += '\\end{array} \n\\]'
    result += '\n\nWe define the following intervals: \n\\begin{enumerate}\n' + \
              '\item\n$I_1=(%s,%s)$\n' % (frac_strs[ind[0]], frac_strs[ind[1]]) + \
              '\item\n$I_2=(%s,%s)$\n' % (frac_strs[ind[2]], frac_strs[ind[3]]) + \
              '\item\n$I_3=(%s,%s)$\n' % (frac_strs[ind[4]], frac_strs[ind[5]]) + \
              '\end{enumerate}\n'

    return result


def make_diagram(m, s, ans):
    V, sv, sv1 = fms.calcSv(m, s)

    # G < H
    g = Fraction(m, s) - ans * (V - 1)
    h = Fraction(m, s) - V + 2 + ans * (V - 2)

    frac_strs, univ_lcm = make_common_frac([ans, g, h, 1 - ans]) if g != h else make_common_frac([ans, g, 1 - ans])
    sv_str = '\hbox{%d %d-shs}' % (V * sv, V)
    sv1_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V - 1)

    if g > h:
        v_shares = '\\renewcommand{\\ob}[1]{\\frac{#1}{%d}}\n\n\\[\n \\begin{array}{ccccc}\n' % univ_lcm + \
                   '( & %s & )( & \hbox{0 %d-shs} & )\\cr\n' % (sv_str, V) + \
                   '%s & & %s & & %s\\cr\n' % (frac_strs[0], frac_strs[1], frac_strs[3]) + \
                   '\\end{array} \n\\]'
        v1_shares = '\\renewcommand{\\ob}[1]{\\frac{#1}{%d}}\n\n\\[\n \\begin{array}{ccccc}\n' % univ_lcm + \
                    '( & \hbox{0 %d-shs} & )( & %s & )\\cr\n' % (V - 1, sv1_str) + \
                    '%s & & %s & & %s\\cr\n' % (frac_strs[0], frac_strs[2], frac_strs[3]) + \
                    '\\end{array} \n\\]'
        return v_shares + '\n\n' + v1_shares

    if h > 1 - ans:
        return '\\renewcommand{\\ob}[1]{\\frac{#1}{%d}}\n\n\\[\n \\begin{array}{ccccc}\n' % univ_lcm + \
               '( & %s & )[ & 0 & ]\\cr\n' % sv_str + \
               '%s & & %s & & %s\\cr\n' % (frac_strs[0], frac_strs[1], frac_strs[3]) + \
               '\\end{array} \n\\]'

    if g < ans:
        return '\\renewcommand{\\ob}[1]{\\frac{#1}{%d}}\n\n\\[\n \\begin{array}{ccccc}\n' % univ_lcm + \
               '[ & 0 & ]( & %s & )\\cr\n' % sv1_str + \
               '%s & & %s & & %s\\cr\n' % (frac_strs[0], frac_strs[2], frac_strs[3]) + \
               '\\end{array} \n\\]'

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

        sv_low_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V)
        sv_high_str = '\hbox{%d %d-shs}' % (V * sv - (V - 1) * sv1, V)
        sv1_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1, V - 1)
        if g == h:
            frac_strs, univ_lcm = make_common_frac([ans, 1 - g, g, 1 - ans])
        else:
            frac_strs, univ_lcm = make_common_frac([ans, 1 - h, 1 - g, g, h, 1 - ans])
        result += data_to_latex([sv_low_str, sv_high_str, sv1_str], frac_strs, univ_lcm)

        split_str = '\hbox{%d %d-shs}' % ((V * sv - (V - 1) * sv1) / 2, V)
        if g == h:
            frac_strs, univ_lcm = make_common_frac([ans, 1 - h, Fraction(1, 2), g])
        else:
            frac_strs, univ_lcm = make_common_frac([ans, 1 - h, 1 - g, Fraction(1, 2), g])
        result += split_to_latex([sv_low_str, split_str, split_str], frac_strs, univ_lcm, V - 1, True)

    elif h < Fraction(1, 2):

        sv_str = '\hbox{%d %d-shs}' % (V * sv, V)
        sv1_low_str = '\hbox{%d %d-shs}' % ((V - 1) * sv1 - V * sv, V - 1)
        sv1_high_str = '\hbox{%d %d-shs}' % (V * sv, V - 1)
        if g == h:
            frac_strs, univ_lcm = make_common_frac([ans, g, 1 - g, 1 - ans])
        else:
            frac_strs, univ_lcm = make_common_frac([ans, g, h, 1 - h, 1 - g, 1 - ans])
        result += data_to_latex([sv_str, sv1_low_str, sv1_high_str], frac_strs, univ_lcm)

        split_str = '\hbox{%d %d-shs}' % (((V - 1) * sv1 - V * sv) / 2, V - 1)
        if g == h:
            frac_strs, univ_lcm = make_common_frac([h, Fraction(1, 2), 1 - g, 1 - ans])
        else:
            frac_strs, univ_lcm = make_common_frac([h, Fraction(1, 2), 1 - h, 1 - g, 1 - ans])
        result += split_to_latex([split_str, split_str, sv1_high_str], frac_strs, univ_lcm, V - 1, False)

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
