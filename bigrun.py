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
                        found = False
                        lb = ans
                        while not found:
                            lb = Fraction(lb.numerator * 2 - 1, lb.denominator * 2)
                            found = Procedures.getProcedures(m, s, lb)
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


if __name__ == '__main__':
    write_file()
    # binary_search(47, 29, Fraction(47, 116), Fraction(93, 232))
