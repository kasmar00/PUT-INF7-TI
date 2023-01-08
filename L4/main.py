from compress import Compress
from bitarray import bitarray
import json


def create_and_encode(text):
    with open("data/norm_wiki_sample.txt") as f:
        corpus = f.read()
        compressor = Compress()

        compressor.create(corpus)

        encoded = compressor.encode(text)

        with open("encoded.bin", "wb") as ef:
            encoded.tofile(ef)
        with open("code.json", "w") as cf:
            json.dump(compressor.code_as_string(), cf)


def decode():
    read = bitarray()
    compressor = Compress()
    with open("encoded.bin", "rb") as ef:
        read.fromfile(ef)
    with open("code.json", "r") as cf:
        code = json.load(cf)
        compressor.load_code(code)

    text = compressor.decode(read)
    return text


text = "ala ma kota a kot ma ale"
create_and_encode(text)
decoded = decode()

print("Are texts equal:", text == decoded)
