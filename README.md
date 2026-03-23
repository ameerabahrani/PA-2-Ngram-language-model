# PA-2-Ngram-language-model

# ngram.py
Ameera Albahrani — Introduction to NLP

A Python implementation of an n-gram language model. Give it some text files, tell it what n to use, and it'll generate random sentences based on what it learned.

The model captures the probability that a word follows a given sequence of (n-1) words before it. So a bigram (n=2) looks at the previous word to predict the next, a trigram (n=3) looks at the previous 2, and so on.

---

## Usage

```bash
python ngram.py <n> <m> <file1> [<file2> ...]
```

- `n` — order of the model (1 = unigram, 2 = bigram, etc.)
- `m` — number of sentences to generate
- `file1, file2, ...` — text files to train on

---

## Example

```bash
python ngram.py 5 2 prideAndprejudice.txt emma.txt senseAndsensibility.txt moby.txt sherlock.txt persuasion.txt greatExp.txt
```

```
This program generates random sentences based on a 5-gram model.
Command line settings : ngram.py 5 2

on entering his room i found holmes in animated conversation with two men one of whom i recognised as peter jones the official police agent while the other was a mere question of length and wearisomeness .
what could it be ?
```

---

## How it works

1. Parse args: `n`, `m`, and the file list.
2. Read all input files into one string, lowercase it.
3. Tokenize — keep words, digits, and `.!?` as separate tokens; ignore everything else.
4. Split into sentences at `.`, `?`, `!` boundaries; drop any sentence shorter than `n` tokens.
5. Slide an n-wide window across each sentence — the first (n-1) tokens are the context key, the nth is the next word. Store in a dict of lists.
6. Save the first (n-1) tokens of each sentence as valid starting contexts.
7. For each of the `m` sentences: pick a random starting context, sample a next word, slide the window forward, repeat until a `.!?` token is hit or there's a dead end.
8. Print the tokens joined by spaces.
