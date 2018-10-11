# Muffins
Various procedural and algorithmic programs to help solve cases of the Muffin problem

## Important Files

### fms.py
Has the function, f(m,s), which runs all of the currently available methods for finding f(m,s).
These methods include Floor-Ceiling, D1, D2, Dk1, Dk2, HALF1, HALF2, and V3 (BM).

### procedure/Procedures.py
Finds whether or not a procedure exists for certain m, s, and guess for f(m,s).

### genAppendix.py
Creates the appendix, where all FC patterns and exceptions to those patterns are listed out.

### bigrun.py
Runs f(m,s) and tests whether there are procedures for the result, for all m and s up to a given
limit.
Additionally, contains a function to test for lower bounds on f(m,s), named "closer_bounds"

### MuffinsAnalysis.ipynb
Contains analysis of all of the exceptions (FC pattern does not apply) found by f(m,s). There
are some nice plots!

### Others...
All the other programs are either not in use or are dependencies for the above programs. For
instance, scripts in the 'procedure' directory are for assistance with finding procedures and V3.
