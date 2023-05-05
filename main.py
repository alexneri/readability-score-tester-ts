# Flesch-kincaid text analyzer
# For use with technical documentation with code.
# This app received multi-line input, strips away the code, and then analyzes the text
# using the Flesch-Kincaid readability test.
#
# Created by Alexander NV Neri on 04 May 2023
# https://github.com/alexneri/readability-score-tester-ts


import os
import re

def clear_screen():
    os.environ['TERM'] = 'xterm'
    os.system('cls' if os.name == 'nt' else 'clear')

def get_rating_comment(score):
    if score >= 100:
        return '5th grade level - Very easy to read. Easily understood by an average 11-year-old student.'
    elif score >= 90:
        return '6th grade level - Very easy to read. Easily understood by an average 11-year-old student'
    elif score >= 80:
        return '7th grade level - Fairly easy to read.'
    elif score >= 70:
        return '8th & 9th grade - Plain English. Easily understood by 13- to 15-year-old students.'
    elif score >= 60:
        return '10th - 12th grade - Fairly difficult to read.'
    elif score >= 50:
        return 'College - Difficult to read.'
    elif score >= 30:
        return 'College grad - Very difficult to read. Best understood by university graduates.'
    else:
        return 'Professional - Extremely difficult to read. Best understood by university graduates.'

class FleschKincaid:
    sentence_endings = '.!?'
    vowels = 'AEIOUaeiou'

    @staticmethod
    def calculate(text: str) -> float:
        words = re.split(r'\s+', text)
        word_count = len(words)
        syllable_count = sum(FleschKincaid.count_syllables(word) for word in words)
        sentence_count = sum(c in FleschKincaid.sentence_endings for c in text)

        avg_words_per_sentence = word_count / sentence_count
        avg_syllables_per_word = syllable_count / word_count

        return 206.835 - 1.015 * avg_words_per_sentence - 84.6 * avg_syllables_per_word

    @staticmethod
    def count_syllables(word: str) -> int:
        count = 0
        prev_vowel = False

        for char in word:
            is_vowel = char in FleschKincaid.vowels

            if is_vowel and not prev_vowel:
                count += 1

            prev_vowel = is_vowel

        if word.endswith('e'):
            count -= 1

        return max(count, 1)

def filter_out_code(input: str) -> str:
    lines = input.split('\n')
    filtered_lines = [line for line in lines if not line.startswith('```')]
    return '\n'.join(filtered_lines)

def main():
    while True:
        input_text = input("Enter multi-line text (end with two consecutive blank lines):\n")
        input_lines = []
        blank_line_count = 0

        while True:
            if not input_text:
                blank_line_count += 1
            else:
                blank_line_count = 0

            if blank_line_count == 2:
                break

            input_lines.append(input_text)
            input_text = input()

        text = '\n'.join(input_lines)
        score = FleschKincaid.calculate(text)
        print(f'Flesch-Kincaid readability score: {score:.2f}')
        print('Rating comment:')
        print(get_rating_comment(score))

        user_input = input('Do you want to analyze new text? (yes/no): ').lower()
        if user_input == 'yes':
            clear_screen()
        else:
            break

if __name__ == '__main__':
    main()