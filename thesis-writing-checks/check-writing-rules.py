#!/usr/bin/python3
forbidden_words = [
    "reaching out",
    "reach out",
    "awesome",
    "one hand",
    "other hand",
    "given thesis",
    "smashing",
    "whopping",
    "nook and cranny",
    "legit",
    "doable",
    "as you know",
    "nowadays"
]  # Lower case.
raw_text = """

The high popularity of software-based solutions in e-commerce, e-governance, e-banking and other important services creates a demand for software and software engineers. In addition to creating functional software solutions with correct business logic, software engineers are often also expected to be responsible for the security of the application. With the increasing complexity of software, it can be easy to miss vulnerabilities and release vulnerable code to the world. 
Ideally, the vulnerabilities should be found in the early stages of the software development lifecycle. Relying on humans to find all vulnerabilities has proven to not be reliable [1]. This has been recognised and many different approaches have been suggested to help automatically detect vulnerabilities since more than 2 decades ago [2]. The best-known approaches include static, dynamic and hybrid code analysis. In addition, there have also been attempts to use machine learning and deep learning methods to find vulnerabilities. Some of these automated approaches have shown good results and are used in the industry. 
However, the tools used to detect vulnerabilities or bad coding practices can be ineffective or inconvenient to use. The ineffectiveness has been presented by previous benchmarks of the static code analysis tools. Goseva-Popstojanov and Perhinschi found that some Common Weakness Enumerations (CWEs) were detected by the static analysis tools, but others were completely missed, with overall performance close to or below 50% [3]. Amankwah et al. experimented with larger set of tools and showed some static analysis tools perform rather decently, while other tools can perform very poorly [4]. The problem of vulnerable code being released to production is further illustrated by the numbers in the Common Vulnerabilities and Exposures (CVE) database. The CVE database shows increase of reported vulnerabilities over the years [5]. To counter these problems, there is a continuous effort to create new tools, improve existing tools or combine multiple tools to yield better results. 
Large language models (LLMs) have shown good abilities for generating and understanding code. Prior research has shown the LLMs to have some potential for vulnerability detection [6]. By exploring the use of generative AI to detect vulnerabilities, we aim to contribute to the improvement of vulnerability detection tooling.
Research Problem/Hypothesis/Question
The focus of the research is the evaluation of off-the-shelf LLMs as vulnerability detection tools and the evaluation of different prompting techniques for this use case. Additionally, we want to explore the options of using LLMs in conjunction with existing tools to improve the usability of the existing tooling. Thus, the research questions are:
•	MRQ: How would the use of off-the-shelf LLMs be able to contribute to vulnerability detection in source code?
•	RQ1: What prompting approach is most successful with the LLMs to detect vulnerabilities?
•	RQ2: Would the LLMs be able to replace or complement existing tooling?
Scope and Goal
The scope:
1.	Creating a framework to assess a dataset of vulnerabilities using different tools.
2.	Assessing existing static analysis tools capabilities for Java programming language using the Juliet dataset. Java programming language was selected, as the author has witnessed it to be widely used in both the private and public sector in Estonia. Juliet dataset was selected for multiple reasons. Firstly, it is synthetic dataset with function level granularity, simplifying the evaluation of the results. Secondly, it has been widely used in prior studies on static code analysis tools, which allows to build on their work using the best tools for comparisons.
3.	Assessing the LLM vulnerability detection capabilities for Java programming language using the Juliet dataset.
4.	Assessing the potential for LLM usage in the domain of vulnerability detection based on the results.
5.	Assessing the potential for the use of LLMs in conjunction with static code analysis tools.
Limitations:
1.	The experimentation will use the Juliet dataset for Java language, which is a synthetic dataset. While there are other datasets available, the Juliet test suite is published by a reputable vendor (NIST) and has previously been studied for evaluating static code analysis tools. The Juliet dataset has a simple structure with each test case containing 1 or 0 vulnerabilities, making it easier to fairly evaluate the results. While a real-world dataset could be argued to be a better representation of vulnerabilities than synthetic dataset, the synthetic dataset gives more confidence the dataset has been properly validated.
2.	A subset of static analysis tools will be used for comparisons. The selection will be based on previous studies benchmarking static analysis tools on the Juliet dataset [4].
3.	The LLMs will be used as black-box devices. Only a few LLMs that have shown good performance in the field of code understanding and generation will be used.
Key assumptions:
1.	Juliet dataset covers many vulnerability types and has enough samples to use it for drawing conclusions.
2.	The training dataset for LLMs might include the Juliet dataset. However, it is also very likely that the developers of static analysis tools have used the Juliet dataset to improve their vulnerability detection rulesets. Meaning neither approach should have an advantage over the other when it comes to the dataset used.
Literature Review
The previous research has shown success in utilizing LLMs as black-box static analysis tools. Szabó and Bilicki managed to achieve an 88% vulnerability detection rate for improper isolation of compartmentalization (CWE-653) weakness in Angular applications using the GPT-4 model [7]. They utilised few-shot and chain-of-thought prompting and used a real-world dataset for evaluation, however, provided no exact numbers for precision, recall and F1 scores. Ozturk et al. achieved a true positive rate between 62% and 68% for finding OWASP's top 10 vulnerabilities in PHP source code using ChatGPT [8]. The true positive rate was almost two times higher than the best-tested static analysis tool, however, ChatGPT also produced a lot higher false positive rate, namely 91%. No precision, recall and F1 scores were provided by the authors. Noever found GPT-4 model was able to achieve better results than two well-known static analysis tools for finding different vulnerabilities in real-world datasets written in different programming languages [6]. No exact precision, recall and F1 scores were provided. Noever made an interesting observation in their research, namely that requesting a fix for the vulnerability improved the performance of the model for vulnerability detection [6].
There have been less successful attempts in the domain as well. Cheshkov, Zadorozhny and Levichev showed that GPT-3.5 and earlier models performed no better than a dummy classifier for finding 5 different vulnerability types in Java code [9]. They used zero-shot prompting on a real-world dataset and calculated precision, recall, F1 and AUC scores. What is more, the authors of Codex, the LLM that also powers Github Copilot, also considered applying the Codex model for vulnerability discovery [10]. While they did emphasize the need for further research in the domain, they found the model did not perform well in comparison to static analysis tools for vulnerability detection.
GPT models have been used for finding security vulnerabilities in source code with varying degrees of success. The researchers have utilized different real-world datasets and used different prompting approaches. However, the focus has mostly been on whether the LLMs are able to identify security vulnerabilities, which has caused the true positives to be highlighted. To get a good overview of the usability of these tools in the real world, false negative and false positive results should be considered as well. What is more, there is no good comparison of different prompting approaches for the same dataset. For most of these works, the datasets are rather small. 
Novelty
As LLMs have gotten major improvements in a short timeframe, there are very few papers looking into the use of modern LLMs to detect vulnerabilities. Most research is based on older LLM models like BERT and very little research uses the largest models like GPT-4. The previous research has mostly used real-world datasets, none of them have used a synthetic dataset like Juliet. The prompting approaches have so far received very little attention, there is no good reasoning on why a specific prompting approach was used. Many papers only focus on less than 10 different CWEs. However just like static analysis tools can detect some vulnerabilities better than others, LLMs might only be good for detecting some types of vulnerabilities. The results are thus varied and the approaches to measuring the performance also vary. 
The contribution consists of multiple parts. Firstly, creating a framework to normalize the dataset, run different analysis tools and systematically report the results. Secondly, using different prompting approaches for LLMs, reporting and analysing the results. Thirdly, combining the LLMs with existing tools and analysing the results.
Research Methods
Normalisation of Juliet dataset:
•	The dataset contains comments and names which hint at whether the method is secure or not. These could influence the decision-making of the LLM and must thus be removed.
Benchmarking static analysis tools on the dataset:
•	Using tools that have shown good performance like YASCA and Java Pathfinder [4].
•	Collecting data on true positive, false positive, true negative, and false negative results.
Benchmarking LLMs on the dataset:
•	Collecting data on true positive, false positive, true negative, and false negative results.
•	Using different prompting techniques and reporting on the results. Firstly, using zero-shot prompting and exploring the use of prompts that have shown good results in previous studies. Secondly, modifying the zero-shot prompts slightly and reporting the results. For example, if LLM reports many false positive results, it would be interesting to explore if adding to the prompt to avoid reporting false positive results affects the output. Thirdly, possibly combining static code analysis tool output with LLMs to use few-shot, chain-of-thought prompting and using hints to enrich the context.
Exploring the value LLMs could add to the processes:
•	Evaluating the ability of LLMs to invalidate false positives from other tools.
•	Potentially evaluating the ability of LLMs to also suggest fixes.
•	Potentially evaluating the ability of LLMs to write tests to validate the issue has been fixed.
Evaluating results:
•	Comparing the results of different approaches used in the study. The Figure 1 displays potential paths we plan to explore. Firstly, running the static code analysis tool (SCAT) on the dataset and reporting results. Secondly, running the LLM with different prompts on the dataset and reporting results. Then, based on the prior results, it would be possible to explore the possibility of using LLM to help discard the true positive results of the SCAT. Another area to explore would be to combine the output of SCAT and LLM analysis to another LLM and asking it to analyse the results.
•	Comparing the results of the study to the results of prior similar studies.



"""  # Put your raw text here.

def main():
    sentences = raw_text.replace("\n", " ").split(".")

    for sentence in sentences:
        words = sentence.strip().split(" ")

        # print(sentence)
        if len(words) > 30:
            print(f"TOO LONG ({len(words)}): {sentence}")

        for forbidden_word in forbidden_words:
            if forbidden_word in sentence.lower():
                print(f"FORBIDDEN WORD: {sentence}")


if __name__ == "__main__":
    main()
