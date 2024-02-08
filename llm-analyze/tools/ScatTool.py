from langchain.agents import tool


@tool("Get output of a CodeQL SCAT analysis of the file")
def get_codeql_results(file_name):
    """Tool that returns the CodeQL static code analysis (SCAT) of Java code when given the name of the Java file. Consider that these provide many false negative results."""
    with open("scat/codeql-results.csv", "r") as f:
        lines = f.readlines()

    output = ""
    for line in lines:
        if file_name in line:
            output += line + "\n"

    if output == "":
        print("No faults found by SCAT tool")
        return "No faults found by SCAT tool"

    output = "Name,Description,Severity,Message,Path,Start line,Start column,End line,End column\n" + output
    print(output)
    return output

@tool("Get output of a SpotBugs SCAT analysis of the file")
def get_spotbugs_results(file_name):
    """Tool that returns the SpotBugs static code analysis (SCAT) of Java code when given the name of the Java file. Consider that these provide many false negative results."""
    with open("scat/spotbugs-results.csv", "r") as f:
        lines2 = f.readlines()

    output = ""
    for line in lines2:
        if file_name in line:
            output += line + "\n"

    if output == "":
        print("No faults found by SCAT tool")
        return "No faults found by SCAT tool"

    output = "Severity (high/medium),Vulnerability class (D-Dodgy code,B-Bad practice,S-Security,M-Multithreaded correctness,V-Malicious code vulnerability,C-Correctness,I-Internationalization,X-Experimental,P-Performance),Vulnerability description\n" + output
    print(output)
    return output
