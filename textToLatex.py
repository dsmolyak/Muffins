from pylatex import Document, LongTable, Alignat
from pylatex.utils import bold
from fractions import Fraction
import findQ2
import DanOne
import DanTwo


def parseIntervals(intervals):
    result = '('
    start = intervals[0]
    current = intervals[0] - 1
    found_end = False
    end = -1
    for i in range(0, len(intervals)):
        if i == len(intervals) - 1:
            last = intervals[i]
            if last == current + 1:
                if last - start > 0:
                    result += '%s-%s' % (start, last)
                else:
                    result += '%s' % start
            else:
                end = intervals[i - 1]
                if end - start > 0:
                    result += '%s-%s,' % (start, end)
                else:
                    result += '%s,' % start
                result += str(last)
        else:
            if intervals[i] != current + 1:
                end = intervals[i - 1]
                found_end = True
            if found_end:
                if end - start > 0:
                    result += '%s-%s,' % (start, end)
                else:
                    result += '%s,' % start
                start = intervals[i] if i + 1 < len(intervals) else -1
            current = intervals[i]
            found_end = False

    return result + ')'


def parse_bigrun(filename, dan):
    file = open(filename, "r")
    lines = file.readlines()
    latex_lines = []
    for line in lines:
        intervals = line.split("[")[1].split("]")[0].split(",")
        intervals = [int(interval) for interval in intervals]
        # intervals_str = parseIntervals(intervals)
        intervals_str = str(len(intervals))
        split_line = line.split(", ")
        m = int(split_line[0])
        s = int(split_line[1])
        denominator = int(split_line[2])

        foundSol = (split_line[-1]).strip()
        smallest_frac = Fraction(intervals[0], denominator)

        Q, ANS_type = findQ2.findQ(m,s, False)
        V, sv, sv1 = findQ2.calcSv(m, s)
        f = Fraction(m, s) - Q * (V - 1)
        g = Fraction(m, s) - V + 2 + Q * (V - 2)
        latex_line = ()
        if dan:
            QD1, type1 = DanOne.findDanOne(m, s)
            strQD1 = '' if QD1 == 1 else str(QD1)
            QD2, type2 = DanTwo.findDanTwo(m, s)
            strQD2 = '' if QD2 == 1 else str(QD2)
            same_str = ''
            if QD1 == Q and QD2 == Q:
                same_str = '1,2'
            elif QD1 == Q:
                same_str = '1'
            elif QD2 == Q:
                same_str = '2'
            elif ANS_type == 'Q1' or ANS_type == 'Q2':
                same_str = 'SHIT'
            latex_line = (m, s, denominator, str(foundSol), ANS_type, str(smallest_frac), strQD1, strQD2, same_str)
        else:
            if Q == smallest_frac:
                latex_line = (m, s, denominator, str(foundSol), ANS_type, str(smallest_frac), str(f), str(g), intervals_str) if ANS_type != 'FC' else \
                    (m, s, denominator, str(foundSol), ANS_type, str(smallest_frac), 'N/A', 'N/A', 'N/A')
            else:
                # print(str(m) + ',' + str(s))
                latex_line = (m, s, denominator, str(foundSol), ANS_type, str(smallest_frac), 'N/A', 'N/A', 'N/A')

        if s > 5 and foundSol == 'False' and not (V == 3 and m - s <= 7):
            latex_lines.append(latex_line)

    return sorted(latex_lines, key=lambda x: x[1])


def write_file(table_rows, dan):
    doc = Document('MyDocc')
    table = LongTable('|c|c|c|c|c|c|c|c|c|')
    table.add_hline()
    if dan:
        table.add_row((bold('M'), bold('S'), bold('Denom'),
                       bold('Sol?'), bold('Method'), bold('Q'), bold('D1'), bold('D2'), bold('Same')))
    else:
        table.add_row((bold('M'), bold('S'), bold('Denom'),
                       bold('Sol?'), bold('Method'), bold('Q'), bold('F'), bold('G'), bold('# in Ints')))
    table.add_hline()
    table.add_hline()
    for row in table_rows:
        table.add_row(row)
        table.add_hline()

    doc.append(table)
    doc.generate_pdf('BIGRUN', clean_tex=False)


if __name__ == '__main__':
    dan = False
    table_rows = parse_bigrun("UpTo50.txt", dan)
    # print(parseIntervals([1]))
    write_file(table_rows, dan)
