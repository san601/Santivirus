import os
import sys
import pandas as pd

# Number of characters in the ASCII table, as we are searching on a hex string, the last character is f
NO_OF_CHARS = 103


def badCharHeuristic(string, size):
    """The preprocessing function for Boyer Moore's bad character heuristic

    Args:
        string (str): The pattern to be searched
        size (int): The size of the pattern

    Returns:
        A list of size NO_OF_CHARS with the last occurrence of each character in the pattern
    """
    # Initialize
    badChar = [-1] * NO_OF_CHARS

    # Fill the actual value of last occurrence
    for i in range(size):
        badChar[ord(string[i])] = i

    return badChar


def check(txt, pat):
    """The main function that searches for the pattern pat in the string txt using the Boyer Moore's bad character
    heuristic

    Args:
        txt (str): The string to be searched
        pat (str): The pattern to be searched for

    Returns:
        True if the pattern is found in the string, else False
    """

    m = len(pat)
    n = len(txt)

    badChar = badCharHeuristic(pat, m)

    s = 0
    while s <= n - m:
        j = m - 1

        while j >= 0 and pat[j] == txt[s + j]:
            j -= 1

        if j < 0:
            return True
        else:
            s += max(1, j - badChar[ord(txt[s + j])])


def scan(path):
    """Scans a file for malicious content and returns the type of malicious content

    Args:
        path: The path to the file to be scanned

    Returns:
        A tuple with the path to the file and the type of malicious content if found, else an empty tuple
    """

    # Initialize
    malicious_files = ()
    df = pd.read_csv('database.csv')

    # Open the file in binary mode and read the file as a hex string
    with open(path, 'rb') as f:
        bin = f.read().hex()

        # Iterating through the database to check if the file is malicious
        for index, data in df.iterrows():
            if check(bin, data['Signature']):
                malicious_files = (path, data['Type'])
                break
        if len(malicious_files) == 0:
            print(path, ' is clean.')

    return malicious_files


def scan_folder(folder_selected, type):
    """Scans a folder for malicious content and deletes it if found and type is 'delete'

    Args:
        folder_selected (str): The path to the folder to be scanned
        type (str): The type of action to be taken if malicious content is found.
            'delete' to scan and delete the malicious files
            'just scan' to just scan the folder
    """

    malicious_files = []
    # Iterating through the folder to scan each file
    for root, dir_name, file_name in os.walk(folder_selected):
        for f in file_name:
            path = os.path.join(root, f)
            temp = scan(path)
            if len(temp) > 0:
                malicious_files.append(temp)
                
    if len(malicious_files) == 0:
        print('\nSadly I couldn\'t find any malicious files. Your folder is clean.')
    else:
        # Printing the list of malicious files
        print('List of malicious files: ')
        for path, file_type in malicious_files:
            print(path, 'is a', file_type)
            
    if type == 'delete':
        print('Deleting malicious files.')
        for path, file_type in malicious_files:
            os.remove(path)
            print('Deletion complete.')


def scan_file(file_selected, type):
    """Scans a file for malicious content and deletes it if found and type is 'delete'

    Args:
        file_selected (str): The path to the file to be scanned
        type (str): The type of action to be taken if malicious content is found.
            'delete' to scan and delete the malicious file
            'just scan' to just scan the file
    """
    
    temp = scan(file_selected)
    if len(temp) > 0:
        print(file_selected, 'is a', temp[1])
        if type == 'delete':
            print('Deleting malicious file.')
            os.remove(file_selected)
            print('Deletion complete.')


if __name__ == '__main__':
    if len(sys.argv) > 2:
        if os.path.isfile(sys.argv[1]):
            scan_file(sys.argv[1], sys.argv[2])
        else:
            scan_folder(sys.argv[1], sys.argv[2])
