We have CODE and identified CWE-ID. 
We want to identify whichCWE identifications are True Positive (TP) and which are False Positive (FP).

1. We evaluate whether the CODE is unit testable for CWE-ID. If no, finish with UNDECIDED, else continue.
2. Evaluate what should be tested. Which inputs and which outputs are expected if the code is not vulnerable?
3. TESTS <- Generate tests with the assumption the code is not vulnerable to the CWE-ID.
4. TEST-RESULTS <- Run tests, in case of compilation errors, use feedback loop to fix tests. If unable to get tests working in x iterations, finish with UNDECIDED.
5. Given the TESTS and TEST-RESULTS, can it be decided whether the code is vulnerable to CWE-ID?
