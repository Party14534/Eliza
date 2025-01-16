# Zach Dellimore

import copy
import re
import random

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


class Keyword:

    word = ""
    rank = 0
    wordType = 0
    response = ""

    def __init__(self, word, rank, wordType, response):
        self.word = word
        self.rank = rank
        self.wordType = wordType
        if response:
            self.response = response


# Keywords
TopKeywords = {
        "friend": Keyword("friend", 1, 1, None),
        "mother": Keyword("mother", 1, 1, None),
        "father": Keyword("father", 1, 1, None),
        "family": Keyword("family", 1, 1, None),
        "feel": Keyword("feel", 1, 3, None),
        "sad": Keyword("sad", 1, 4, None),
        "unhappy": Keyword("unhappy", 1, 4, None),
        "depressed": Keyword("depressed", 1, 4, None)
        }

MiddleKeywords = {
        "because": Keyword("because", 2, 0, "Is that the real reason?"),
        "alway": Keyword("always", 2, 0, "Can you give me an example of a time that happened?"),
        "think": Keyword("think", 2, 0, "What caused you to think that?")
        }

BottomKeywords = {
        "it": "What does it refer to?",
        "maybe": "Why are you not certain?"
        }

ExcludeNouns = {
        "the",
        "hello",
        "i"
        }

Fallback = [
        "Can you elaborate?",
        "Please go on?",
        "Tell me more?"
        ]


def ParseInput(line):
    output = []
    words = re.findall(r'\b\w+\b', line)

    for index, word in enumerate(words):
        # If it is a proper noun rank it
        if len(word) > 0 and word[0].isupper() and word.lower() not in ExcludeNouns:
            output.append(Keyword(word, 1, 2, "Can you tell me about " + word))
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

        singularWord = singularWord.lower()

        if singularWord in TopKeywords:
            keyword = copy.deepcopy(TopKeywords[singularWord])
            if singularWord == "feel" and index < len(words) - 1:
                keyword.word += " " + words[index + 1]
            output.append(keyword)
        elif singularWord in MiddleKeywords:
            output.append(MiddleKeywords[singularWord])

    return output


def main():
    # Main loop of chatbot
    while (True):
        # First get user input
        line = input("User> ")

        if line == "":
            print("Exiting")
            break

        # Then parse user input and generate a response
        output = ParseInput(line)

        sorted_output = sorted(output, key=lambda keyword: keyword.rank)

        response = ""

        if len(sorted_output) > 0:
            keyword = sorted_output[0]

            match sorted_output[0].wordType:
                case 1:
                    response = f"ELIZA> Can you tell me about your {keyword.word}"
                case 2:
                    response = f"ELIZA> Can you tell me about {keyword.word}"
                case 3:
                    response = f"ELIZA> Why do you {keyword.word}"
                case 4:
                    response = f"ELIZA> Why are you {keyword.word}"
                case _:
                    response = keyword.response
        else:
            response = random.choice(Fallback)

        print(response)


if __name__ == "__main__":
    main()
