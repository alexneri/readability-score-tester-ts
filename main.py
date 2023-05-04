import sys
import re

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

def suggest_improvements(text: str) -> list[str]:
    suggestions = [
        '1. Try to use shorter sentences.',
        '2. Replace complex words with simpler alternatives.',
        '3. Use active voice instead of passive voice.',
        '4. Break down complex ideas into smaller, easier-to-understand concepts.',
        '5. Use examples and analogies to explain complex topics.'
    ]

    return suggestions

def get_input() -> str:
    print('Enter multi-line text (end with two consecutive blank lines):')
    input_lines = []

    blank_line_count = 0
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            blank_line_count += 1
        else:
            blank_line_count = 0

        if blank_line_count == 2:
            break

        input_lines.append(line)

    return '\n'.join(input_lines)

def main():
    while True:
        input_text = get_input()
        filtered_text = filter_out_code(input_text)
        score = FleschKincaid.calculate(filtered_text)
        suggestions = suggest_improvements(filtered_text)

        print(f'Flesch-Kincaid readability score: {score:.2f}')
        print('Suggestions for improvement:')
        print('\n'.join(suggestions))

        user_input = input('Do you want to analyze new text? (yes/no): ').strip().lower()
        if user_input != 'yes':
            break

if __name__ == '__main__':
    main()