# Running CodeQL locally

## Setting up the CodeQL
Follow docs here: https://docs.github.com/en/code-security/codeql-cli/getting-started-with-the-codeql-cli/setting-up-the-codeql-cli
Used: `codeql database create codeql-analysis-top-25 --language=java --overwrite`

## Running CodeQL
Follow docs here: https://docs.github.com/en/code-security/codeql-cli/getting-started-with-the-codeql-cli/analyzing-your-code-with-codeql-queries

In my case, I needed to run: `codeql database analyze codeql-analysis-top-25 --format=csv --output=codeql-results.csv`
when in the dataset directory root.

## Working with the results
The results headers and some explanations: https://docs.github.com/en/code-security/codeql-cli/using-the-advanced-functionality-of-the-codeql-cli/csv-output
The mappings file is here: https://codeql.github.com/codeql-query-help/java-cwe/
