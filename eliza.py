# Zach Dellimore

'''
Process:
    1. Parse input for keywords
    2. Rank keywords
    3. Respond to highest ranked keywords
        4. If no keywords are found response with Tell me more about that
'''

'''
Using integers to determine response type
POSSESIVE NOUN = 1
NOUN = 2
VERB = 3
ADJECTIVE = 4
...
'''


import re


class Keyword:

    word = ""
    rank = 0
    wordType = 0

    def __init__(self, word, rank, wordType):
        self.word = word
        self.rank = rank
        self.wordType = wordType


# Keywords
TopKeywords = {
        "friend": Keyword("friend", 1, 1),
        "mother": Keyword("mother", 1, 1),
        "father": Keyword("father", 1, 1),
        "family": Keyword("family", 1, 1),
        "feel": Keyword("feel", 1, 3),
        "sad": Keyword("sad", 1, 4),
        "unhappy": Keyword("unhappy", 1, 4),
        "depressed": Keyword("depressed", 1, 4)
        }

MiddleKeywords = {
        "because": "Is that the real reason?",
        "always": "Can you give me an example of a time that happened?",
        "think": "What caused you to think that?"
        }

BottomKeywords = {
        "it": "What does it refer to?",
        "maybe": "Why are you not certain?"
        }

Fallback = [
        "Can you elaborate?",
        "Please go on?",
        "Tell me more?"
        ]


def ParseInput(line):
    output = []
    words = line.split()
    for word in words:
        # If it is a proper noun rank it
        if len(word) > 0 and word[0].isupper():
            output.append(Keyword(word, 1, 2))
            continue

        # Substitute plurals
        singularWord = ""
        singularWord1 = re.sub(r'(?is)(\B)s\b', r'\1', word)
        singularWord2 = re.sub(r'(?is)(\B)ies\b', r'\1y', word)

        if singularWord2 != word:
            singularWord = singularWord2
        elif singularWord1 != word:
            singularWord = singularWord1
        else:
            singularWord = word

        if singularWord in TopKeywords:
            output.append(TopKeywords[singularWord])

    return output


def main():
    # Main loop of chatbot
    while (True):
        # First get user input
        line = input("User> ")

        if line == "(exit)":
            break

        # Then parse user input and generate a response
        output = ParseInput(line)
        for word in output:
            print(word.word)


if __name__ == "__main__":
    main()
