import bisect
import itertools
import random
from typing import Dict, List


def takeSecond(elem):
    return elem[1]


def count_freq(words: List[str]):
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


def sum_dict(dict: Dict):
    return sum([x for x in list(dict.values())])


def freq_to_probs(freq: Dict):
    count = sum_dict(freq)
    probs = {}
    for key, val in list(freq.items()):
        probs[key] = val/count
    return probs


def seq_prob(fprob_table, length=6):
    choices = list(fprob_table.keys())
    weights = list(fprob_table.values())
    cumdist = list(itertools.accumulate(weights))

    s = []
    while len(s) < length:
        x = random.random() * cumdist[-1]
        s.append(choices[bisect.bisect(cumdist, x)])

    return s


with open("dane/norm_wiki_sample.txt") as f:
    corpus = f.read()
    words = corpus.split(" ")
    freqs = count_freq(words)
    probs = freq_to_probs(freqs)

    for word, freq in sorted(list(probs.items()), key=takeSecond, reverse=True)[:100]:
        print(f"{word} : {freq*100}%")

    corpus_word_count = words.__len__()

    freqs_sorted = sorted(list(freqs.items()), key=takeSecond, reverse=True)
    print(freqs_sorted[:10])

    top_30k_words_count = sum_dict(dict(freqs_sorted[:30000]))
    print(
        f"Top 30k words make up: {top_30k_words_count/corpus_word_count*100}% of corpus")

    top_6k_words_count = sum_dict(dict(freqs_sorted[:6000]))
    print(
        f"Top 6k words make up: {top_6k_words_count/corpus_word_count*100}% of corpus")

    print("//=======\\\\")
    print("|| ZAD 2 ||")
    print("\\\\=======//")

    seq = seq_prob(probs, 100)

    print(" ".join(seq))
