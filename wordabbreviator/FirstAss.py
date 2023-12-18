import numpy as np # Importing necessary libraries for the program
import re
import os

def word_least_letter_checker(theword, sorted_postn_values): # Function to check the least letter in a word
    least_letter = None
    least_letter_score = 1000
    index_count = 0

    for letter in theword[1:]: # Iterate through each letter in the word
        index_count += 1


        if sorted_postn_values[letter] < least_letter_score or least_letter is None:  # Check and update the least letter based on certain conditions
            least_letter = letter
            if index_count <= 2:
                least_letter_score = sorted_postn_values[letter] + index_count
            elif index_count > 2:
                least_letter_score = sorted_postn_values[letter] + 3


            if least_letter == theword[-1]: # Special case if the least letter is the last letter in the word
                for letter in theword[1:-1]:
                    if sorted_postn_values[letter] < 5:
                        least_letter = letter
                        if index_count <= 2:
                            least_letter_score = sorted_postn_values[letter] + index_count
                        elif index_count >= 3:
                            least_letter_score = sorted_postn_values[letter] + 3


            elif sorted_postn_values[least_letter] > 5 and theword[-1] != 'E': # Handle cases where the least letter is 'E'
                least_letter = theword[-1]
                least_letter_score = 5
            elif sorted_postn_values[least_letter] > 20 and theword[-1] == 'E':
                least_letter = theword[-1]
                least_letter_score = 20
            else:
                if index_count <= 2:
                    least_letter_score = sorted_postn_values[letter] + index_count
                elif index_count > 2:
                    least_letter_score = sorted_postn_values[letter] + 3

    return least_letter, least_letter_score, index_count


def least_score_checker_updated(name, sorted_postn_values): # Function to check the least score for each word in a name
    index_count = 0
    least_letter_tracker = {}
    least_score_tracker = {}
    names_split = name.split()


    for theword in names_split: # Iterate through each word in the name
        least_letter, least_letter_score, index_count = word_least_letter_checker(theword, sorted_postn_values)
        least_score_tracker[theword] = least_letter_score
        least_letter_tracker[theword] = least_letter
    return least_letter_tracker, least_score_tracker


def nameAbbreviator(name: str, sorted_postn_values): # Function to abbreviate a given name
    abb = ''
    score = -1
    abbreviations_dic = {}
    words = name.split()


    if len(words) == 1:  # Case: Only one word in the name
        for word in words:

            if len(word) < 3:  # Abbreviate based on word length and conditions
                abb = ''
                score = np.nan
            elif len(word) == 3:
                abb = word
                score_of_mid_letter = sorted_postn_values[word[1]]
                if abb[-1] == 'E':
                    score = score_of_mid_letter + 20
                else:
                    score = score_of_mid_letter + 5
            elif len(word) > 3:
                abb = word[0]
                least_letter, least_letter_score, least_index_count = word_least_letter_checker(word, sorted_postn_values)

                if least_letter == word[-1]: # Special case if the least letter is the last letter in the word
                    second_least_letter, second_least_letter_score, second_least_index_count = word_least_letter_checker(
                        word[:-1], sorted_postn_values)
                    abb += second_least_letter
                    abb += least_letter
                    score = least_letter_score + second_least_letter_score
                else:
                    second_least_letter, second_least_letter_score, second_least_index_count = word_least_letter_checker(
                        word.replace(least_letter, ''), sorted_postn_values)
                    if second_least_index_count < least_index_count:
                        abb += second_least_letter
                        abb += least_letter
                    else:
                        abb += least_letter
                        abb += second_least_letter
                    score += least_letter_score + second_least_letter_score


    elif len(words) >= 3: # Case  Three or more words in the name
        for word in words:
            abb += word[0]
        abb = abb[0:3]
        score = 0


    elif len(words) == 2 and len(name.replace(' ', '')) == 3:  # Case Two words in the name, total length is 3
        abb = name.replace(' ', '')
        for word in words:

            if len(word[0]) == 1:  # Abbreviate based on word length and conditions
                if abb[-1] == 'E':
                    score = 20
                else:
                    score = 5
            else:
                if abb[1] == 'E':
                    score = 20
                else:
                    score = 5


    elif len(words) == 2: # Case Two words in the name
        abb += words[0][0]
        least_letter_tracker, least_score_tracker = least_score_checker_updated(name, sorted_postn_values)
        least_letter_word = list(least_score_tracker.keys())[
            list(least_score_tracker.values()).index(min(least_score_tracker.values()))]
        if least_letter_word == words[1]:
            abb += words[1][0]
            abb += least_letter_tracker[least_letter_word]
            score = least_score_tracker[least_letter_word]
        elif least_letter_word == words[0]:
            abb += least_letter_tracker[least_letter_word]
            abb += words[1][0]
            score = least_score_tracker[least_letter_word]

    return abb, score


def abbreviator(path): # Main function to abbreviate names in a file
    with open(str(path)) as file:
        names = file.readlines()

    staged_names = []
    for name in names:
        staged_names.append(name.upper().replace("'", "").replace("\n", ""))
    cleaned_names = []
    for name in staged_names:

        name = re.sub('[^a-zA-Z \n]', ' ', name) # Remove special characters and extra spaces
        name = re.sub('\s+', ' ', name)
        name = name.lstrip().rstrip()
        cleaned_names.append(name)

    abbreviations_dic = {}
    abbreviatons_only = []

    letters = [] # Define a dictionary for letter positions in the alphabet
    values = []
    with open('resources/values.txt') as file: #Opening the values.txt which contains the values for each Alphabet
        for line in file:
            letters.append(line.rstrip().split()[0])  # takes each line, creates a letter-value pair ['A': '25'], slice out the letter (index of 0) and append to a list: letters
            values.append(int(line.rstrip().split()[1]))  # slices out the number (index of 1) from the letter-value pair ['A': '25'], converts to integer and append to a list: values
    postn_values = dict(zip(letters, values))  # create a dictionary from the two lists
    sorted_postn_values = dict(sorted(postn_values.items(), key=lambda x: x[1]))  # sorts the dictionary, this will be necessary later in Abbreviation score.


    for name in cleaned_names: # Iterate through each cleaned name and abbreviate
        abb, score = nameAbbreviator(name, sorted_postn_values)
        abbreviations_dic[name] = {abb: score}
        abbreviatons_only.append(abb)

    name_and_abb_dic = dict(zip(names, abbreviatons_only))

    names_and_abbs = []
    for name_only, abbreviation_only in name_and_abb_dic.items():
        names_and_abbs.append(name_only.split('\n')[0])
        names_and_abbs.append(abbreviation_only)

    input_filename = path.split('/')[-1].split('.')[0].lower()
    surname = 'Yashash'
    output_name = surname + '_' + input_filename + '_abbrevs.txt'

    with open('output/' + output_name, 'w') as file:
        file.write('\n'.join(names_and_abbs))

if __name__ == '__main__':
    while True:
        path = input('Please enter data filename and path: ') #to enter the input from user

        if os.path.exists(path):  # check if the file exists
            abbreviator(path)      # call the abbreviator function with the provided path
            break  # Exit the loop if a valid file is entered
        else:
            print(f"Error: File '{path}' does not exist. Please enter a valid filename and path.") #error message to user and to correct the file path
