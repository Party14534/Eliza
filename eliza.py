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


class Substitution:
    pattern = ""
    rank = 0
    output = ""

    def __init__(self, output, pattern, rank):
        self.output = output
        self.pattern = pattern
        self.rank = rank


Substitutions = [
        Substitution("", r"Tell me about your \1", 5),
        Substitution("", r"Why do you \1 \2?", 5),
        Substitution("", r"How long have you been \1?", 5),
        Substitution("", r"Tell me about your \2", 5),
        Substitution("", r"Tell me about \1", 5),
        ]

# Keywords
TopKeywords = {
        "friend": [0],
        "mother": [0],
        "father": [0],
        "family": [0],
        "feel": [1],
        "sad": [2],
        "unhappy": [2],
        "depressed": [2],
        "my": [3]
        }

MiddleKeywords = {
        "because": Substitution("Is that the real reason?", "",  3),
        "always": Substitution("Can you give me an example of a time that happened?", "", 3),
        "think": Substitution("What caused you to think that?", "", 3),
        "sometimes": Substitution("Can you give me an example of a time that happened?", "", 3)
        }

BottomKeywords = {
        "it": Substitution("What does it refer to?", "", 1),
        "maybe": Substitution("Why are you not certain?", "", 1)
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


def getSubstitution(word, patternIndex, input):
    wordPattern = ''

    match patternIndex:
        case 1 | 3:
            wordPattern = r'.*\b(' + word + r')\b\s+\b([A-z]+)\b.*'
        case _:
            wordPattern = r'.*\b(' + word + r')\b.*'

    output = re.sub(wordPattern, Substitutions[patternIndex].pattern, input,
                    flags=re.IGNORECASE)

    if output != input:
        sub = copy.deepcopy(Substitutions[patternIndex])
        sub.output = output
        return sub

    return None


def ParseInput(line):
    output = []
    words = re.findall(r'\b\w+\b', line)

    for word in words:
        if word.lower() in TopKeywords:
            substitutions = TopKeywords[word.lower()]
            for substitutionIndex in substitutions:
                substitution = getSubstitution(word, substitutionIndex, line)
                if substitution:
                    output.append(substitution)

        elif word.lower() in MiddleKeywords:
            output.append(MiddleKeywords[word.lower()])

        elif word.lower() in BottomKeywords:
            output.append(BottomKeywords[word.lower()])

        elif len(word) > 0 and word[0].isupper() and word.lower() not in ExcludeNouns:
            # If it is a proper noun rank it
            substitution = getSubstitution(word, 4, line)
            if substitution:
                output.append(substitution)

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

        sorted_output = sorted(output, reverse=True,
                               key=lambda substitution: substitution.rank)

        response = ""

        if len(sorted_output) > 0:
            response = sorted_output[0].output

        else:
            response = random.choice(Fallback)

        print(response)


if __name__ == "__main__":
    main()
