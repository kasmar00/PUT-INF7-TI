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
countslist = sorted(list(counts.items()), key=takeSecond, reverse=True)
for x in range(2):
    i, j = countslist[x]
    print(f"'{i}': {j/len(corpus)}")
    probs[i] = j/len(corpus)

print(list(probs.keys()))


s = f" {corpus}"
counts = {}
for i in range(len(s)-1):
    key = s[i:i+2]
    counts[key] = counts.get(key, 0)+1
# print(counts)

markovProbs = {}
sum = sum([x for x in counts.values()])
for key, val in sorted(list(counts.items()), key=takeSecond, reverse=True):
    markovProbs[key] = val / sum

# print([x for x in list(markovProbs.items) if x[0][0] in probs.keys()])

for x in list(markovProbs.items()):
    if x[0][0] in list(probs.keys()):
        print(f"'{x[0]}' : {x[1]/probs[x[0][0]]}")
