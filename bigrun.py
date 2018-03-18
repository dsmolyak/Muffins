from pylatex import Document, LongTable, Alignat
from pylatex.utils import bold
from fms import f
from JacobPrograms import Procedures
import math
from fractions import Fraction

import multiprocessing


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
    table = LongTable('|c|c|c|c|c|c|')
    table.add_hline()
    table.add_row((bold('M'), bold('S'), bold('UB'),
                bold('Method'), bold('Open?'), bold('LB')))
    table.add_hline()
    table.add_hline()
    for s in range(3, 51):
        for m in range(s + 1, 61):
            if relatively_prime(m, s):
                ans, ans_type = f(m, s)
                open_prob = ''
                lb = ''
                try:
                    if Procedures.getProcedures(m, s, ans):
                        open_prob = ''
                    else:
                        open_prob = 'Open'
                        lb = Fraction(ans.numerator - 1, ans.denominator)
                        lb = lb if lb > Fraction(1, 3) else Fraction(1, 3)
                        lb, ans = closer_bounds(m, s, lb, ans)
                except Procedures.TimeoutError:
                    open_prob = 'Timeout'
                except KeyError:
                    open_prob = 'Timeout'
                row = (m, s, ans, ans_type, open_prob, lb)
                table.add_row(row)
                print(row)
                table.add_hline()

    doc.append(table)
    doc.generate_pdf('latex/largeRUN_test', clean_tex=False)


def binary_search(m, s, higher, lower):
    for i in range(5):
        mid = (higher + lower) / 2
        print(mid)
        if Procedures.getProcedures(m, s, mid):
            lower = mid
        else:
            higher = mid


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


def closer_bounds(m, s, lb, ub):
    res_ub = str(ub)
    res_lb = str(lb)
    for den in range (5, 200):
        for num in range(int(den / 3 - 1), int(den / 2 + 1)):
            curr_frac = Fraction(num, den)
            if lb < curr_frac < ub:
                print(curr_frac)
                try:
                    if den % s == 0 and Procedures.getProcedures(m, s, curr_frac):
                        res_lb, res_ub = convert_den(curr_frac, ub)
                        print(res_lb, res_ub)
                        lb = curr_frac
                except Procedures.TimeoutError:
                    print("no")
                except KeyError:
                    print("no")
    return res_lb, res_ub


if __name__ == '__main__':
    m = 41
    s = 19
    q, _ = f(m, s)
    lb = Fraction(q.numerator - 1, q.denominator)
    lb = lb if lb > Fraction(1, 3) else Fraction(1, 3)
    print("\n" + str(closer_bounds(m, s, lb, q)))
    # write_file()
    # binary_search(47, 29, Fraction(47, 116), Fraction(93, 232))
