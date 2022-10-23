def count_prob(string):
    counts = {}
    for i in string:
    	counts[i] = counts.get(i, 0) + 1
    return counts

def takeSecond(elem):
    return elem[1]

with open("data/norm_hamlet.txt") as f:
    corpus = f.read()
    counts = count_prob(corpus)

probs = {}
for i, j in sorted(list(counts.items()), key=takeSecond, reverse=True):
    print(f"'{i}': {j/len(corpus)}")
    probs[i] = j/len(corpus)
 
 
# zad3

print(probs)
#probslist = sorted(list(probs.items()))
probslist = probs

import random
import itertools
import bisect

def seq_prob(fprob_table, K=6, N=1):
    choices = list(fprob_table.keys())
    weights = list(fprob_table.values())
    cumdist = list(itertools.accumulate(weights))

    results = []
    for _ in range(N):
        s = ""
        while len(s) < K:
            x = random.random() * cumdist[-1]
            s += choices[bisect.bisect(cumdist, x)]
        results.append(s)

    return results

sequence = seq_prob(probslist, K = 1000)[0]

def average_word(string):
    words = string.split(" ")
    lens = [len(x) for x in words]
    return sum(lens)/len(words)
    
print(f"Average word: {average_word(sequence)}")    
