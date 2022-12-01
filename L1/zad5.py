import bisect
import itertools
import random
import sys

should_print = True


class Accumulated_probs:
    def __init__(self, cond_probs):
        self.choices = list(cond_probs.keys())
        self.weights = list(cond_probs.values())
        self.cumdist = list(itertools.accumulate(self.weights))

# Generate sequences


def gen_char(probs: Accumulated_probs):
    x = random.random() * probs.cumdist[-1]
    return probs.choices[bisect.bisect(probs.cumdist, x)]


def gen_seq(probs, length=100, rank=1, starting_seq="probability"):

    prev = starting_seq[-rank:]
    print("prev:", prev)
    s = starting_seq

    for _ in range(length):
        char = gen_char(probs.get(prev))

        s += char
        prev = prev[1:] + char

    return s


# Markov probabilities

# struktura danych prob:
x = {
    "aa": {
        "a": 0.1,
        "b": 0.9
    },
    "ab": {
        "a": 0.3,
        "b": 0.7
    }
}


def take_second(elem):
    return elem[1]


# https: // www.cs.princeton.edu/courses/archive/fall13/cos126/assignments/markov.html
def ngrams(corpus: str, length: int):
    ret = []
    dcorpus = corpus*2
    for i in range(len(corpus)):
        ret.append(dcorpus[i:i+length])
        # tmp = corpus[i:] + corpus[:i]
        # ret.append(tmp[:length])
    return ret


def char_seq_probs(corpus: str, rank: int):
    counts = {}
    for key in ngrams(corpus, rank+1):
        counts[key] = counts.get(key, 0)+1

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
    ret = {}
    for key, value in list(combined.items()):
        ret[key] = Accumulated_probs(value)
    return ret


def gen_markov_probs(corpus, rank=1):
    probs = char_seq_probs(corpus, rank)
    seq_probs = {}
    for i in range(0, rank):
        seq_probs.update(char_seq_probs(corpus, i))
    combined = combine_probs_with_seq(seq_probs, probs)
    return combined_to_accumulated(combined)

# UTIL


def average_word(string):
    words = string.split(" ")
    lens = [len(x) for x in words]
    return sum(lens)/len(words)


def debug(*args):
    if should_print:
        print(*args)

# RUN


def test():
    rank = 1
    mprobs = gen_markov_probs("abcdef fedcba acbdfe", rank)
    debug(mprobs)
    seq = gen_seq(mprobs, 100, rank, starting_seq="abcdef ")
    debug(seq)


def prod():
    print("Solution")
    global should_print
    should_print = False
    with open("data/norm_wiki_sample.txt") as f:
        corpus = f.read()
        for rank in [1, 3, 5]:
            mprobs = gen_markov_probs(corpus, rank)
            seq = gen_seq(mprobs, 10000, rank)
            with open(f"gen_{rank}.txt", "w") as f2:
                f2.write(seq)
            print(
                f"Average word len for rank {rank}: {average_word(seq)}")


def main():
    test()
    prod()


if __name__ == "__main__":
    main()
