'''
Zach Dellimore V00980652
02/03/2025

Problem:
    Implement an ELIZA chatbot to talk with the user only using keyword search
    and substitutions

Process:
    1. Parse input for keywords
    2. For each keyword check all their possible substitutions
    3. Respond with the highest ranked substitution
        4. If no keywords are found respond with Tell me more about that

Example:
    ELIZA> Hello my name is Eliza, what is your name?
    USER> Zach
    ELIZA> Hello Zach, what did you want to talk about today?
    Zach> My cat
    ELIZA> Can you tell me about your cat?
    Zach> His name is Reginald and he makes me feel inadequate
    ELIZA> Why do you feel inadequate?
    Zach> He makes fun of me everyday and calls me names
    ELIZA> Please go on
'''

import copy
import re
import random


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
        Substitution("", r"Can you tell me about your \1", 5),
        Substitution("", r"Why do you \1 \2", 6),
        Substitution("", r"How long have you been \1", 5),
        Substitution("", r"Can you tell me about your \2", 4),
        Substitution("", r"Can you tell me about \1", 4),
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

# These keywords don't need a regex substitution
NoSubKeywords = {
        "because": Substitution("Is that the real reason", "",  3),
        "always": Substitution("Can you give me an example of a time that happened", "", 3),
        "everyday": Substitution("When was the last time this happened", "", 3),
        "think": Substitution("What caused you to think that", "", 4),
        "sometimes": Substitution("Can you give me an example of a time that happened", "", 3),
        "today": Substitution("Can you tell me about your day", "", 3),
        "it": Substitution("What does it refer to", "", 1),
        "maybe": Substitution("Why are you not certain", "", 1),
        "hello": Substitution("Hello, what is it you'd like to talk about", "", 1)
        }

ExcludeNouns = {
        "the",
        "hello",
        "i",
        "he",
        "his",
        "hers",
        "he's",
        "she",
        "she's",
        "they",
        "i've",
        "there",
        "last"
        }

Fallback = [
        "Can you elaborate?",
        "Please go on",
        "Tell me more"
        ]

name = "User"


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

    # Get all words
    words = re.findall(r'\b\w+\b', line)

    for word in words:
        # Check if the word is in any of the keyword dictionaries
        if word.lower() in TopKeywords:
            substitutions = TopKeywords[word.lower()]
            for substitutionIndex in substitutions:
                substitution = getSubstitution(word, substitutionIndex, line)
                if substitution:
                    output.append(substitution)

        elif word.lower() in NoSubKeywords:
            output.append(NoSubKeywords[word.lower()])

        elif len(word) > 0 and word[0].isupper() and word.lower() not in ExcludeNouns:
            # If it is a proper noun rank it, this has a tendency to be wrong
            substitution = getSubstitution(word, 4, line)
            if substitution:
                output.append(substitution)

    return output


def main():
    previousSubIndex = -1

    # Main loop of chatbot
    while (True):
        # First get user input
        line = input(name + "> ")

        if line == "":
            print("Exiting")
            break

        # Then parse user input and generate a response
        output = ParseInput(line)

        sorted_output = sorted(output, reverse=True,
                               key=lambda substitution: substitution.rank)

        response = ""

        # Get the top rated output and try not to choose the same one from last time
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

    # Get the user's name
    print("ELIZA> Hello my name is Eliza, what is your name?")
    line = input("USER> ")
    words = line.split(' ')
    name = words[-1]
    print("ELIZA> Hello " + name + ", what did you want to talk about today?")

    main()
