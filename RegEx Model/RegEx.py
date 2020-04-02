import re
import os
import matplotlib.pyplot as plt


spoken_path =  "../../Data/text_spoken_kde/"
fiction_path = "../../Data/text_fiction_awq/"
newspaper_path = "../../Data/text_newspaper_lsp/"
all_paths = [spoken_path, fiction_path, newspaper_path]

## 1 ##
def a_find_cooccurance_prob(paths, w1, w2, size, return_all = False):
	matches = 0.0
	condition = 0.0
	j = []
	for path in paths:
		for filename in os.listdir(os.getcwd() + path):
			filepath = (path[1:] + filename)
			textfile = open(filepath, 'r')
			filetext = textfile.read()
			textfile.close()
			q = re.findall('%s\W+(?:\w+\W+)%s?%s' %(w1, size, w2), filetext) + re.findall('%s\W+(?:\w+\W+)%s?%s' %(w2, size, w1), filetext)
			j += q
			matches += len((q))
			
			condition += len((re.findall(w2, filetext)))
	if return_all:
		return matches, condition, matches/condition, j
	return matches/condition

def b_find_word_in_between(paths, w1, w2, w3, size, return_all = False):
	J = []
	for path in paths:
		for filename in os.listdir(os.getcwd() + path):
			filepath = (path[1:] + filename)
			textfile = open(filepath, 'r')
			filetext = textfile.read()

			textfile.close()

			J += re.findall('%s\W+(?:\w+\W+)%s?%s' %(w1, size, w2), filetext) + re.findall('%s\W+(?:\w+\W+)%s?%s' %(w2, size, w1), filetext)
	
	matches = sum([1.0 for j in J if w3 in j])
	condition = len(J)

	if return_all:
		return matches, condition, matches/condition, J
	return matches/condition

## 2 ##
def find_cooccurance_preferences(paths, w1, w2, size, return_all = False):
	J_w1_w2 = []
	J_w2_w1 = []
	for path in paths:
		for filename in os.listdir(os.getcwd() + path):
			filepath = (path[1:] + filename)
			textfile = open(filepath, 'r')
			filetext = textfile.read()

			textfile.close()

			J_w1_w2 += re.findall('%s\W+(?:\w+\W+)%s?%s' %(w1, size, w2), filetext)
			J_w2_w1 += re.findall('%s\W+(?:\w+\W+)%s?%s' %(w2, size, w1), filetext)
	
	matches = float(len(J_w1_w2))
	condition = float(len(J_w1_w2) + len(J_w2_w1))

	if return_all:
		return matches, condition, matches/condition, J_w1_w2 + J_w2_w1
	return matches/condition

# 1
# a = a_find_cooccurance_prob([spoken_path], "alleged", "crimes", "{0,3}", True) # (a) = 0.0139
# b = b_find_word_in_between([spoken_path], "guilty", "defendant", "not", "{0,3}", True) # (b) = 0.1837

# 2
# a = find_cooccurance_preferences(all_paths, "salt", "pepper", "{0,3}", True) # (a) = 0.925
# b = find_cooccurance_preferences(all_paths, "men", "women", "{0,3}", True) # (b) = 0.831

# c = [(i, find_cooccurance_preferences(all_paths, "there", "here", "{0,%s}" %(str(i)))) for i in range(15)]
c = [(0, 0.00629080118694362), (1, 0.02549523110785033), (2, 0.057198275862068965), (3, 0.10057347050517276), (4, 0.11903371612707887), (5, 0.13204452048753815), (6, 0.13596062079450857), (7, 0.1369149856867053), (8, 0.13738953832763143), (9, 0.13715694037091145), (10, 0.13817142857142858), (11, 0.13865546218487396), (12, 0.1389114241463235), (13, 0.1395552366032749), (14, 0.14037705027336977)]
fig, ax = plt.subplots()
ax.set(xlabel='n-word window', ylabel='P("here" before "there")',
   title='P("here" before "there" for different n-word windows')
ax.grid()
val_plt, = plt.plot([i[0] for i in c], [1 - i[1] for i in c], label='Validation Dataset')
plt.show()



