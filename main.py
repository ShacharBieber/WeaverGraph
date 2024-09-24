from nltk.corpus import words
import typing
import string
from collections import deque
import argparse

LETTERS = list(string.ascii_lowercase)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--source_word',
        type=str,
        help='The source word'
    )
    parser.add_argument(
        '-t',
        '--target_word',
        type=str,
        help='The target word'
    )
    parser.add_argument(
        '-l',
        '--word_length',
        type=int,
        default=4,
        help='The word length (4 is the default. 5 is another common choice)'
    )
    parser.add_argument(
        '-p',
        '--dictionary_path',
        type=str,
        default=None,
        help='Path to a given dictionary. The default is the nltk corpus'
    )
    return parser.parse_args()


class WordVertex:
    def __init__(self, word):
        self.word = word
        self.neighbors = set()

    def __str__(self):
        return f'WordVertex: {self.word}, neighbors={[neighbor.word for neighbor in self.neighbors]}'

    def __repr__(self):
        return f'WordVertex: {self.word}, neighbors={[neighbor.word for neighbor in self.neighbors]}'

    def get_neighbors_strs(self, words: set) -> list:
        neighbor_list = []
        for position in range(0, len(self.word)):
            for letter_replacement in LETTERS:
                neighbor_candidate = f'{self.word[:position]}{letter_replacement}{self.word[position + 1:]}'
                if neighbor_candidate in words and neighbor_candidate != self.word:
                    neighbor_list.append(neighbor_candidate)
        return neighbor_list

    def check_is_neighbor(self, other, words) -> bool:
        neighbors = self.get_neighbors_strs(words)
        if other.word in neighbors:
            return True


def get_words(word_length: int) -> set:
    word_list = words.words()
    words_set = set()
    for word in word_list:
        word_candidate = word.lower()
        if len(word_candidate) == word_length:
            words_set.add(word_candidate)
    return words_set


def read_dictionary(word_length: int, dictionary_path: str) -> set:
    words_set = set()
    with open(dictionary_path, 'r') as infile:
        for word in infile.readlines():
            word_candidate = word[:-1].lower()
            if len(word_candidate) == word_length:
                words_set.add(word_candidate)
    return words_set


def get_graph(word_length: int, dictionary_path: str = None) -> dict:
    if not dictionary_path:
        words_set = get_words(word_length)
    else:
        words_set = read_dictionary(word_length=word_length, dictionary_path=dictionary_path)
    word_to_vertex_dict = {}
    for word in words_set:
        word_vertex = WordVertex(word=word)
        word_vertex.neighbors = word_vertex.get_neighbors_strs(words=words_set)
        word_to_vertex_dict[word] = word_vertex
    for word, word_vertex in word_to_vertex_dict.items():
        vertex_neighbors = set()
        for neighbor in word_vertex.neighbors:
            vertex_neighbors.add(word_to_vertex_dict[neighbor])
        word_vertex.neighbors = vertex_neighbors
    return word_to_vertex_dict


def bfs_path_finder(words_graph_dict: dict, source_word: str, target_word: str):
    origin_dict = {word: '' for word in words_graph_dict.keys()}
    visited_words = {word: False for word in words_graph_dict.keys()}
    queue = deque()
    visited_words[source_word] = True
    queue.append(words_graph_dict[source_word])
    while queue:
        current_vertex = words_graph_dict[queue.popleft().word]
        visited_words[current_vertex.word] = True
        if current_vertex.word == target_word:
            print("Found a solution!")
            solution_str = target_word
            solution_count = 1
            while origin_dict[current_vertex.word]:
                solution_str = f'{solution_str} <- {origin_dict[current_vertex.word]}'
                solution_count += 1
                current_vertex = words_graph_dict[origin_dict[current_vertex.word]]
            print(solution_str)
            print(f'{solution_count} steps.')
            return True
        else:
            for neighbor in current_vertex.neighbors:
                if not visited_words[neighbor.word]:
                    queue.append(neighbor)
                    if not origin_dict.get(neighbor.word):
                        origin_dict[neighbor.word] = current_vertex.word
    print(f'There is no path from {source_word} to {target_word} :(')
    return False


def main():
    parsed_arguments = parse_arguments()
    source_word, target_word = parsed_arguments.source_word, parsed_arguments.target_word
    word_length, dictionary_path = parsed_arguments.word_length, parsed_arguments.dictionary_path
    word_to_vertex_dict = get_graph(word_length=word_length, dictionary_path=dictionary_path)
    bfs_path_finder(
        words_graph_dict=word_to_vertex_dict,
        source_word=source_word,
        target_word=target_word
    )


if __name__ == '__main__':
    main()
