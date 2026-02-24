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
    
    print("total tokens = ", len(tokens))
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

    for sentence in sentences:
        for i in range(len(sentence) - n):
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
            next = random.choice(ngrams[context_tuple]) #choose a random next token from the list of possible next tokens for the context
            sentence_tokens.append(next) #add the next token to the sentence
            if next in end: #if the next token is a sentence-ending punctuation mark, stop generating this sentence
                break
            context = context[1:] + [next] #update the context by removing the first token and adding the next token
        print(" ".join(sentence_tokens))


    


    #print("total sentences = ", len(sentences))
    #print("first 30 sentences = ", sentences[:30])
    
    #print("first 30 tokens = ", tokens[:30])
    #print("total unique tokens = ", len(set(tokens)))
    #print("total characters = ", len(text))

if __name__ == "__main__":
    main()

