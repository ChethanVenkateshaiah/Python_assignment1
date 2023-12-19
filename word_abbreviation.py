import numpy as np  # Import the numpy library for numerical operations
import re  # Import the regular expression library for text manipulation
import os  # Import the os library for file and directory operations

# Function to load letter values from a file
def load_letter_values(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return None

    alphabet, scores = [], []
    try:
        with open(file_path) as file:
            for line in file:
                parts = line.strip().split()
                alphabet.append(parts[0])  # Store the alphabet letter
                scores.append(int(parts[1]))  # Store the corresponding score
        return dict(zip(alphabet, scores))  # Create a dictionary mapping letters to scores
    except Exception as error:
        print(f"Error reading the file: {error}")
        return None

# Function to format a name by removing non-alphabetic characters and converting to uppercase
def format_name(name):
    formatted_name = re.sub('[^A-Z ]', ' ', name.upper().replace("'", ""))
    return re.sub('\s+', ' ', formatted_name).strip()

# Function to calculate the score of an abbreviation for a name
def calculate_score(letter, position, is_last, letter_scores):
    if position == 0:  # The first letter of a word has a score of 0
        return 0
    if is_last:
        return 20 if letter == 'E' else 5  # Score for the last letter in a word
    return (1 if position == 1 else 2 if position == 2 else 3) + letter_scores[letter]

# Function to find the best abbreviation for a name
def find_best_abbreviation(name, letter_scores):
    words = name.split()  # Split the name into words
    best_score = np.inf  # Initialize the best score as positive infinity
    best_abbrev = None  # Initialize the best abbreviation as None
    for i in range(len(name)):
        if not name[i].isalpha(): continue  # Skip non-alphabetic characters
        for j in range(i + 1, len(name)):
            if not name[j].isalpha(): continue  # Skip non-alphabetic characters
            for k in range(j + 1, len(name)):
                if not name[k].isalpha(): continue  # Skip non-alphabetic characters
                abbrev = name[i] + name[j] + name[k]  # Generate an abbreviation
                score = calculate_abbreviation_score(abbrev, name, words, letter_scores)
                if score < best_score:
                    best_score = score
                    best_abbrev = abbrev
    return best_abbrev

# Function to calculate the abbreviation score for a name
def calculate_abbreviation_score(abbrev, full_name, words, letter_scores):
    score = 0
    for index, letter in enumerate(abbrev[1:], start=1):
        position_in_word, is_last = get_letter_position(full_name, words, letter, index)
        score += calculate_score(letter, position_in_word, is_last, letter_scores)
    return score

# Function to get the position of a letter in a name and whether it is the last letter in a word
def get_letter_position(full_name, words, letter, index):
    letter_position = full_name.find(letter, index)
    cumulative_length = 0
    for word in words:
        if cumulative_length <= letter_position < cumulative_length + len(word):
            position_in_word = letter_position - cumulative_length
            is_last = position_in_word == len(word) - 1
            return position_in_word, is_last
        cumulative_length += len(word) + 1  # Including space
    return 0, False

# Main function
def main():
    values_file_path = r'C:\Users\Chethan\Desktop\Python word abbreviation\values.txt'  # Path to the file containing letter values
    letter_scores = load_letter_values(values_file_path)  # Load letter values from the file
    if letter_scores is None:
        return

    input_filename = input("Enter the name of the input file (e.g., names.txt): ")  # Get the input filename from the user
    names = [format_name(line.strip()) for line in open(input_filename)]  # Read and format names from the input file

    surname = input("Enter your surname: ")  # Get the user's surname
    output_filename = f"{surname.lower()}_{os.path.splitext(input_filename)[0]}_abbrevs.txt"  # Generate the output filename

    with open(output_filename, 'w') as file:
        for name in names:
            best_abbrev = find_best_abbreviation(name, letter_scores)  # Find the best abbreviation for each name
            file.write(f"{name}\n{best_abbrev}\n")  # Write the name and its abbreviation to the output file

    print(f"Output written to {output_filename}")  # Print the output filename

if __name__ == "__main__":
    main()  # Call the main function if the script is executed directly