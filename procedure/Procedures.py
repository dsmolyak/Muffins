import math
from fractions import Fraction

from sympy import *

from procedure import integers
from procedure import symflip
import time

from functools import wraps
import errno
import os
import signal
import fms


class TimeoutError(Exception):
    pass

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



# this file contains a bunch of functions to generate procedures for the muffin problem.
# This file is the interface that I use to generate procedures.
# For example, to make procedures for f(m,s), run getProcedures(m,s), or optionally getProcedures(m,s,Q=Fraction(,))


def floorciel(m, s):
    m = S(m)
    s = S(s)
    arg1 = m / (s * ceiling(2 * m / s))
    arg2 = 1 - m / (s * floor(2 * m / s))
    return max(S(1) / 3, min(arg1, arg2))


def getPiecesDenom(m, s):  # returns (piece size list, denominator)
    fc = floorciel(m, s)
    intv = 1

    intervals = symflip.doit(m, s)
    if not intervals == EmptySet():
        points = list(intervals.boundary)
        intv = points[0]
        if intv < fc:
            return intervalToPieces(m, s, intervals)

            # try:
        #	intervals = symflip.doit(m,s)
        #	if not intervals == EmptySet():
        #		points = list(intervals.boundary)
        #		intv = points[0]
        #		if intv < fc:
        #			return intervalToPieces(m,s,intervals)
        # except Exception as e:
        #	print('exception is:')
        #	print(e)
        #	pass

        # or, if floor cieling:
    intervals = symflip.getIntervals(m, s, fc, ceiling(2 * m / s))
    return intervalToPieces(m, s, intervals)


def intervalToPieces(m, s, intervals):  # returns (pieces size list, denominator)
    points = list(intervals.boundary)
    d = symflip.lcm([fraction(f)[1] for f in points] + [s])  # denominator that we are going to use is lcm
    lowest, highest = int(points[0] * d), int(
        points[-1] * d + 1)  # smallest and biggest pieces, working in units of 1/d
    pieces = [n for n in range(lowest, highest) if intervals.contains(S(n) / d)]  # get all pieces
    return (pieces, d)


def procedures(m, s):
    pieces, d = getPiecesDenom(m, s)
    return integers.solve(m, s, d=d, pieces=pieces, intervals=Interval(0, 1))


def getRow(m, s):
    pieces, d = getPiecesDenom(m, s)
    # numProc = len(list(procedures(m,s)))
    hasElem = any(True for _ in procedures(m, s))
    return (m, s, d, pieces, hasElem)


def bigrun(maxM, maxS):
    for m in range(1, maxM + 1):
        for s in range(1, maxS + 1):  # 7, maxS+1):
            if m > s + 1:
                if math.gcd(m, s) == 1:
                    yield getRow(m, s)


def biggrid(maxM, maxS):
    lines = []
    for m in range(1, maxM + 1):
        values = []
        for s in range(1, maxS + 1):
            if m > s:
                # (m,s,d,pieces,hasElem) = getRow(m,s)
                # pieces, d = getPiecesDenom(m,s)
                # bound = pieces[0]/d
                # if hasElem:
                inter = 1
                try:
                    inter,_ = fms.f(m, s)
                except:
                    pass
                fc = floorciel(m, s)
                bound = min(inter, fc)
                if bound == S(1) / 3:
                    values.append(str(bound))
                else:
                    values.append(str(0))
            else:
                values.append(str(0))
        lines.append(";".join(values))
    text = "\n".join(lines)
    text_file = open("girdy3.csv", "w")
    text_file.write(text)
    text_file.close()


def graphMOverS(maxM, maxS):
    lines = []
    for m in range(1, maxM + 1):
        values = []
        for s in range(1, maxS + 1):
            if m > s:
                (m, s, d, pieces, hasElem) = getRow(m, s)
                pieces, d = getPiecesDenom(m, s)
                bound = float(pieces[0]) / float(d)
                mOverS = float(m) / float(s)
                if hasElem:
                    lines.append(str(mOverS) + ", " + str(bound))
    text = "\n".join(lines)
    text_file = open("plot.csv", "w")
    text_file.write(text)
    text_file.close()


