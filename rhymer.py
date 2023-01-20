# import libraries
import requests
import re
import argparse

DATAMUSE_API = "https://api.datamuse.com/words"

def get_ryhmes(word: str, option='rel_rhy', max=100, api_endoint=DATAMUSE_API):
    """
    This function takes in a word and an option for the type of rhyme to be used, and an endpoint for the API to be used.
    It then makes a request to the API with the specified parameters, and returns a list of words that rhyme with the input word.
    
    Args:
        word (str): The word to find rhymes for
        option (str, optional): The type of rhyme to be used. Defaults to 'rel_rhy'
        max (int, optional): The maximum number of rhymes to return. Defaults to 100
        api_endoint (str, optional): The endpoint for the API to be used. Defaults to "https://api.datamuse.com/words"
        
    Returns:
        list(str): A list of words that rhyme with the input word
    """
    # Create a dictionary to store the parameters for the API request
    parameter = {}
    # Add the option and word to the parameter dictionary
    parameter[option] = word
    parameter['max'] = max
    # Make a GET request to the API with the specified parameters
    request = requests.get(api_endoint, parameter)
    # Print a message indicating that the program is searching for rhymes
    print(f"checking [{option}] for {word}...")
    # Get the JSON response from the API
    rhyme = request.json()
    # Return a list of words from the JSON response
    return [elt['word'] for elt in rhyme]


# getting all ryhmes from api.datamuse.com

def get_last_word(sentence: str):
    """
    This function takes in a sentence as a string and returns the last word of that sentence.
    It removes any special characters like ( ) . from the sentence and returns last word
    Args:
        sentence (str): Sentence as a string

    Returns:
        str: The last word of the sentence
    """
    # Replace all occurances of ')' with an empty string
    sentence = sentence.replace(')', '')
    # Replace all occurances of '(' with an empty string
    sentence = sentence.replace('(', '')
    # Replace all occurances of '.' with a space
    sentence = sentence.replace('.', ' ')
    # Split the sentence using the regex pattern '\W+' which will match all non-word characters
    words = re.split(r'\W+', sentence)
    # Return the last word in the list
    return words[-1]

def main(filename, output_file='output.txt'):
    """
    The main function takes a file name and an optional output file name.
    It reads the input file, and groups the lines based on rhyme.
    It then writes the grouped lines to the output file
    Args:
        filename (str): The name of the input file
        output_file (str, optional): The name of the output file. Defaults to 'output.txt'.
    """
    # Initialize an empty list to store the output
    output = []
    i = 0
    # Open the input file
    with open(filename) as f:
        # Read all the lines from the file
        lines = f.readlines()
        # Remove any lines that are shorter than 2 characters
        lines = [line for line in lines if len(line) > 2]

        # Keep running while there are still lines to process
        while len(lines) > 0:
            # Get the last word of the first line
            last_word = get_last_word(lines[0].strip('\n'))

            # Get a list of words that rhyme with the last word
            rhymes = get_ryhmes(last_word)
            # Append a new empty list to the output list
            output.append([])
            # Add the first line to the last list in the output
            output[i].append(lines[0])
            # Remove the first line from the input list
            lines.remove(lines[0])
            # Make a copy of the input list
            lines_swap = lines.copy()
            # Iterate over the copy of the input list
            for s in lines_swap:
                # Get the last word of the current line
                lw = get_last_word(s.strip('\n'))
                # Check if the last word of the current line is in the list of rhyming words or if it is the same as the last word of the first line
                if lw in rhymes or lw == last_word:
                    # If it is, remove the line from the input list
                    lines.remove(s)
                    # And add it to the current group in the output list
                    output[i].append(s)

            i += 1
    # Sort the output list by the number of lines in each group, in descending order
    output.sort(key=len, reverse=True)
    # output has lines
    # Open the output file for writing
    with open(output_file, 'w') as f:
        # Iterate over the groups of lines in the output
        for lines in output:
            # Iterate over the lines in each group
            for line in lines:
                # Write the line to the output file, with a newline character if one is not already present
                f.write(line + '\n'*('\n' not in line))
            # Write an additional newline character after each group of lines
            f.write('\n')

if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(
        prog='rhymer.py',
        description='RhymerV0.2 script will sort sentences acording to their rhymes',
        epilog='This script uses datamuse.com API.')
    # Add an argument for the input file
    parser.add_argument('input_filename', help="Input file containing lines.")
    # Add an argument for the output file
    parser.add_argument('output_filename', default='output.txt',
                        help="output file where the sorted poem is stored.")
    # Parse the command line arguments
    args = parser.parse_args()
    try:
        # Call the main function with the input and output filenames
        main(args.input_filename, output_file=args.output_filename)
        # Print a message indicating that the sorting was successful
        print(f"[OK] sorted in {args.output_filename}")
    except Exception as e:
        # Print a message indicating the proper usage of the script
        print(f"{str(e)}/n[ERROR] usage: python rhymer.py sample.txt output.txt")
