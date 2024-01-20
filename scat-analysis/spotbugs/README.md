# Running SpotBugs locally

## Setting up the SpotBugs
Follow docs here: https://spotbugs.readthedocs.io/en/latest/installing.html 

## Running SpotBugs
Follow docs here: https://spotbugs.readthedocs.io/en/latest/running.html
and here: https://spotbugs.readthedocs.io/en/latest/gradle.html

## Working with the results
Some of the documentation is really hard to correlate to the tool output. 

    1st col is severity: 
     * H - high
     * M - medium
    2nd col is class:
     * D - Dodgy code (STYLE)
     * B - Bad practice (BAD_PRACTICE)
     * S - Security (SECURITY)
     * M - Multithreaded correctness (MT_CORRECTNESS)
     * V - Malicious code vulnerability (MALICIOUS_CODE)
     * C - Correctness (CORRECTNESS)
     * I - Internationalization (I18N)
     * X - Experimental (EXPERIMENTAL)
     * P - Performance (PERFORMANCE)
