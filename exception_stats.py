from fms import f
import csv
from fractions import Fraction
from procedure import scottsimple


filename = 'data/fms.csv'


with open(filename, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['m', 's', 'ans'])
    for s in range(3, 100):
        print('----------------> %d' % s)
        max_range = s * s
        # if s % 2 == 1:
        #     max_range = int(.65 * (s * s))
        # if s % 2 == 0:
        #     max_range = int(.35 * (s * s))
        for m in range(s + 1, max_range):
            if m % 100 == 0:
                print(m, s)
            ans = scottsimple.f(m, s)
            # exception_type = 'None' if 'FC' in ans_types and ans != Fraction(1, 3) else ans_types
            csv_writer.writerow([m, s, ans])
