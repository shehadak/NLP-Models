#!/usr/bin/env python
import numpy as np

FILENAME = "../../Data/glove.6B/glove.6B.300d.txt"
def read_vectors_from_file(filename):
    d = {}
    with open(filename, 'rt') as infile:
        for line in infile:
            parts = line.split()
            word = parts[0]
            rest = parts[1:]
            d[word] = np.array(list(map(float, rest)))
    return d

def cosine_similarity(v1, v2): return np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))

def ecludian_distance(v1, v2): return np.linalg.norm(v1-v2)

def find_analogy(e, w1, w2, w3):
    # input: e: embedding vectors; w: word as string
    # output: semantic np vector of a word x such that w1 : w2 :: w3 : x
    return e[w2] - e[w1] + e[w3]

def find_closest_words(e, v, n):
    # input: e: embedding vectors; v: semantic vector; n: integer
    # output: n words closest to vector v in the embeddings.
    return sorted(e, key=lambda x: cosine_similarity(v, e[x]))[::-1][:n]

def similarity_two_sentences(e, s1, s2):
	v1 = np.mean([e[w] for w in s1.split(' ')], axis=0)
	v2 = np.mean([e[w] for w in s2.split(' ')], axis=0)
	return cosine_similarity(v1, v2)

e = read_vectors_from_file(FILENAME)
y = find_analogy(e, 'man', 'king', 'girl')
print(find_closest_words(e, y, 5))


