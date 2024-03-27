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

Overall, all approaches incorrectly identify an SQL injection vulnerability in the code. The wording of the problem in the case of CodeQL and SpotBugs hints that string concatenation should not be used in SQL statements. Similarly, Claude 3 Opus model correctly mentions that string concatenation should not be used. GPT-4 incorrectly states the function to be vulnerable to SQL injection. We classify all results as false positives, as the code is not exploitable, but all approaches report SQL injection vulnerabilities. The Claude 3 Opus model provides the best verdict, correctly noticing that the code is currently not exploitable. However, it still reports: "vulnerability: YES | vulnerability type: CWE-89", which we count as positive classification.

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
