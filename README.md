This code solves the Weaver game (https://wordwormdormdork.com/) using BFS.
The default is using the nltk dictionary, but it can also be given a local dictionary file (see en_4_letters.txt for an example).

## How to Run

1. Download or clone this repository.
2. Run the script in a Python environment:
   
   ```bash
   python weaver_solver.py -s <source_word> -t <target_word> -l <word_length> -p <custom_dict_path>
4. About the parameters:
    - **-s (--source_word)**: a string representing the source word
    - **-t (--target_word)**: a string representing the target word
    - **-l (--length)** (optional): an int representing the length of the word (4 is the default. 5 is another common choice).
    - **-p (--dictionary_path)** (optional): a string representing a path to the custom dictionary. If none is given, the default is nltk.corpus.words   

   
## Requirements
- Python 3.x
- nltk package
