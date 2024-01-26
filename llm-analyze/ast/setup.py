from dotenv import load_dotenv, find_dotenv
from tree_sitter import Language
import os

load_dotenv(find_dotenv())
Language.build_library(
    # Store the library in the `build` directory
    "build/my-languages.so",
    # Include one or more languages
    [os.environ.get("AST_JAVA_REPO_LOCATION")],
)
JAVA_LANGUAGE = Language("build/my-languages.so", "java")
