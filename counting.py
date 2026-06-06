"""
Give a string representing a sentence:
Count letters
Count words
Count vowels
Frequency of letters
Frequency of vowels
Histogram of letters
"""

import string


def count_letters(sentence):
    count = 0
    for letter in sentence:
        # if letter not in '.,?!;:':
        if letter not in string.punctuation:
            count += 1
    return count


def count_words(sentence):
    words = sentence.split(' ')
    return len(words)


def count_vowels(sentence):
    count = 0
    for letter in sentence:
        if letter.lower() in 'aeiou':
            count += 1
    return count


def letter_frequency(sentence):
    frequency = {}
    for letter in sentence:
        if letter.lower() in string.ascii_lowercase:
            if letter.lower() in frequency:
                frequency[letter.lower()] += 1
            else:
                frequency[letter.lower()] = 1
    return frequency


def vowel_frequency(sentence):
    frequency = {}
    for letter in sentence:
        # Populate the frequency dictionary with vowel count
        if letter.lower() in 'aeiou':
            if letter in frequency:
                frequency[letter.lower()] += 1
            else:
                frequency[letter.lower()] = 1
    return frequency


def letter_histogram(sentence):
    histogram = {}

    # Initialize the histogram
    for letter in string.ascii_lowercase:
        histogram[letter] = 0

    # Populate the histogram
    for letter in sentence:
        if letter.lower() in histogram:
            histogram[letter.lower()] += 1

    return histogram


def main():
    # sentence = "It was a dark and stormy night."
    sentence = 'The quick brown fox jumps over the lazy dog.'

    print(f"Letter count = {count_letters(sentence)}")
    print(f"Word count = {count_words(sentence)}")
    print(f"Vowel count = {count_vowels(sentence)}")

    print("\nLetter frequency:")
    for letter, frequency in sorted(letter_frequency(sentence).items()):
        print(f"{letter}: {frequency}")

    print("\nVowel frequency:")
    for letter, frequency in sorted(vowel_frequency(sentence).items()):
        print(f"{letter}: {frequency}")

    print("\nLetter histogram:")
    for letter, frequency in letter_histogram(sentence).items():
        print(f"{letter}: {frequency}")


if __name__ == '__main__':
    main()
