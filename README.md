# Muffins
Various procedural and algorithmic programs to help solve cases of the Muffin problem. Thank you to Jacob Prinz for the procedure finding programs (in the procedure folder), and to Saadiq Shaik for the program using the GAPS method (gaps.py).

## Setup/Prerequisites
1. Must be using Python 3 (If Python 3 is not default, replace each occurance below of `python` with `python3` or `python36`)
2. Pulp library installed (`pip install pulp` or `pip3 install pulp`)
3. Sympy library installed (`pip install sympy` or `pip3 install sympy`)
4. Pylatex library installed (`pip install pylatex` or `pip3 install pylatex`)


## Important Files

### muf
Run this program to find the upper bound and lower bound for f(m,s).

For example: `./muf 5 3` will return the upper bound of f(5,3), the method used to find it, the lower bound of f(5,3), and the procedure used to cut m muffins for s people with the lower bound as the smallest piece.
(Replace `muf` with `muf3` or `muf36` depending on what your corresponding command is for `python`)


### diag

Run this program to generate a diagram for a proof of upper bound.

For example: `./diag 11 5` or `./diag 11 5 13/30` will return the latex code for a diagram to help prove that f(11,5) = 13/30
(Replace `diag` with `diag3` or `diag36` depending on what your corresponding command is for `python`)



### fms.py - named for f(m,s)
Run this program to find the upper bound for f(m,s).

For example: `python fms.py 5 3` will return the upper bound of f(5, 3) and the method used to find it.

For ranges of values, for instance 10 < m < 21 and 4 < s < 11:

`python fms.py 11 20 5 10`

### procedures.py
Run this program to find the whether a procedure exists for cutting m muffins for s people, with the smallest piece at least a certain size, Q.

For Q generated by fms.py: `python procedures.py 5 3`

For specifying your own Q: `python procedures.py 5 3 5/12`


### bigrun.py
Run this program to generate a list of upper and lower bounds for f(m,s) in a certain range.

First, to run this program you must create a `bigrun` folder (if it doesn't exist already): `mkdir bigrun`

Then, you run `bigrun.py` with the your lower and upper bound for m and s.

For example, for ranges of values 10 < m < 21 and 4 < s < 11:

`python bigrun.py 11 20 5 10`

The resulting latex and pdfs should appear in the `bigrun` folder.
