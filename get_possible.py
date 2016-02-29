
import copy

def not_possible(word, letters):
    letters_copy = copy.copy(letters)
    for letter in word:
        if letter not in letters_copy:
            return True
        letters_copy.remove(letter)
    return False

def build_dict(word_lengths, grid):
    letters = sorted(reduce(lambda x,y: x+y, grid))
    dictionary = []
    with open('/usr/share/dict/words', 'r') as wordfile:
        for word in wordfile:
            word = word.strip().upper()
            if len(word) not in word_lengths:
                continue
            if not_possible(word,letters):
                continue
            dictionary.append(word)
    return dictionary

def main():
    word_lengths = map(int, raw_input().strip().split(' '))
    n = input()
    grid = []
    for r in xrange(n):
        grid.append(map(str, raw_input().strip().split(' ')))

    possible_words = build_dict(word_lengths, grid)
    print "Poss words: ", len(possible_words)

    domains = []
    for length in word_lengths:
        domains.append(filter(lambda x: len(x) == length, possible_words))
    print map(len, domains)

if __name__ == '__main__':
    main()
