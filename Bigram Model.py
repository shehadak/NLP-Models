from nltk import ngrams
import matplotlib.pyplot as plt
import numpy as np

training_raw = {'</s> dogs bark </s>',
				'</s> dogs chase cats </s>',
				'</s> cats meow </s>',
				'</s> dogs chase birds </s>',
				'</s> cats chase birds </s>',
				'</s> dogs chase the cats </s>',
				'</s> the birds chirp </s>'}
validation_raw = {'</s> the cats meow </s>', '</s> the dogs bark </s>'}
test_raw = {'</s> cats meow </s>', '</s> dogs chase the birds </s>'}

def process_n_grams(data_raw, n):
	return {ngrams(sentence.split(), n) for sentence in data_raw}

def get_probs_dict(training_raw):
	bi = process_n_grams(training_raw, 2)
	training_data = set()
	probs_dict = {}
	for sent in bi:
		for gram in sent:
			pre, post = gram
			if pre in probs_dict:
				probs_dict[pre][1][post] = probs_dict[pre][1][post] + 1 if post in probs_dict[pre][1] else 1
				probs_dict[pre][0] += 1
			else:
				probs_dict[pre] = [1, {post:1}]
	return probs_dict

def probability_function(probs_dict, alpha=0):
	V = len(probs_dict)
	def get_prob(seq):
		pre, post = seq
		if pre in probs_dict:
			if post in probs_dict[pre][1]:
				return (probs_dict[pre][1][post] + alpha)/(probs_dict[pre][0] + alpha*V)
		return (alpha/(alpha*V)) if alpha!=0 else 0
	return get_prob

def evaluate_perplexity(validation_raw, P, inverse=True):
	pp = 1
	N = 0
	validation_processed = process_n_grams(validation_raw, 2)
	for sent in validation_processed:
		for gram in sent:
			N +=1
			pp*= P(gram)
	return pp**(-1/N) if inverse else pp

def plot_perplexity(alphas, validation, test):
	# plt.plot(alphas, validation, alphas, test)
	# plt.show()
	fig, ax = plt.subplots()
	ax.set(xlabel='Alpha (α)', ylabel='Perplexity',
       title='Alpha VS. Perplexity for validation & Test Datasets')
	ax.grid()
	val_plt, = plt.plot(alphas, validation, label='Validation Dataset')
	test_plt, = plt.plot(alphas, test, label='Test Dataset')
	plt.legend(handles=[val_plt, test_plt])
	plt.show()

div = 1
d = get_probs_dict(training_raw)
A, V, T = [], [], []
possibilities = []
for a in range(1,50):
	P = probability_function(d, alpha=a/div)
	v = (evaluate_perplexity(validation_raw, P, inverse=True))
	t = (evaluate_perplexity(test_raw, P, inverse=True))
	V.append(v)
	A.append(a/div)
	T.append(t)
	print(v,t)

plot_perplexity(A,V,T)








