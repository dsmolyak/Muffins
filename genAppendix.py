from pylatex import Document, Section, Math, Alignat, NoEscape
from FloorCeiling import fc_pattern
from fractions import Fraction
import math

from fms import f

total_num_exceptions = 0


def find_exceptions(s, d, stat_map):
    pattern_found = False
    start_k = 1
    exceptions = {}
    range_end = int((100 - d) / s) + 1
    for k in range(1, range_end):
        m = s * k + d
        q, q_type = f(m, s)
        if q_type == 'FC' and q != Fraction(1, 3):
            if not pattern_found:
                pattern_found = True
                start_k = k
        elif q_type == 'FC' and q == Fraction(1, 3):
            exceptions[Fraction(m,s)] = (q, r'FC-exception')
            stat_map['total'] += 1
            stat_map['1/3'] += 1
            if math.ceil(2 * m / s) == 3:
                stat_map['V3'] += 1
        elif q_type == 'BM':
            exceptions[Fraction(m, s)] = (q, 'BM-exception')
            stat_map['BM'] += 1
        else:
            exceptions[Fraction(m, s)] = (q, 'INT-exception')
            stat_map['int'] += 1
            stat_map['total'] += 1
            if q == Fraction(1, 3):
                stat_map['1/3'] += 1
            if math.ceil(2 * m / s) == 3:
                stat_map['V3'] += 1
    if not pattern_found:
        start_k = k
    return exceptions, start_k


def create_appendix(stat_map):
    doc = Document('Appendixx')
    doc.append(NoEscape(r'\appendix'))
    with doc.create(Section(NoEscape('Appendix F: Conjectures for $s=3$ to 50'))):
        for s in range(3, 51):
            print('s: ', s)
            exceptions_list = [({}, 0)]
            num_exceptions = 0
            for k in range(1, s):
                print('k: ', k)
                exceptions, start_k = find_exceptions(s, k, stat_map)
                num_exceptions += len(exceptions)
                exceptions_list.append((exceptions, start_k))
            doc.append(NoEscape(r'\begin{conjecture}\label{co:' + str(s) + r'}'))
            doc.append(NoEscape(r'If $m=' + str(s) + r'k+i$ where $0\le i\le ' + str(s - 1) + '$ then $f(m,' + str(s)
                                + r')$ depends only on $k,i$ via a formula, given below'))
            if num_exceptions == 0:
                doc.append('.')
            else:
                doc.append(NoEscape(', with ' + str(num_exceptions) + ' exceptions (we will note the exceptions).'))
            doc.append(NoEscape('\n'))
            doc.append(NoEscape(r'\noindent' + '\n'
                                r'\text{\bf{Case 0:}} $m=' + str(s) + 'k+0$ with $k\ge 1$. Then $f(' +
                                str(s) + 'k,' + str(s) + ')=1$.'))
            doc.append(NoEscape('\n'))
            for i in range(1, s):
                numer, denom = fc_pattern(i, s)
                if numer is not None:
                    exceptions, start_k = exceptions_list[i]
                    pattern_frac = r'\frac{' + numer + '}{' + denom + '}'
                    doc.append(NoEscape(r'\noindent'))
                    doc.append(NoEscape(r'\text{\bf{Case ' + str(i) + ':}} $m=' + str(s) + 'k+' + str(i) +
                                        r'$ with $k\ge ' + str(start_k) + r'$. Then $f(' +
                                        str(s) + 'k+' + str(i) + ',' + str(s) + ')=' + pattern_frac + '$.'))
                    if len(exceptions) != 0:
                        exp_str = ' (Exception: '
                        for exp in exceptions.keys():
                            q, exp_type = exceptions[exp]
                            exp_str += r'$f(' + str(exp.numerator) + ',' + str(exp.denominator) + ')=' \
                                       + str(q) + r'$ ' + exp_type + ', '
                        doc.append(NoEscape(exp_str.strip(', ') + '.)'))
                    doc.append(NoEscape('\n'))
            doc.append(NoEscape(r'\end{conjecture}' + '\n\n' + '--------------------\n'))
    doc.generate_tex('Appendix')
    # doc.generate_pdf('Appendix', clean_tex=False)



if __name__ == '__main__':
    stat_map = {'total': 0, 'V3': 0, 'int': 3, '1/3': 0, 'BM': 0}
    create_appendix(stat_map)
    print(stat_map)
