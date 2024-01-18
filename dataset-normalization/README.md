# Scripts for pre-processing Juliet 1.3 dataset

The pre-processed dataset is available at https://github.com/katamb/juliet-top-25. 
The first steps were done manually.

First make sure you have .env file with the env variable DATASET_DIRECTORY_ROOT defined for the project. 
This should point to the Juliet dataset directory.

Steps taken:
1. Manually delete packages with CWE's that are not in the MITRE top 25. 
Did not remove CWE's that were in the subset of MITRE top 25 vulnerabilities.
2. Upgrade build tools. 
Gradle is easier to run, requires less Java-specific knowledge and is better supported by static analysis tools.
Thus, Gradle build tool was added and all ant-related stuff was removed for simplicity.
3. Use IntelliJ code reformatting to reformat the code. This makes it easier to read.
4. Run `remove-comments.py` to remove all comments and extra whitespace from the test files.
5. Run `prune-testcases.py` to remove the more complex testcases.
6. Run `split-files.py` to split files into 2: good case and bad case.
7. 