def graphMOverSFunky(maxM, maxS):
    lines = []
    for m in range(1, maxM + 1):
        values = []
        for s in range(1, maxS + 1):
            if m > s:
                (m, s, d, pieces, hasElem) = getRow(m, s)
                pieces, d = getPiecesDenom(m, s)
                bound = float(pieces[0]) / float(d)
                mOverS = float(m) / float(s)
                if hasElem:
                    lines.append(str(mOverS) + ", " + str(bound * (s / m) ** 0.5))
    text = "\n".join(lines)
    text_file = open("funky-plot.csv", "w")
    text_file.write(text)
    text_file.close()


def resultsToStr(results):
    lines = []
    for result in results:
        (m, s, d, pieces, hasElem) = result
        pieceStr = ','.join([str(piece) for piece in pieces])
        line = "%d, %d, %d, [%s], %s" % (m, s, d, pieceStr, str(hasElem))
        lines.append(line)
    return '\n'.join(lines)


def resultsToFile(results, filename):
    text_file = open(filename, "w")
    text_file.write(resultsToStr(results))
    text_file.close()


def stupidStr(results):
    lines = []
    for result in results:
        (m, s, d, pieces, hasElem) = result
        size = float(pieces[0] / d)
        if not hasElem:
            line = "%d, %d, %s" % (m, s, str(size))
            lines.append(line)
    return '\n'.join(lines)


def procedureToString(procedure):
    lines = []
    muffins, students = procedure
    lines.append("Muffins:")
    for muffin in muffins:
        count, pieces = muffin
        lines.append(str(count) + " x " + str(pieces))
    lines.append("Students:")
    for student in students:
        count, pieces = student
        lines.append(str(count) + " x " + str(pieces))
    return '\n'.join(lines)


# @timeout(900, os.strerror(errno.ETIMEDOUT))
def getProcedures(m, s, Q=None, print_proc=False):
    pieces, d = None, None
    if Q == None:
        pieces, d = getPiecesDenom(m, s)
    else:
        # d = Q.denominator
        # numer = Q.numerator
        d = symflip.lcm(Q.denominator, s)
        numer = Q.numerator * d / Q.denominator
        lowest, highest = numer, d - numer  # smallest and biggest pieces, working in units of 1/d
        pieces = [n for n in range(lowest, highest + 1)]  # get all pieces
    procedures = list(integers.solve(m, s, d=d, pieces=pieces, intervals=Interval(0, 1)))
    if print_proc:
        print("denominator: " + str(d))
    for procedure in procedures:
        if print_proc:
            print(procedureToString(procedure))
        return True
    if len(procedures) == 0:
        if print_proc:
            print('No procedures found')
        return False


def try6multiples(upto, start=1):
    text = []
    for k in range(start, upto + 1):
        m = 6 * k + 3
        s = 6 * k + 1
        Q = S(4 * k + 1) / S(12 * k + 2)
        interval = Interval(Q, 1 - Q)
        pieces, d = intervalToPieces(m, s, interval)
        procedures = integers.solve(m, s, d=d, pieces=pieces, intervals=Interval(0, 1))
        text.append(
            "m, s = " + str((m, s)) + "\ndenominator=" + str(d) + '\n' + procedureToString(next(procedures)) + '\n')
    return '\n'.join(text)


if __name__ == '__main__':
    m = 59
    s = 33

    Q, ANS_type = fms.f(m, s)
    print('Q: ' + str(Q))
    print('Min type: ' + ANS_type)

    start_time = time.time()
    try:
        # print(m, s, str(getProcedures(m, s, Q, True)))
        # print(Fraction(981, 2280))
        print(getProcedures(m, s, Fraction(293, 726), True))
    except TimeoutError:
        print('darn')
    except KeyError:
        print('darn')
    print(time.time() - start_time)

