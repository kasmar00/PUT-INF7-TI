# Aby wyliczyć entropię znaków i słów oraz ich entropię warunkową dla danych zawartych w pliku, należy wykonać następujące kroki:

# Otworzyć plik w trybie do odczytu.
# Odczytać dane z pliku i zapisać je w zmiennej.
# Dla każdego znaku lub słowa w danych obliczyć jego prawdopodobieństwo wystąpienia.
# Obliczyć entropię znaków lub słów jako sumę prawdopodobieństw poszczególnych znaków lub słów pomnożonych przez logarytm dwójkowy prawdopodobieństwa.
# Obliczyć entropię warunkową kolejnych rzędów dla danych znaków lub słów, wyznaczając prawdopodobieństwo wystąpienia danego znaku lub słowa w zależności od poprzedniego znaku lub słowa i obliczając entropię w taki sam sposób jak w kroku 4.
# Oto przykładowy program w pythonie, który wylicza entropię znaków i słów oraz ich entropię warunkową kolejnych rzędów dla danych zawartych w pliku:

import math
import collections


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


def calculate_entropy(data):
    # liczymy częstotliwość wystąpień każdego elementu
    counter = collections.Counter(data)
    entropy = 0
    # dla każdego elementu obliczamy entropię i dodajemy do wyniku
    for count in counter.values():
        probability = count / len(data)
        entropy += - probability * math.log2(probability)
    return entropy


def calculate_conditional_entropy_ai(data, order):
    # tworzymy słownik, w którym kluczami będą ciągi znaków o długości "order"
    # a wartościami - listy znaków, które występują po tych ciągach
    conditional_entropy = {}
    for i in range(len(data)-order):
        sequence = data[i:i+order]
        next_item = data[i+order]
        if sequence in conditional_entropy:
            conditional_entropy[sequence].append(next_item)
        else:
            conditional_entropy[sequence] = [next_item]
    # obliczamy entropię dla każdego ciągu znaków i sumujemy
    entropy = 0
    for sequence in conditional_entropy:
        entropy += calculate_entropy(conditional_entropy[sequence])
    # zwracamy entropię warunkową, czyli entropię podzieloną przez liczbę ciągów znaków
    return entropy / len(conditional_entropy)


def gen_sequences(data, order):
    sequences = []
    for i in range(len(data)-order):
        sequences.append(data[i:i+order+1])
    return sequences


def calculate_conditional_entropy(data, order):
    divided_text = gen_sequences(data, order)
    sequences = {}
    for i in range(len(data)-order):
        sequence = DictKey(data[i:i+order])
        next_item = data[i+order]
        if sequence in sequences:
            if next_item in sequences[sequence]:
                sequences[sequence][next_item] += 1
            else:
                sequences[sequence][next_item] = 1
        else:
            sequences[sequence] = {next_item: 1}

    entropy = 0
    for prev, vals in list(sequences.items()):
        for val in vals:
            pxy = vals[val] / len(divided_text)
            px_cond_y = vals[val] / sum(vals.values())
            entropy += pxy * math.log2(px_cond_y)

    return -entropy


# print(gen_sequences("abcdeffedcba", 1))

# print(calculate_conditional_entropy("abcdeffedcba", 1))
# print(calculate_conditional_entropy("abcdeffedcba", 2))o

def print_entropies_for_file(filename):
    print(f"Entropies of {filename}.txt")
    with open(f"dane/{filename}", "r") as file:
        data = file.read()

        words = data.split(" ")

        print("  Entropies")
        print("    Chars: ", calculate_entropy(data))
        print("    Words: ", calculate_entropy(words))

        for i in range(1, 5):
            print(f"  Conditional entropy for order {i}:")
            print("    Chars: ", calculate_conditional_entropy(data, i))
            # TODO: w fix for words - list of words cant be a key of dict
            print("    Words: ", calculate_conditional_entropy(words, i))


def part1():
    print("Part 1")
    filename = "norm_wiki_en.txt"
    print_entropies_for_file(filename)


def part2():
    print("Part 2")
    print("Entropies of latin ")
    print_entropies_for_file("norm_wiki_la.txt")


def part3():
    print("Part 3")
    for i in range(0, 6):
        print_entropies_for_file(f"sample{i}.txt")


def prod():
    part1()
    print()
    part2()
    print()
    part3()


prod()
