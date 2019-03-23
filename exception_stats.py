import functools

from fms import f
import csv
from fractions import Fraction
from procedure import scott
import bigrun
import sys

filename = 'data/gaps.csv'

with open(filename, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['m', 's', 'ans', 'method'])
    for s in range(1, 100):
        print('----------------> %d' % s)
        max_range = 4 * s  # s * s
        # if s % 2 == 1:
        #     max_range = int(.65 * (s * s))
        # if s % 2 == 0:
        #     max_range = int(.35 * (s * s))
        for m in range(s + 1, max_range):
            if bigrun.relatively_prime(m, s):
                if m % 100 == 0:
                    print(m, s, file=sys.stdout)
                ans = scott.f(m, s, True)
                ub, ub_types = f(m, s)
                if max(Fraction(1, 3), ans) == ub:
                    ans_types = functools.reduce(lambda a, b: a + ',' + str(b), ub_types)
                else:
                    try:
                        print(m, s, ans)
                        lb_type = bigrun.verify_gaps(m, s, ans.numerator, ans.denominator)
                        if lb_type == 'Open':
                            ans_types = 'None'
                            csv_writer.writerow([m, s, ans, ans_types])
                        else:
                            ans_types = lb_type
                    except TimeoutError:
                        ans_types = 'GAPS-TIMEOUT'
                        sys.stdout = open("/dev/stdout", "w")  # not sure why needed, but otherwise I/O error
                    except UnboundLocalError:
                        ans_types = 'None'
                        sys.stdout = open("/dev/stdout", "w")


