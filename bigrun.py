from pylatex import Document, LongTable
from pylatex.utils import bold
from fms import f
import procedures
import math
from fractions import Fraction


def factor(n):
    # returns a list containing factors that aren't 1 or n
    # e.g. factor(12) returns [2, 3, 4, 6]
    res = []
    high = int(math.ceil(math.sqrt(n)))
    for i in range(2, high + 1):

        if n % i == 0:
            res.append(i)
            div = n / i
            if div != i:
                res.append(int(div))
    return res


def relatively_prime(m, s):
    if m % s == 0:
        return False
    else:
        l1 = factor(m)
        l2 = factor(s)
        for item in l1:
            if item in l2:
                return False
    return True


def write_file():
    doc = Document('MyDocc')
    doc_open = Document('Open')

    table = LongTable('|c|c|c|c|c|c|c|c|')
    table.add_hline()
    table.add_row((bold('M'), bold('S'), bold('Method'), bold('Open?'),
                   bold('LB'), bold('UB'), bold('LB-CD'), bold('UB-CD')))
    table.add_hline()
    table.add_hline()

    table_open = LongTable('|c|c|c|c|c|c|c|c|')
    table_open.add_hline()
    table_open.add_row((bold('M'), bold('S'), bold('Method'), bold('Open?'),
                        bold('LB'), bold('UB'), bold('LB-CD'), bold('UB-CD')))
    table_open.add_hline()
    table_open.add_hline()

    for s in range(3, 61):
        m_start = s + 1 # if s + 1 > 60 else 60
        for m in range(m_start, 71):
            if relatively_prime(m, s):
                ub, ans_type = f(m, s)
                open_prob = ''
                lb = ''
                lb_cd = ''
                ub_cd = ''
                try:
                    if procedures.getProcedures(m, s, ub):
                        open_prob = ''
                    else:
                        open_prob = 'Open'
                        lb = Fraction(ub.numerator - 1, ub.denominator)
                        lb = lb if lb > Fraction(1, 3) else Fraction(1, 3)
                        lb = closer_bounds(m, s, lb, ub)
                        lb_cd, ub_cd = convert_den(lb, ub)
                except procedures.TimeoutError:
                    open_prob = 'Timeout'
                except KeyError:
                    open_prob = 'Timeout'
                row = (m, s, ans_type, open_prob, str(lb), str(ub), lb_cd, ub_cd)
                table.add_row(row)
                print(row)
                table.add_hline()
                if len(open_prob) > 0:
                    table_open.add_row(row)
                    table_open.add_hline()

    doc.append(table)
    doc.generate_pdf('latex/BIGRUN', clean_tex=False)
    doc_open.append(table_open)
    doc_open.generate_pdf('latex/BIGRUN_opens', clean_tex=False)


# define gcd function
def gcd(x, y):
    while y:
        x, y = y, x % y

    return x


def lcm(x, y):
    lcm = (x*y)//gcd(x,y)
    return lcm


def convert_den(lb, ub):
    lb_num = lb.numerator
    ub_num = ub.numerator
    lb_den = lb.denominator
    ub_den = ub.denominator
    new_den = lcm(lb_den, ub_den)
    res_lb = '{0:d}/{1:d}'.format(int(lb_num * (new_den / lb_den)), new_den)
    res_ub = '{0:d}/{1:d}'.format(int(ub_num * (new_den / ub_den)), new_den)
    return res_lb, res_ub


def open_probs():
    doc_open = Document('Open')
    table_open = LongTable('|c|c|c|c|c|c|c|')
    table_open.add_hline()
    table_open.add_row((bold('M'), bold('S'), bold('LB'), bold('UB'),
                        bold('LB-CD'), bold('UB-CD'), bold('Method')))
    table_open.add_hline()
    table_open.add_hline()

    tuples = [(29, 17), (41, 19), (59, 22), (51, 23), (46, 27), (47, 29), (53, 31), (55, 34)]
    for tup in tuples:
        m = tup[0]
        s = tup[1]
        if tup == (41, 19):
            ub, ans_type = Fraction(983, 2280), 'ERIK'
        else:
            ub, ans_type = f(m, s)
        try:
            if procedures.getProcedures(m, s, ub):
                print('solved')
            else:
                lb = Fraction(ub.numerator - 1, ub.denominator)
                lb = lb if lb > Fraction(1, 3) else Fraction(1, 3)
                if tup == (41, 19):
                    lb = Fraction(980, 2280)
                lb = closer_bounds(m, s, lb, ub)
        except procedures.TimeoutError:
            print('Timeout')
        except KeyError:
            print('Timeout')
        lb_cd, ub_cd = convert_den(lb, ub)
        row = (m, s, str(lb), str(ub), lb_cd, ub_cd, ans_type)
        print(row)
        table_open.add_row(row)
        table_open.add_hline()

    doc_open.append(table_open)
    doc_open.generate_pdf('latex/BIGRUN_opens', clean_tex=False)


def closer_bounds(m, s, lb, ub):
    for den in range(3, 550):
        for num in range(int(den / 3 - 1), int(den / 2 + 1)):
            curr_frac = Fraction(num, den)
            if lb < curr_frac < ub and den % s == 0:
                print(curr_frac)
                try:
                    if procedures.getProcedures(m, s, curr_frac):
                        res_lb, res_ub = convert_den(curr_frac, ub)
                        print(res_lb, res_ub)
                        lb = curr_frac
                except procedures.TimeoutError:
                    print("no")
                except KeyError:
                    print("no")
    return lb


if __name__ == '__main__':
    write_file()
