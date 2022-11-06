import bisect
import itertools
import random
from typing import List


should_print = True


class DictKey():
    key = []

    def __init__(self, key) -> None:
        if type(key) is str:
            self.key = [key]
        if type(key) is list:
            self.key = key

    def __hash__(self) -> int:
        return hash(" ".join(self.key))

    def __eq__(self, __o: object) -> bool:
        return self.key == __o.key

    def __ne__(self, __o: object) -> bool:
        return not (self == __o)

    def value(self):
        return " ".join(self.key)

    def __str__(self) -> str:
        return f"DK({self.key})"


class Accumulated_probs:
    def __init__(self, cond_probs):
        self.choices = list(cond_probs.keys())
        self.weights = list(cond_probs.values())
        self.cumdist = list(itertools.accumulate(self.weights))

    def __str__(self) -> str:
        return f"AP({self.choices}; {self.weights}; {self.cumdist})"


def gen_word(probs):

    # choices = list(probs.keys())
    # weights = list(probs.values())
    # cumdist = list(itertools.accumulate(weights))

    # x = random.random() * cumdist[-1]
    # return choices[bisect.bisect(cumdist, x)]
    x = random.random() * probs.cumdist[-1]
    return probs.choices[bisect.bisect(probs.cumdist, x)]


def gen_seq(probs, length=100, rank=1, starting_seq=["probability", "of", "words", "is"]):
    prev = starting_seq[-rank:]
    print("prev:", prev)
    s = starting_seq

    for _ in range(length):
        word = gen_word(probs.get(DictKey(prev)))

        s.append(word)
        prev = prev[1:] + [word]

    return s


# struktura danych prob:
x = {
    DictKey(["abacki", "babacki"]): {
        "abacki": 0.1,
        "babacki": 0.9
    },
    DictKey(["babacki", "abacki"]): {
        "abacki": 0.3,
        "babacki": 0.7
    },
    DictKey(["babacki", "babacki"]): {
        "abacki": 0.3,
        "babacki": 0.7
    },
    DictKey(["abacki", "abacki"]): {
        "abacki": 0.7,
        "babacki": 0.3
    }
}


def take_second(elem):
    return elem[1]


# https: // www.cs.princeton.edu/courses/archive/fall13/cos126/assignments/markov.html
def ngrams(corpus: List[str], length: int):
    ret = []
    dcorpus = corpus*2
    for i in range(len(corpus)):
        ret.append(dcorpus[i:i+length])
        # tmp = corpus[i:] + corpus[:i]
        # ret.append(tmp[:length])
    return ret


def word_seq_probs(corpus: List[str], rank: int):
    counts = {}
    for key in ngrams(corpus, rank+1):
        counts[DictKey(key)] = counts.get(DictKey(key), 0)+1

    probs = {}
    sum_counts = sum([x for x in counts.values()])
    for key, val in sorted(list(counts.items()), key=take_second, reverse=True):
        probs[key] = val / sum_counts

    return probs


def dictToString(dict):
    ret = "{"
    for key, val in list(dict.items()):
        ret += f"{key}: {val}, "
    ret += "}"
    return ret


def combine_probs_with_seq(probs, seq_probs):
    combined = {}
    debug(f"Probs: {dictToString(probs)}")
    debug(f"Seq_probs: {dictToString(seq_probs)}")
    for key, val in list(seq_probs.items()):
        # debug(f"P(i)={probs[key[0]]}, P(i,j)={seq_probs[key]}={val}, P(j|i)={val / probs[key[0]]}")
        # debug(f"'{key}' :{val/probs[key.key[0]]} ") # Co robi ta linijka???
        key_start = DictKey(key.key[:-1])
        char = key.key[-1]
        cond_prob = val/probs[key_start]
        combined[key_start] = combined.get(key_start, {})
        combined[key_start][char] = cond_prob

    return combined


def combined_to_accumulated(combined):
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


def average_word(string):
    words = string.split(" ")
    lens = [len(x) for x in words]
    return sum(lens)/len(words)


def debug(*args):
    if should_print:
        print(*args)


# RUN


def test():
    rank = 3
    mprobs = gen_markov_probs([*"abcdef fedcba acbdfe "], rank)
    debug(dictToString(mprobs))
    seq = gen_seq(mprobs, 100, rank, starting_seq=[*"abcdef "])
    debug("".join(seq))


# def prod():
#     print("Solution")
#     global should_print
#     should_print = False
#     with open("dane/norm_hamlet.txt") as f:
#         corpus = [*f.read()][:1000]
#         for rank in [1, 3, 5]:
#             mprobs = gen_markov_probs(corpus, rank)
#             seq = gen_seq(mprobs, 10000, rank, starting_seq=[*"tragedy"])
#             seq = "".join(seq)
#             print(
#                 f"Average word len for rank {rank}: {average_word(seq)}")


def prod():
    print("Solution")
    global should_print
    should_print = False
    with open("dane/norm_hamlet.txt") as f:
        corpus = f.read().split(" ")
        for rank in [1, 2]:
            mprobs = gen_markov_probs(corpus, rank)
            print(dictToString(mprobs)[:250])
            seq = gen_seq(mprobs, 1000, rank)
            seq = " ".join(seq)
            with open(f"gen_{rank}.txt", "w") as f2:
                f2.write(seq)
            print(
                f"Average word len for rank {rank}: {average_word(seq)}")


def main():
    test()
    prod()


if __name__ == "__main__":
    main()
