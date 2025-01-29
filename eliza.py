# Zach Dellimore

import copy
import re
import random

'''
Process:
    1. Parse input for keywords
    2. For each keyword check all their possible substitutions
    3. Respond with the highest ranked substitution
        4. If no keywords are found respond with Tell me more about that


'''


# This class defines the substitutions
class Substitution:
    output = ""  # Optional output for no substitution keywords
    pattern = ""  # Pattern to be used in the substitution
    rank = 0  # Rank used to sort outputs

    def __init__(self, output, pattern, rank):
        self.output = output
        self.pattern = pattern
        self.rank = rank


# List of pre-defined substitutions
Substitutions = [
        Substitution("", r"Tell me about your \1", 5),
        Substitution("", r"Why do you \1 \2", 5),
        Substitution("", r"How long have you been \1", 5),
        Substitution("", r"Tell me about your \2", 4),
        Substitution("", r"Tell me about \1", 5),
        Substitution("", r"When was the last time you felt \3", 6),
        Substitution("", r"Why do you \2 your", 6),
        Substitution("", r"Why do you feel you are", 4)
        ]

# Keywords link from the keyword to their substitution
TopKeywords = {
        "friend": [0],
        "girlfriend": [0],
        "boyfriend": [0],
        "mother": [0],
        "mom": [0],
        "father": [0],
        "dad": [0],
        "sister": [0],
        "brother": [0],
        "cousin": [0],
        "child": [0],
        "children": [0],
        "family": [0],
        "feel": [1, 5],
        "sad": [2],
        "unhappy": [2],
        "depressed": [2],
        "my": [3, 6],
        "am": [7]
        }

NoSubKeywords = {
        "because": Substitution("Is that the real reason?", "",  3),
        "always": Substitution("Can you give me an example of a time that happened?", "", 3),
        "think": Substitution("What caused you to think that?", "", 3),
        "sometimes": Substitution("Can you give me an example of a time that happened?", "", 3),
        "today": Substitution("Can you tell me about your day?", "", 3),
        "it": Substitution("What does it refer to?", "", 1),
        "maybe": Substitution("Why are you not certain?", "", 1),
        "hello": Substitution("Hello, what is it you'd like to talk about?", "", 1)
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
        "i've",
        "there"
        }

Fallback = [
        "Can you elaborate?",
        "Please go on",
        "Tell me more"
        ]


def getSubstitution(word, patternIndex, input):
    wordPattern = ''

    match patternIndex:
        case 7:
            wordPattern = r'.*\b(I)\b\s+\b(am)\b'
        case 6:
            wordPattern = r'.*\b(I)\b\s+\b([A-z]+)\b\s+\b(my)\b'
        case 5:
            wordPattern = r'.*\b(always)\b\s+\b(feel)\b\s+\b([A-z]+)\b.*'
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

        elif word.lower() in NoSubKeywords:
            output.append(NoSubKeywords[word.lower()])

        elif len(word) > 0 and word[0].isupper() and word.lower() not in ExcludeNouns:
            # If it is a proper noun rank it
            substitution = getSubstitution(word, 2, line)
            if substitution:
                output.append(substitution)

    return output


def main():
    previousSubIndex = -1

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
            if sorted_output[0].pattern == previousSubIndex and len(sorted_output) > 1:
                response = sorted_output[1].output
                previousSubIndex = sorted_output[1].pattern
            else:
                response = sorted_output[0].output
                previousSubIndex = sorted_output[0].pattern

            response += "?"

        else:
            response = random.choice(Fallback)

        print("ELIZA> " + response)


if __name__ == "__main__":
    previousSubIndex = -1
    main()
