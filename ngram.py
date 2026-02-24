import sys
import re

def main():
    if len(sys.argv) < 4:
        print("Usage: python ngram.py <n> <m> <input_file>")
        return
    n = int(sys.argv[1]) 
    m = int(sys.argv[2])
    files = sys.argv[3:] #Get all input files

    print("n = ", n)
    print("m = ", m)
    print("files = ", files)

    text = ""

    #file reading

    for file in files: #Iterate through each file
        with open(file, "r", encoding="utf-8") as f: #Open the file for reading
            text += f.read() + " " #read each file into a single string, separated by a space

    text = text.lower() #normalize the text to lowercase
    tokens = re.findall(r"\d+|[a-z]+|[.!?]", text) #tokenize the text into words and 
    
    sentences = []
    curr = []
    end = {".", "?", "!"}

    for token in tokens:
        curr.append(token)
        if token in end:
            if len(curr) >= n: #only consider sentences with at least n tokens
                sentences.append(curr)
            curr = []

    print("total sentences = ", len(sentences))
    print("first 30 sentences = ", sentences[:30])
    print("total tokens = ", len(tokens))
    print("first 30 tokens = ", tokens[:30])
    print("total unique tokens = ", len(set(tokens)))
    print("total characters = ", len(text))

if __name__ == "__main__":
    main()

