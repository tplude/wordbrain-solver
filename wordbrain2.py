
import pprint
import itertools
import copy

def not_possible(word, letters):
    letters_copy = copy.deepcopy(letters)
    for letter in word:
        if letter not in letters_copy:
            return True
        letters_copy.remove(letter)
    return False

def build_dict(word_lengths, grid):
    letters = sorted(reduce(lambda x,y: x+y, grid))
    dictionary = []
    with open('./wiki-100k.txt','r') as wordfile:
        for word in wordfile:
            word = word.strip().upper()
            if len(word) not in word_lengths:
                continue
            if not_possible(word, letters):
                continue
            #dictionary[word] = reduce(lambda x, y: x+y, sorted([l for l in word]))
            dictionary.append(word)
    return dictionary

def grid_contains_all(choice, grid_letters):
    letters_of_choices = sorted([l for l in reduce(lambda x,y: x+y, choice)])
    return (grid_letters == letters_of_choices)

def reduce_possibilities(poss_words, grid, word_lens):
    domains = []
    for length in word_lens:
        domains.append(filter(lambda x: len(x) == length, poss_words))
    print map(len, domains)

    grid_letters = sorted(reduce(lambda x, y: x+y, grid))
    possibles = set([])
    for choice in itertools.product(*domains):
        if grid_contains_all(choice, grid_letters):
            possibles.add(choice)
    return possibles

def recursive_traverse(word, row, col, grid, moves, results):
    if len(word) == 0:
        results.append(grid)
        return results
    for move in moves:
        new_row = row + move[0]
        new_col = col + move[1]
        if new_row < 0 or new_row > len(grid)-1:
            continue
        if new_col < 0 or new_col > len(grid)-1:
            continue
        if grid[new_row][new_col] == word[:1]:
            grid_copy = copy.deepcopy(grid)
            grid_copy[new_row][new_col] = ''
            results = recursive_traverse(word[1:], new_row, new_col, grid_copy, moves, results)
    return results

def reduce_grid(grid):
    cols = [map(lambda x: x[col], grid) for col in range(len(grid))]
    filtered = [filter(lambda x: x != '', c) for c in cols]
    for fc in filtered:
        for nums in range(len(grid) - len(fc)):
            fc.insert(0,'')
    return [map(lambda x: x[col], filtered) for col in range(len(grid))]

def ingest_word(word, grid):
    moves = [(1,0), (-1,0), (0,-1), (0,1), (1,-1), (1,1), (-1,1), (-1,-1)]
    resultant_grids = []
    for r in range(len(grid)):
        for c in range(len(grid)):
            if grid[r][c] == word[:1]:
                grid_copy = copy.deepcopy(grid)
                grid_copy[r][c] = ''
                resultant_grids = recursive_traverse(word[1:], r, c, grid_copy, moves, resultant_grids)
    return map(reduce_grid, resultant_grids)

def traverse_grid(words, grids, winning_grid):
    if len(words) == 0:
        if winning_grid in grids:
            return True
        else:
            return False
    for word in words:
        for grid in grids:
            resulting_grids = ingest_word(word,grid)
            if traverse_grid(words[1:], resulting_grids, winning_grid):
                return True

def legal_moves(word_tuples, grid):
    final_tuples = set([])
    winning_grid = [['' for c in range(len(grid))] for r in range(len(grid))]
    for wt in word_tuples:
        if traverse_grid(wt, [grid], winning_grid):
            final_tuples.add(wt)
    return final_tuples

def main():
    word_lengths = map(int, raw_input().strip().split(' '))

    max_len = max(word_lengths)
    n = input()
    grid = []
    for r in xrange(n):
        grid.append(map(str, raw_input().strip().split(' ')))

    possible_words = build_dict(word_lengths, grid)
    possible_tuples = reduce_possibilities(possible_words, grid, word_lengths)
    legal_sequences = legal_moves(possible_tuples, grid)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(legal_sequences)

if __name__ == '__main__':
    main()
