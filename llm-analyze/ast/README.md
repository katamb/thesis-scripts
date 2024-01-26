To generate AST (abstract syntax tree) of a Java file, first run setup.py file.
This requires first cloning this repo: https://github.com/tree-sitter/tree-sitter-java 
and then setting AST_JAVA_REPO_LOCATION in dotenv file to point to the cloned repo.

Then GetAst.py can be run. Use the function `return_ast` and provide it full file path.
