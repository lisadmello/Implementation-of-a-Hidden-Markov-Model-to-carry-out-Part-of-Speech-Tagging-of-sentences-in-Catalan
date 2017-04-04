import codecs
import math
import time

start_time = time.time()
from collections import defaultdict

file = codecs.open('hmmmodel.txt', 'r', 'utf-8')
# Read the contents of the file into memory
contents = file.read()
# Close the file
file.close()
# Create a list of all unique tags
tag_list = []
# Create transition matrix
transition_matrix = defaultdict(dict)
# Create emission matrix
emission_matrix = defaultdict(dict)
# Get the parameters
parameters = contents.splitlines()
# Get the number of tags
no_of_tags = int(parameters[0])
# For each tag
for i in range(1, no_of_tags + 1):
    tag_list.append(parameters[i])

end = int(parameters[no_of_tags + 1])
# Setup transition matrix
for i in range(no_of_tags + 2, no_of_tags + 2 + end):
    words = parameters[i].split(" ")
    transition_matrix[words[0]][words[1]] = float(words[2])

end2 = int(parameters[no_of_tags + 2 + end])
# Setup Emission Matrix
vocab = set()
for j in range(no_of_tags + 2 + end + 1, no_of_tags + 2 + end + 1 + end2):
    words = parameters[j].split(" ")
    emission_matrix[words[0]][words[1]] = float(words[2])
    # print words[1]
    vocab.add(words[1])
print len(vocab)
# Read the test data
f = codecs.open("catalan_corpus_dev_raw.txt", "r", "utf-8")
test_data = f.read()
test_data = test_data.splitlines()

# Open output file
f1 = codecs.open("hmmoutput.txt", "w+", "utf-8")

# For each line in the test data
for line in test_data:
    probability_array = defaultdict(dict)
    backpointer = defaultdict(dict)
    for q in tag_list:
        probability_array[q] = {}
    words = line.split(" ")
    no_of_words = len(words)
    for q in tag_list:
        if words[0] in vocab:
            if words[0] in emission_matrix[q]:
                probability_array[q][1] = math.log(transition_matrix[u"qo"][q]) + math.log(emission_matrix[q][words[0]])
            else:
                probability_array[q][1] = math.log(transition_matrix[u"qo"][q]) + float("-inf")
        else:
            probability_array[q][1] = math.log(transition_matrix[u"qo"][q])
        backpointer[q][1] = u"qo"
    for t in range(2, no_of_words + 1):
        for q in tag_list:
            max1 = float("-inf")
            max2 = float("-inf")
            for q_dash in tag_list:
                if words[t-1] in vocab:
                    if words[t - 1] in emission_matrix[q]:
                        temp = probability_array[q_dash][t - 1] + math.log(transition_matrix[q_dash][q]) + math.log(emission_matrix[q][words[t - 1]])
                    else:
                        temp = probability_array[q_dash][t - 1] + math.log(transition_matrix[q_dash][q]) + float("-inf")
                else:
                    temp = probability_array[q_dash][t - 1] + math.log(transition_matrix[q_dash][q])
                if temp >= max1:
                    max1 = temp
                    probability_array[q][t] = temp
                if (probability_array[q_dash][t - 1] + math.log(transition_matrix[q_dash][q])) >= max2:
                    max2 = probability_array[q_dash][t - 1] + math.log(transition_matrix[q_dash][q])
                    backpointer[q][t] = q_dash
    # print probability_array
    # print backpointer

    max3 = float("-inf")
    T = no_of_words
    for x in probability_array:
        if probability_array[x][T] > max3:
            max3 = probability_array[x][T]
            tail = x
    # print backpointer
    # print probability_array
    counter = no_of_words
    annotation = []
    while counter > 0:
        if counter == no_of_words:
            annotation.append(words[counter - 1] + u"/" + tail)
        else:
            annotation.append(words[counter - 1] + u"/" + tail + u" ")
        # print tail
        tail = backpointer[tail][counter]
        counter -= 1
    for x in reversed(annotation):
        f1.write(x)
    f1.write("\n")

print("--- %s seconds ---" % (time.time() - start_time))
f.close()

# with open(sys.argv[1], 'r') as file:
#     contents = file.read()
# file.close()