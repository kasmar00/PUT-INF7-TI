import bisect
import itertools
import random
from typing import List


should_print = True


def gen_word(probs):

    choices = list(probs.keys())
    weights = list(probs.values())
    cumdist = list(itertools.accumulate(weights))

    x = random.random() * cumdist[-1]
    return choices[bisect.bisect(cumdist, x)]


def gen_seq(probs, length=100, rank=1, starting_seq=["probability", "of", "words", "is"]):
    prev = starting_seq[-rank:]
    print("prev:", prev)
    s = starting_seq

    for _ in range(length):
        word = gen_word(probs.get(tuple(prev)))

        s.append(word)
        prev = prev[1:] + [word]

    return s


# struktura danych prob:
x = {
    ("abacki", "babacki"): {
        "abacki": 0.1,
        "babacki": 0.9
    },
    ("babacki", "abacki"): {
        "abacki": 0.3,
        "babacki": 0.7
    },
    ("babacki", "babacki"): {
        "abacki": 0.3,
        "babacki": 0.7
    },
    ("abacki", "abacki"): {
        "abacki": 0.7,
        "babacki": 0.3
    }
}


def take_second(elem):
    return elem[1]


# https: // www.cs.princeton.edu/courses/archive/fall13/cos126/assignments/markov.html
def ngrams(corpus: List[str], length: int):
    ret = []
    for i in range(len(corpus)):
        tmp = corpus[i:] + corpus[:i]
        ret.append(tmp[:length])
    return ret


def word_seq_probs(corpus: List[str], rank: int):
    counts = {}
    for key in ngrams(corpus, rank+1):
        counts[tuple(key)] = counts.get(tuple(key), 0)+1

    probs = {}
    sum_counts = sum([x for x in counts.values()])
    for key, val in sorted(list(counts.items()), key=take_second, reverse=True):
        probs[key] = val / sum_counts

    return probs


def combine_probs_with_seq(probs, seq_probs):
    combined = {}
    debug(f"Probs: {probs}")
    debug(f"Seq_probs: {seq_probs}")
    for key, val in list(seq_probs.items()):
        # debug(f"P(i)={probs[key[0]]}, P(i,j)={seq_probs[key]}={val}, P(j|i)={val / probs[key[0]]}")
        debug(f"'{key}' :{val/probs[key[0]]} ")
        key_start = key[:-1]
        char = key[-1]
        cond_prob = val/probs[key_start]
        combined[key_start] = combined.get(key_start, {})
        combined[key_start][char] = cond_prob

    return combined


def combined_to_accumulated(combined):
    return combined
    ret = {}
    for key, value in list(combined.items()):
        ret[key] = Accumulated_probs(value)
    return ret


def gen_markov_probs(corpus: List[str], rank=1):
    probs = word_seq_probs(corpus, rank)
    seq_probs = {}
    for i in range(0, rank):
        seq_probs.update(word_seq_probs(corpus, i))
    combined = combine_probs_with_seq(seq_probs, probs)
    return combined_to_accumulated(combined)


# UTIL

def debug(*args):
    if should_print:
        print(*args)


print(gen_seq(x, starting_seq=["abacki", "babacki"], rank=2))

probs = gen_markov_probs(['abacki', 'babacki', 'babacki', 'abacki', 'abacki', 'abacki', 'abacki', 'abacki', 'abacki', 'abacki', 'babacki', 'abacki', 'abacki',
                          'babacki', 'babacki', 'babacki', 'babacki', 'babacki', 'abacki', 'babacki', 'babacki', 'babacki', 'babacki', 'abacki', 'babacki', 'babacki', 'babacki'
                          ], rank=1)
print(probs)
