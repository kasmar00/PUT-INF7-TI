import bisect
import itertools
import random


def count_prob(string):
    counts = {}
    for i in string:
        counts[i] = counts.get(i, 0) + 1
    return counts


def average_word(string):
    words = string.split(" ")
    lens = [len(x) for x in words]
    return sum(lens)/len(words)


def takeSecond(elem):
    return elem[1]


with open("data/norm_hamlet.txt") as f:
    corpus = f.read()
    counts = count_prob(corpus)
    print(f"Average word in corpus: {average_word(corpus)}")

probs = {}
for i, j in sorted(list(counts.items()), key=takeSecond, reverse=True):
    print(f"'{i}': {j/len(corpus)}")
    probs[i] = j/len(corpus)

# zad3

#probslist = sorted(list(probs.items()))
probslist = probs


def seq_prob(fprob_table, K=6):
    choices = list(fprob_table.keys())
    weights = list(fprob_table.values())
    cumdist = list(itertools.accumulate(weights))

    s = ""
    while len(s) < K:
        x = random.random() * cumdist[-1]
        s += choices[bisect.bisect(cumdist, x)]

    return s


sequence = seq_prob(probslist, K=10000)

print(f"Average word: {average_word(sequence)}")
