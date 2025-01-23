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

May not need this
'''

Substitutions = [
        r"Tell me about your \1",
        r"Why do you \1 \2?",
        r"How long have you been \1?",
        r"Tell me about your \2",
        r"Tell me about \1",
        ]


class Keyword:
    word = ""
    rank = 0
    wordType = 0
    substitution = 0
    response = ""

    def __init__(self, word, rank, wordType, response, substitution):
        self.word = word
        self.rank = rank
        self.wordType = wordType
        self.substitution = substitution
        if response:
            self.response = response

    def respond(self, input):
        if self.response:
            return self.response

        pattern = ""

        match self.substitution:
            case 1 | 3:
                pattern = r'.*\b(' + self.word + r')s?\b\s+\b([A-z]+)\b.*'
            case _:
                pattern = r'.*\b(' + self.word + r')s?\b.*'

        response = re.sub(pattern, Substitutions[self.substitution], input,
                          flags=re.IGNORECASE)

        print(pattern, response)

        return response


# Keywords
TopKeywords = {
        "friend": Keyword("friend", 1, 1, None, 0),
        "mother": Keyword("mother", 1, 1, None, 0),
        "father": Keyword("father", 1, 1, None, 0),
        "family": Keyword("family", 1, 1, None, 0),
        "feel": Keyword("feel", 1, 3, None, 1),
        "sad": Keyword("sad", 1, 4, None, 1),
        "unhappy": Keyword("unhappy", 1, 4, None, 2),
        "depressed": Keyword("depressed", 1, 4, None, 2),
        "my": Keyword("my", 1, 1, None, 3)
        }

MiddleKeywords = {
        "because": Keyword("because", 2, 0, "Is that the real reason?", 0),
        "alway": Keyword("always", 2, 0, "Can you give me an example of a time that happened?", 0),
        "think": Keyword("think", 2, 0, "What caused you to think that?", 0),
        "sometime": Keyword("sometimes", 2, 0, "Can you give me an example of a time that happened?", 0)
        }

BottomKeywords = {
        "it": "What does it refer to?",
        "maybe": "Why are you not certain?"
        }

ExcludeNouns = {
        "the",
        "hello",
        "i",
        "he",
        "he's",
        "she",
        "she's",
        "they",
        }

Fallback = [
        "Can you elaborate?",
        "Please go on?",
        "Tell me more?"
        ]


def ParseInput(line):
    output = []
    words = re.findall(r'\b\w+\b', line)

    for word in words:
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
            output.append(keyword)
        elif singularWord in MiddleKeywords:
            output.append(MiddleKeywords[singularWord])
        elif len(word) > 0 and word[0].isupper() and word.lower() not in ExcludeNouns:
            # If it is a proper noun rank it
            output.append(Keyword(word, 1, 2, None, 4))
            continue

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

            response = keyword.respond(line)

        else:
            response = random.choice(Fallback)

        print(response)


if __name__ == "__main__":
    main()
