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
