import time

from pylatex import Document, LongTable
from pylatex.utils import bold
from fms import f, calcSv, relatively_prime
from procedure import scott
import procedures
from fractions import Fraction
import sys
from gaps import MuffinsAuto
import functools
import csv

from functools import wraps
import errno
import os
import signal


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


@timeout(10, os.strerror(errno.ETIMEDOUT))
def verify_gaps(m, s, numer, denom):
    with open('output.txt', 'w') as file:
        sys.stdout = file
        muffin = MuffinsAuto(m, s, numer, denom)
        muffin.main()

    with open('output.txt', 'r') as file:
        sys.stdout = sys.__stdout__
        data_str = file.read().replace('\n', '')
        if 'fail' in data_str:
            return 'Open'
        elif data_str[-5:] == 'EERIK':
            return 'MID'
        elif data_str[-4:] == 'ERIK':
            return 'GAP'
        elif data_str[-5:] == 'BILL2':
            return 'GAPBM'
        elif data_str[-5:] == 'BILL1':
            return 'HALF'
        else:
            return 'Open'


def write_file(m_l=3, m_u=70, s_l=3, s_u=60, findProc=False):
    doc = Document('BIGRUN_ALL')
    doc_one = Document('BIGRUN_ONE')
    doc_open = Document('Open')
    doc_non_FC = Document('Non_FC')
    doc_V3 = Document('V3')
    doc_gaps = Document('GAPS')

    table = LongTable('|c|c|c|c|c|c|c|c|')
    table.add_hline()
    table.add_row((bold('M'), bold('S'), bold('Method'), bold('Open?'),
                   bold('LB'), bold('UB'), bold('LB-CD'), bold('UB-CD')))
    table.add_hline()
    table.add_hline()

    table_one = LongTable('|c|c|c|c|c|c|c|c|')
    table_one.add_hline()
    table_one.add_row((bold('M'), bold('S'), bold('Method'), bold('Open?'),
                   bold('LB'), bold('UB'), bold('LB-CD'), bold('UB-CD')))
    table_one.add_hline()
    table_one.add_hline()

    table_open = LongTable('|c|c|c|c|c|c|c|c|')
    table_open.add_hline()
    table_open.add_row((bold('M'), bold('S'), bold('Method'), bold('Open?'),
                        bold('LB'), bold('UB'), bold('LB-CD'), bold('UB-CD')))
    table_open.add_hline()
    table_open.add_hline()

    table_non_FC = LongTable('|c|c|c|c|c|c|c|c|')
    table_non_FC.add_hline()
    table_non_FC.add_row((bold('M'), bold('S'), bold('Method'), bold('Open?'),
                          bold('LB'), bold('UB'), bold('LB-CD'), bold('UB-CD')))
    table_non_FC.add_hline()
    table_non_FC.add_hline()

    table_V3 = LongTable('|c|c|c|c|c|c|c|c|')
    table_V3.add_hline()
    table_V3.add_row((bold('M'), bold('S'), bold('Method'), bold('Open?'),
                      bold('LB'), bold('UB'), bold('LB-CD'), bold('UB-CD')))
    table_V3.add_hline()
    table_V3.add_hline()

    table_gaps = LongTable('|c|c|c|c|c|c|c|c|')
    table_gaps.add_hline()
    table_gaps.add_row((bold('M'), bold('S'), bold('Method'), bold('Open?'),
                      bold('LB'), bold('UB'), bold('LB-CD'), bold('UB-CD')))
    table_gaps.add_hline()
    table_gaps.add_hline()

    bigrun_csv = open('data/bigrun_all.csv', 'w')
    csv_writer = csv.writer(bigrun_csv)
    csv_writer.writerow(['M', 'S', 'FC', 'HALF', 'INT', 'MID', 'EBM', 'HBM', 'VHBM'])

    for s in range(s_l, s_u + 1):
        m_start = s + 1 if s + 1 > m_l else m_l
        for m in range(m_start, m_u + 1):
            if relatively_prime(m, s):
                ub, ans_types, all_results = f(m, s, bigrun=True)
                csv_writer.writerow([m, s] + all_results)
                open_prob = ''
                lb = ''
                lb_cd = ''
                ub_cd = ''
                used_gaps = False
                try:
                    if checkProc(findProc, m, s, ub):
                        open_prob = ''
                    else:
                        used_gaps = True
                        lb = Fraction(ub.numerator - 2, ub.denominator)
                        lb = lb if lb > Fraction(1, 3) else Fraction(1, 3)
                        lb, lb_type = closer_bounds(m, s, lb, ub, max_denom=750)
                        if lb_type == 'Open':
                            open_prob = 'Open'
                            lb_cd, ub_cd = convert_den(lb, ub)
                        else:
                            ans_types = [lb_type]
                            ub = lb
                            lb = ''
                except procedures.TimeoutError:
                    open_prob = 'Timeout'
                except KeyError:
                    open_prob = 'Timeout'
                ans_types_str = functools.reduce(lambda a, b: a + ',' + str(b), ans_types)
                row = (m, s, ans_types_str, open_prob, str(lb), str(ub), lb_cd, ub_cd)
                table.add_row(row)
                row_one = (m, s, ans_types[0], open_prob, str(lb), str(ub), lb_cd, ub_cd)
                table_one.add_row(row_one)
                print(row_one)
                table.add_hline()
                table_one.add_hline()
                if len(open_prob) > 0:
                    table_open.add_row(row)
                    table_open.add_hline()
                if len(open_prob) > 0 or 'FC' not in ans_types_str:
                    table_non_FC.add_row(row)
                    table_non_FC.add_hline()
                V, _, _ = calcSv(m, s)
                if V == 3:
                    if not used_gaps:
                        _, ans_types_all = f(m, s, bigrun=False)
                        ans_types_all_str = functools.reduce(lambda a, b: a + ',' + str(b), ans_types)
                        row = (m, s, ans_types_all_str, open_prob, str(lb), str(ub), lb_cd, ub_cd)
                    table_V3.add_row(row)
                    table_V3.add_hline()
                if len(open_prob) == 0 and used_gaps:
                    table_gaps.add_row(row)
                    table_gaps.add_hline()

    doc.append(table)
    doc.generate_pdf('bigrun/BIGRUN_all', clean_tex=False)
    doc_one.append(table_one)
    doc_one.generate_pdf('bigrun/BIGRUN_one', clean_tex=False)
    doc_open.append(table_open)
    doc_open.generate_pdf('bigrun/BIGRUN_opens', clean_tex=False)
    doc_non_FC.append(table_non_FC)
    doc_non_FC.generate_pdf('bigrun/BIGRUN_non_FC', clean_tex=False)
    doc_V3.append(table_V3)
    doc_V3.generate_pdf('bigrun/BIGRUN_V3', clean_tex=False)
    doc_gaps.append(table_gaps)
    doc_gaps.generate_pdf('bigrun/BIGRUN_GAPS', clean_tex=False)


