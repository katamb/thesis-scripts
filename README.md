# Scripts for Masters thesis
This repository contains Python script used for running the experiments required for my Master thesis.
For variables, a dotenv (`.env`) file should be created.
The associated dataset is available in: https://github.com/katamb/juliet-top-25.

## The `dataset-normalization` package
This package contains the scripts used for pre-processing the dataset. The files should be run in order.
To run the scripts, a variable called `DATASET_DIRECTORY_ROOT` should be set up in the dotenv file, which should point to the dataset root directory.
The original dataset id the Java Juliet 1.3 dataset: https://samate.nist.gov/SARD/test-suites/111.
The dataset was reduced to contain the vulnerabilities from MITRE's top 25 and the subcategories of the MITRE's top 25.
The build tooling was changed to Gradle and then the scripts in this repository were used for further pre-processing.

We don't want to give LLMs clues about the vulnerabilities in the files, so we remove comments and change names of variables (like "good" or "bad") which could give away the answer.
Secondly we don't want to waste tokens, as running LLMs is expensive, so we want to remove unnecessary whitespace. The steps taken:
1. Run `remove-comments.py` to remove all comments and extra whitespace from the test files.
2. Run `prune-testcases.py` to remove the more complex testcases spanning multiple files. Similarly to what was done for example here: https://arxiv.org/pdf/2311.16169.pdf
3. Run `split-files.py` to split files into 2: good case and bad case.
4. Run `remove-clues.py` script to also rename the files and most of the methods.
   After that, some manual processing were required, e.g.
   replacing all instances of "good" and "bad" in remaining variable and method names.
   Also, to help later classifications, a `file-mapping.csv` file is added to the dataset root which maps the new obscure files
   to the vulnerabilities and marks whether the file is vulnerable or not.
5. The resulting dataset is in the `full-pre-processed-set` branch in the dataset repository. 
   The dataset was made smaller using the `get-random-subset.py` script.

## The `llm-analyze` package
This is the package with the logic for running LLM analysis scripts. 
The dotenv file needs to have the following values set: `DATASET_DIRECTORY_ROOT`, the API key of the LLM used (e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`), `RESULTS_DIRECTORY_ROOT`, `CURRENT_DATASET_NAME`.
The tested prompts are in the `prompts` directory. The naming of the prompts differs from the naming in the thesis paper but the contents match. A mapping file will be made available. 

If the prompting strategy requires generating API call sequence, then:
1. Clone `tree-sitter` repository 
2. Set `AST_JAVA_REPO_LOCATION` in dotenv to point to the `tree-sitter` repository (https://github.com/tree-sitter/tree-sitter)
3. Run the `llm-analyze/tools/ast/setup.py` file
4. Now the `llm-analyze/tools/ast/GetAst.py` and `llm-analyze/tools/ast/ApiCallExtractor.py` should be usable 

The `main.py` is used to orchestrate the experiments. The `BaseLlmRunner.py` contains the common functionalities. 
The `SimplePromptRunner.py` can be used for running prompts that require one call towards the LLM.
The `CriticiseRefinePromptRunner.py` can be used for running prompts that require multiple calls towards the LLM.
The results are written to the `results.csv` file.

Potential improvement ideas:
1. If more testing with higher temperatures is expected, add temperature value to the `results.csv`
2. The LLM version and temperature could also be settable through dotenv file, if that is deemed easier

## The `scat-analyze` package
This package contains scripts for mapping CodeQL and SpotBugs analysis results to a unified format.
Both subdirectories contain the scripts, the results before and after processing and `README.md` files with explanations and links to important resources.

## The `statistics` package
In this folder are the scripts required for analysing the results. 
We utilize a relational database (PostgreSQL) to analyse the results. 
To start off, run `docker compose up` in this folder.

1. Run the scripts in `db_setup.sql` file
2. Import the file mapping csv file (in our case, `statistics/subset-34/file-mapping.csv`)
3. Import the static analysis results (in our case, `statistics/subset-34/scat-results/codeql-extended-quality-results.csv` and `statistics/subset-34/scat-results/spotbugs-extended-results.csv)`)
4. Import the LLM analysis reports (in our case, everything in `statistics/subset-34/llm-results/`)
5. You are ready to run queries. For this, the example scripts with comments are available in files `scat_db_queries.sql`, `llm_db_queries.sql` and `combining_db_queries.sql`.

## The `test-generator` package
**Experimental feature!**

This uses LLMs to generate tests and auto-run them. For this, you need to have the dataset set up in a Docker container.
DISCLAIMER: Running this code is at your own risk. The code generated by LLMs could be malicious and should not be trusted by default.

## The `thesis-writing-checks` package
Used to check for writing best-practices: no long sentences, no "bad" expressions etc. Likely to be removed at some point.
