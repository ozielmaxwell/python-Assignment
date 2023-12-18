import re

def load_letter_values(values_file_path="values.txt"):
    """
    Load letter values from the specified file.
    
    Returns:
    A dictionary where keys are letters and values are corresponding scores.
    """
    with open(values_file_path) as values_file:
        return {line.split()[0]: int(line.split()[1]) for line in values_file}

def is_last_letter(name, i):
    """
    Check if the character at position i in name is the last letter of a word in CamelCase.

    Returns:
    True if name[i] is the last letter of a word.
    """
    return i == len(name) - 1 or name[i + 1].isupper()

def calculate_scores_in_word(name_camel_case, letter_values):
    """
    Calculate values for each character in a name. Name is expected to be in CamelCase.

    Returns:
    A list of scores where list[i] is the score for name[i].
    """
    name = name_camel_case
    char_word_pos = 0
    scores = [-1] * len(name)

    for i in range(len(name)):
        if char_word_pos == 0:
            scores[i] = 0
        elif is_last_letter(name, i):
            scores[i] = 5 if name[i].upper() != 'E' else 20
        else:
            bonus = min(char_word_pos, 3)  # Use min to handle cases where char_word_pos is greater than 3
            scores[i] = letter_values[name[i].upper()] + bonus

        char_word_pos = 0 if is_last_letter(name, i) else char_word_pos + 1

    return scores

def reformat_name(name):
    """ 
    Clean the name as requested in the assignment brief and turn it into CamelCase.

    Returns:
    The reformatted name.
    """
    name = re.sub("'+", "", name)  # Remove apostrophes
    name = re.sub("[^a-zA-Z]+", " ", name)  # Replace non-letter chars with spaces
    name = name.title()  # Ensure titlecase
    name = re.sub(" ", "", name)  # Remove spaces
    return name

def create_abbreviations(name, letter_values):
    """
    Generate all possible abbreviations for one name along with their scores.

    Returns:
    A dictionary {abbreviation: score}.
    """
    name = reformat_name(name)
    scores = calculate_scores_in_word(name, letter_values)
    abbreviations = {}

    for i in range(1, len(name) - 1):
        for j in range(i + 1, len(name)):
            abbreviation = f"{name[0]}{name[i]}{name[j]}".upper()
            score = 0 + scores[i] + scores[j]

            if abbreviation not in abbreviations or score < abbreviations[abbreviation]:
                abbreviations[abbreviation] = score

    return abbreviations

def create_all_abbreviations(file_path, letter_values):
    """
    Read a file at file_path and create abbreviations for each line in it.

    Returns:
    A list of pairs of strings and dictionaries: [(name, {abbreviation: score})].
    """
    with open(file_path) as infile:
        return [(line.rstrip("\n"), create_abbreviations(line.rstrip("\n"), letter_values)) for line in infile]

def find_duplicates(all_abbreviations):
    """
    Creates a list of abbreviations that occur twice across any names.
    """
    instances = {}
    for _, abbreviations in all_abbreviations:
        for abbreviation in abbreviations.keys():
            instances[abbreviation] = 1 if abbreviation not in instances else instances[abbreviation] + 1
            
    return {abbreviation for abbreviation in instances.keys() if instances[abbreviation] > 1}

def remove_duplicates(all_abbreviations, duplicates):
    """
    Create a new all_abbreviations-like list but with any abbreviation appearing in duplicates removed.

    Returns:
    [(name, {abbreviation: score})] from all_abbreviations but with select abbreviations removed.
    """
    return [(name, {abbreviation: score for abbreviation, score in abbreviations.items() if abbreviation not in duplicates}) for name, abbreviations in all_abbreviations]

def find_and_remove_duplicates(all_abbreviations):
    """
    Removes any abbreviations that are not unique by calling find_duplicates() and remove_duplicates().
    If an abbreviation occurs more than once, all its instances are removed and not just the surplus ones.

    Returns:
    all_abbreviations but with duplicate abbreviations removed.
    """
    duplicates = find_duplicates(all_abbreviations)
    return remove_duplicates(all_abbreviations, duplicates)

def choose_best_abbreviations_inner(abbreviations):
    """
    Find the abbreviation with the lowest score for one name's set of abbreviations.
    If multiple abbreviations have the same score, returns all (or none if no abbreviations provided).

    Returns:
    A list of abbreviations (usually of length 1, but sometimes 0 or 2+).
    """
    min_score = float('inf')
    best_abbreviations = []

    for abbreviation, score in abbreviations.items():
        if score < min_score:
            best_abbreviations = [abbreviation]
            min_score = score
        elif score == min_score:
            best_abbreviations.append(abbreviation)

    return best_abbreviations

def choose_best_abbreviations(filtered):
    """
    Find the lowest-scored abbreviation for each name.

    Returns:
    A list of pairs [(name, [best_abbreviation, ])].
    """
    return [(name, choose_best_abbreviations_inner(abbreviations)) for name, abbreviations in filtered]

def write_best_abbreviations_to_file(best_abbreviations, file_path):
    """
    Writes the output of choose_best_abbreviations() into a file in the specified format.
    """
    with open(file_path, 'w') as outfile:
        for name, abbreviations in best_abbreviations:
            outfile.write(f"{name}\n")
            outfile.write(f"{(' '.join(abbreviations))}\n")

def main():
    """
    Entry point of the program, does what was specified in the brief by calling the other functions.
    """
    file_name = input("Enter the name of your text file(without the extention .txt): ")
    letter_values = load_letter_values()
    all_abbreviations = create_all_abbreviations(f"{file_name}.txt", letter_values)
    filtered = find_and_remove_duplicates(all_abbreviations)
    print(filtered)
    best_abbreviations = choose_best_abbreviations(filtered)
    write_best_abbreviations_to_file(best_abbreviations, f"Maxwell_{file_name}_abbrevs.txt")

# to enable running this file either by itself or as a module
if __name__ == "__main__":
    main()
