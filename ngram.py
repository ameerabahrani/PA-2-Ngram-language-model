r"""
ngram.py
Ameera Albahrani
Class: Introduction to NLP
26 February 2026

This is a simple implementation of an n-gram language model.
It reads in one or more text files and builds an n-gram model based on the tokens in the text, and generates random sentences based on that model.
The N-gram model captures the probability that a word follows a given sequence of (n-1) preceding words. 
For example, a bigram model looks at the previous 1 word to predict the next, and a trigram (n=3) model looks at the previous 2 words to predict the next.

-----------------
Usage Instructions:
The program runs from the commandline with the following arguments:
python ngram.py <n> <m> <input_file1> [<input_file2> ...]
Where:
- n: the order of the n-gram model (e.g., 1 for unigram, 2 for bigram, etc.)
- m: is the number of sentences to generate
- <input_file1>, <input_file2>, ... : the text files to build the model from
-----------------
Example Command:
C:\Users\user\OneDrive - American University of Beirut\Desktop\PA 2>python ngram.py 5 2 prideAndprejudice.txt emma.txt senseAndsensibility.txt moby.txt sherlock.txt persuasion.txt greatExp.txt
This program generates random sentences based on a 5-gram model.
Command line settings : ngram.py 5 2

on entering his room i found holmes in animated conversation with two men one of whom i recognised as peter jones the official police agent while the other was a mere question of length and wearisomeness .
what could it be ?

------------------
Algorithm:
1.Parse command-line args (n, m, file list)
2.Read all input files into a single string
3.Normalize to lowercase
4.Tokenize ... extract words, digits, and .!? as separate tokens; ignore other punctuation
5.Split tokens into sentences at ., ?, ! boundaries; discard sentences shorter than n tokens
6.Slide an n-wide window across each sentence. 
    - the first (n-1) tokens are the context key, the n-th token is the next word value. 
    - store in a dict of lists
7.Store the first (n-1) tokens of each sentence as valid starting contexts
8.For each of the m sentences: pick a random starting context
    - then repeatedly look up the current context
    - sample a random next word, append it, slide the window forward by one
    - stop when a .!? token is generated or a dead end is hit
9.Print the token list joined by spaces

-------------------

"""


from collections import defaultdict
import random
import sys
import re

def main():
    
    if len(sys.argv) < 4:
        print("Usage: python ngram.py <n> <m> <input_file>")
        return
    n = int(sys.argv[1]) 
    m = int(sys.argv[2])
    files = sys.argv[3:] #Get all input files

    print(f"This program generates random sentences based on a {n}-gram model.")
    print(f"Command line settings : ngram.py {n} {m}")
    print()

    #print("n = ", n)
    #print("m = ", m)
    #print("files = ", files)

    # Read all input files into a single string
    text = ""
    for file in files: #Iterate through each file
        with open(file, "r", encoding="utf-8", errors="ignore") as f: #Open the file for reading
            text += f.read() + " " #read each file into a single string, separated by a space

    # Normalize and tokenize the text
    text = text.lower() #normalize the text to lowercase
    tokens = re.findall(r"\d+|[a-z]+(?:'[a-z]+)*|[.!?]", text) #tokenize the text into words and 
    
    #print("total tokens = ", len(tokens))
    # Split the tokens into sentences based on punctuation marks
    # only consider sentences with at least n tokens
    sentences = []
    curr = []
    end = {".", "?", "!"}

    for token in tokens:
        curr.append(token)
        if token in end:
            if len(curr) >= n: #only consider sentences with at least n tokens
                sentences.append(curr)
            curr = []

    # Building the n gram model 
    ngrams = defaultdict(list)

    if n == 1:
        allTok = [tok for sent in sentences for tok in sent]
        ngrams[()] = allTok
        starts = [()]
        return ngrams, starts

    for sentence in sentences:
        for i in range(len(sentence) - n + 1):
            context = tuple(sentence[i:i+n-1]) #get the (n-1) perceding tokens as the context
            next = sentence[i+n-1] #get the next token after 
            ngrams[context].append(next) #add the next token to the list of possible next tokens for the context

    #store valid sentence starting contexts (those that appear at the beginning of sentences)
    start = [] 
    for sentence in sentences:
        if len(sentence) >= n: #only consider sentences with at least n tokens
            start.append(tuple(sentence[:n-1])) #add the first n tokens of the sentence as a valid starting context

    # generate m sentences using the n-gram model
    for i in range(m):
        context = list(random.choice(start)) #choose a random starting context from the stored valid ones
        sentence_tokens = list(context) #initialize the sentence with the starting context
        maxTok = 200 #to prevent infinite loops
        while len(sentence_tokens) < maxTok:
            context_tuple = tuple(context) #convert the context to a tuple for lookup in the n-gram model
            if context_tuple not in ngrams: #if the context is not in the n-gram model, stop generating this sentence
                break
            nextWord = random.choice(ngrams[context_tuple]) #choose a random next token from the list of possible next tokens for the context
            sentence_tokens.append(nextWord) #add the next token to the sentence
            if nextWord in end: #if the next token is a sentence-ending punctuation mark, stop generating this sentence
                break
            if n > 1:
                context = context[1:] + [nextWord] #update the context by removing the first token and adding the next token
        print(" ".join(sentence_tokens))


    #print("total sentences = ", len(sentences))
    #print("first 30 sentences = ", sentences[:30])
    
    #print("first 30 tokens = ", tokens[:30])
    #print("total unique tokens = ", len(set(tokens)))
    #print("total characters = ", len(text))

if __name__ == "__main__":
    main()

