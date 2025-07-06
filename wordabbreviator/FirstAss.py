import numpy as np
import re
import os

def word_least_letter_checker(theword, sorted_postn_values):
    least_letter = None
    least_letter_score = 1000
    index_count = 0

    for i, letter in enumerate(theword[1:], start=1):
        # Calculate score for this letter with position penalty
        pos_value = sorted_postn_values.get(letter, 1000)
        penalty = i if i <= 2 else 3
        letter_score = pos_value + penalty

        if least_letter is None or letter_score < least_letter_score:
            least_letter = letter
            least_letter_score = letter_score
            index_count = i

    # Additional check for last letter logic as in original code:
    if least_letter == theword[-1]:
        for letter_inner in theword[1:-1]:
            val = sorted_postn_values.get(letter_inner, 1000)
            if val < 5:
                least_letter = letter_inner
                # recalc score with penalty
                idx = theword.index(letter_inner)
                penalty = idx if idx <= 2 else 3
                least_letter_score = val + penalty
                index_count = idx
                break

    # If least letter score is too high and last letter != 'E'
    last_letter = theword[-1]
    last_letter_val = sorted_postn_values.get(last_letter, 1000)
    if least_letter_score > 5 and last_letter != 'E':
        least_letter = last_letter
        least_letter_score = 5
        index_count = len(theword) - 1
    elif least_letter_score > 20 and last_letter == 'E':
        least_letter = last_letter
        least_letter_score = 20
        index_count = len(theword) - 1

    return least_letter, least_letter_score, index_count


def least_score_checker_updated(name, sorted_postn_values):
    least_letter_tracker = {}
    least_score_tracker = {}
    names_split = name.split()

    for theword in names_split:
        least_letter, least_letter_score, index_count = word_least_letter_checker(theword, sorted_postn_values)
        least_score_tracker[theword] = least_letter_score
        least_letter_tracker[theword] = least_letter
    return least_letter_tracker, least_score_tracker


def nameAbbreviator(name: str, sorted_postn_values):
    abb = ''
    score = -1
    words = name.split()

    if len(words) == 1:
        word = words[0]
        if not word.isalpha():
            return "Please enter a valid word (letters only).", np.nan
        if len(word) < 3:
            abb = ''
            score = np.nan
        elif len(word) == 3:
            abb = word
            score_of_mid_letter = sorted_postn_values.get(word[1], 1000)
            if abb[-1] == 'E':
                score = score_of_mid_letter + 20
            else:
                score = score_of_mid_letter + 5
        else:
            abb = word[0]
            least_letter, least_letter_score, least_index_count = word_least_letter_checker(word, sorted_postn_values)

            if least_letter == word[-1]:
                second_least_letter, second_least_letter_score, second_least_index_count = word_least_letter_checker(
                    word[:-1], sorted_postn_values)
                abb += second_least_letter + least_letter
                score = least_letter_score + second_least_letter_score
            else:
                second_least_letter, second_least_letter_score, second_least_index_count = word_least_letter_checker(
                    word.replace(least_letter, ''), sorted_postn_values)
                if second_least_index_count < least_index_count:
                    abb += second_least_letter + least_letter
                else:
                    abb += least_letter + second_least_letter
                score = least_letter_score + second_least_letter_score

    elif len(words) >= 3:
        for word in words:
            abb += word[0]
        abb = abb[:3]
        score = 0

    elif len(words) == 2 and len(name.replace(' ', '')) == 3:
        abb = name.replace(' ', '')
        for word in words:
            if len(word) == 1:
                if abb[-1] == 'E':
                    score = 20
                else:
                    score = 5
            else:
                if abb[1] == 'E':
                    score = 20
                else:
                    score = 5

    elif len(words) == 2:
        abb += words[0][0]
        least_letter_tracker, least_score_tracker = least_score_checker_updated(name, sorted_postn_values)
        least_letter_word = min(least_score_tracker, key=least_score_tracker.get)
        if least_letter_word == words[1]:
            abb += words[1][0] + least_letter_tracker[least_letter_word]
            score = least_score_tracker[least_letter_word]
        else:
            abb += least_letter_tracker[least_letter_word] + words[1][0]
            score = least_score_tracker[least_letter_word]

    else:
        abb = ''
        score = np.nan

    return abb, score


def abbreviator(path):
    if not os.path.exists('output'):
        os.makedirs('output')

    with open(str(path), encoding='utf-8') as file:
        names = file.readlines()

    staged_names = []
    for name in names:
        staged_names.append(name.upper().replace("'", "").replace("\n", ""))

    cleaned_names = []
    for name in staged_names:
        name = re.sub('[^a-zA-Z \n]', ' ', name)
        name = re.sub('\s+', ' ', name)
        name = name.strip()
        cleaned_names.append(name)

    letters = []
    values = []
    with open('resources/values.txt', encoding='utf-8') as file:
        for line in file:
            parts = line.rstrip().split()
            if len(parts) == 2:
                letters.append(parts[0])
                values.append(int(parts[1]))
    postn_values = dict(zip(letters, values))
    sorted_postn_values = dict(sorted(postn_values.items(), key=lambda x: x[1]))

    output_name = f"Abrivated_{os.path.basename(path).split('.')[0].lower()}_abbrevs.txt"

    with open(os.path.join('output', output_name), 'w', encoding='utf-8') as file:
        for name in cleaned_names:
            abb, score = nameAbbreviator(name, sorted_postn_values)
            line = f"{name}: {abb} (Score: {score if not np.isnan(score) else 'N/A'})"
            file.write(line + '\n')
            print(line)  # Print to console

# For direct testing
if __name__ == '__main__':
    while True:
        path = input('Please enter data filename and path: ')
        if os.path.exists(path):
            abbreviator(path)
            print(f"Abbreviations saved in 'output' folder.")
            break
        else:
            print(f"Error: File '{path}' does not exist. Please enter a valid filename and path.")