def open_cases():
    opens = [(67, 21), (69, 32)]
    for i, case in enumerate(opens):
        m = case[0]
        s = case[1]
        ub, ans_types = f(m, s)
        open_prob = ''
        lb = ''
        lb_cd = ''
        ub_cd = ''
        used_gaps = False
        if max(Fraction(1, 3), scott.f(m, s, True)) == ub:
            open_prob = ''
        else:
            used_gaps = True
            lb = Fraction(ub.numerator - 2, ub.denominator)
            lb = lb if lb > Fraction(1, 3) else Fraction(1, 3)
            lb, lb_type = closer_bounds(m, s, lb, ub, max_denom=2000)
            if lb_type == 'Open':
                open_prob = 'Open'
                lb_cd, ub_cd = convert_den(lb, ub)
            else:
                ans_types = [lb_type]
                ub = lb
                lb = ''
        ans_types_str = functools.reduce(lambda a, b: a + ',' + str(b), ans_types)
        row = (m, s, ans_types_str, open_prob, str(lb), str(ub), lb_cd, ub_cd)
        print(row)


# define gcd function
def gcd(x, y):
    while y:
        x, y = y, x % y

    return x


def lcm(x, y):
    lcm = (x * y) // gcd(x, y)
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


def checkProc(findProc, m, s, ub):
    return procedures.getProcedures(m, s, ub) if findProc else max(Fraction(1, 3), scott.f(m, s, True)) == ub


def closer_bounds(m, s, lb, ub, findProc=False, max_denom=1000):
    verify_result = verify_gaps(m, s, lb.numerator, lb.denominator)
    if verify_result != 'Open':
        return lb, verify_result
    found_lb = False
    for den in range(3, max_denom):
        for num in range(int(den / 3 - 1), int(den / 2 + 1)):
            curr_frac = Fraction(num, den)
            if lb < curr_frac < ub and den % s == 0:
                print(curr_frac)
                try:
                    if checkProc(findProc, m, s, curr_frac):
                        found_lb = True
                        res_lb, res_ub = convert_den(curr_frac, ub)
                        print(res_lb, res_ub)
                        lb = curr_frac
                        verify_result = verify_gaps(m, s, lb.numerator, lb.denominator)
                        if verify_result != 'Open':
                            return lb, verify_result
                except procedures.TimeoutError:
                    print("no")
                except KeyError:
                    print("no")
    if found_lb:
        return lb, 'Open'
    else:
        return Fraction(1, 3), 'Open'


def to_csv():
    bigrun_tex = open('bigrun/BIGRUN_all.tex', 'r').read()
    bigrun_csv = open('data/bigrun.csv', 'w')
    csv_writer = csv.writer(bigrun_csv)
    csv_writer.writerow(['m', 's', 'type', 'ans'])
    bigrun_lines = bigrun_tex.split('\n')
    for line in bigrun_lines:
        if '&' in line:
            data = line.split('&')
            if not data[3]:
                csv_writer.writerow([data[0], data[1], data[2], data[5]])
    bigrun_csv.close()


if __name__ == '__main__':
    if len(sys.argv) == 5:
        m = int(sys.argv[1])
        m_l = int(sys.argv[1])
        m_u = int(sys.argv[2])
        s_l = int(sys.argv[3])
        s_u = int(sys.argv[4])
        write_file(m_l, m_u, s_l, s_u)

    else:
        start = time.time()
        verify_gaps(67, 21, 41, 90)
        print(time.time() - start)
