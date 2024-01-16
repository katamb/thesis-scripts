# Scripts for pre-processing Juliet dataset

First make sure you have .env file with the env variable DATASET_DIRECTORY_ROOT defined for the project. 
This should point to the Juliet dataset directory.

Steps taken:
1. Use IntelliJ code reformatting to reformat the code. This makes it easier to read.
2. Run `remove-comments.py` to remove all comments and extra whitespace from the test files.
3. Run `prune-testcases.py` to remove the more complex testcases.
4. Run `split-files.py` to split files into 2: good case and bad case.
5. 
