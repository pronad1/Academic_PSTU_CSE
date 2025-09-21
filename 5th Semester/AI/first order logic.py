from itertools import product

from itertools import product

def truth_table(express):
    print(" P | Q | R \n__________")
    for P,Q in product([0,1],repeat=2):
        R = express(P,Q)
        print(f" {P} | {Q} | {R} ")
express=lambda P,Q: P or Q
truth_table(express)

# Operators
OPS = {
    '~': lambda a: not a,
    '^': lambda a, b: a and b,
    'v': lambda a, b: a or b
}

# Truth table for any number of variables


# Compress multiple sentences
def compress_sentences(sentences):
    # Split all into word lists
    word_lists = [s.split() for s in sentences]

    # Find common starting words
    prefix = []
    for words in zip(*word_lists):
        if len(set(words)) == 1:  # all match
            prefix.append(words[0])
        else:
            break

    # If no common prefix, join with " and "
    if not prefix:
        return " or ".join(sentences)

    # Build compressed sentence
    differences = [" ".join(w[len(prefix):]) for w in word_lists]
    return " ".join(prefix) + " " + " or ".join(differences)


if __name__ == "__main__":
    # Ask how many sentences
    n = int(input("How many sentences? "))

    # Collect sentences and variable names
    sentences = []
    var = []
    for i in range(n):
        text = input(f"Enter sentence {i+1}: ")
        sentences.append(text)
        var.append(chr(80 + i))  # P, Q, R, S...

    # Example: expression for 3 vars (change as needed)
    def expr(**kwargs):
        # Example: P AND Q AND R
        result = True
        for v in var:
            result = result or kwargs[v]
        return result

    # Print compressed sentence
    sentence = compress_sentences(sentences)
    print("Sentence:", sentence, "\n")

    # Show truth table
    express=lambda a, b: a and b
    truth_table(express)
