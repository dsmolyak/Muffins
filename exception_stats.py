from fms import f
import csv
from fractions import Fraction


filename = 'data/fms.csv'

with open(filename, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['m', 's', 'ans', 'exception type (if any)'])
    for s in range(3, 100):
        print('----------------> %d' % s)
        for m in range(s + 1, 1000):
            if m % 100 == 0:
                print(m, s)
            ans, ans_type = f(m, s)
            exception_type = 'None' if ans_type == 'FC' and ans != Fraction(1, 3) else ans_type
            csv_writer.writerow([m, s, ans, exception_type])
