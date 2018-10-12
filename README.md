# Muffins
Various procedural and algorithmic programs to help solve cases of the Muffin problem

## Setup/Prerequisites
1. Must be using Python 3
2. Pulp library installed (`pip install pulp`)
3. Sympy library installed (`pip install sympy`)


## Important Files

### fms.py - named for f(m,s)
Run this program to find the upper bound for f(m,s).

For example: `python fms.py 5 3` will return the upper bound of f(5, 3) and the method used to find it.

### procedure/Procedures.py
Run this program to find the whether a procedure exists for cutting m muffins into s people, with the smallest piece at least a certain size, Q.

For Q generated by fms.py: `python procedure/procedures.py 5 3`

For specifying your own Q: `python procedure/procedures.py 5 3 5/12`
