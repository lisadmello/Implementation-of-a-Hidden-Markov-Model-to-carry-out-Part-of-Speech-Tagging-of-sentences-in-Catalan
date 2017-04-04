from collections import defaultdict
import codecs
import time
start_time = time.time()

file1 = codecs.open("catalan_corpus_train_tagged.txt", "r", "utf-8")
# Read the contents of the file into memory.
train_data_file = file1.read()
file1.close()

# import sys
# with open(sys.argv[1], 'r') as file:
#     train_data_file = file.read()
# file.close()

# Return a list of the lines, breaking at line boundaries.
train_data = train_data_file.splitlines()
print train_data[0]

# Create a dictionary that contains a tag as the key and its corresponding count as the value
tags = defaultdict(int)
# For each sentence in the training data
for line in train_data:
    # Split the sentence into words
    words = line.split(" ")
    # For each word
    for word in words:
        # Extract the tag using the last two characters
        tag = word[-2:]
        # Update the count of the tag in the tags dictionary
        if tag in tags:
            tags[tag] += 1
        else:
            tags[tag] = 1

f1 = codecs.open("hmmmodel.txt", "w+", "utf-8")
f1.write("%d\n" % len(tags))
for i in tags:
    f1.write("%s\n" % i)

# tags["qo"] = 0.0

transition_matrix = defaultdict(dict)

for line in train_data:
    # Split the sentence into words
    words = line.split(" ")
    # Get tag of first word in the sentence
    tag1 = words[0][-2:]
    # Update transition from qo to the tag
    if tag1 in transition_matrix['qo']:
        transition_matrix['qo'][tag1] += 1
    else:
        transition_matrix['qo'][tag1] = 1
    # For each word in the sentence
    for i in range(0, len(words) - 1):
        # start tag
        head = words[i][-2:]
        # end tag
        tail = words[i + 1][-2:]
        # Update transition from start tag to end tag
        if tail in transition_matrix[head]:
            transition_matrix[head][tail] += 1
        else:
            transition_matrix[head][tail] = 1

for t in transition_matrix:
    for x in transition_matrix[t]:
        transition_matrix[t][x] += 1

for t in tags:
    if t not in transition_matrix:
        transition_matrix[t] = {}

for t in transition_matrix:
    for tag in tags:
        if tag not in transition_matrix[t]:
            transition_matrix[t][tag] = 1

count = 0
for t in transition_matrix:
    for x in transition_matrix[t]:
        count += 1

f1.write("%d\n" % count)
# For each start tag
for t in transition_matrix:
    sum = 0
    # For each corresponding end tag
    for x in transition_matrix[t]:
        # Add up total for denominator
        sum += transition_matrix[t][x]
    # Update the probability of each end tag
    for x in transition_matrix[t]:
        transition_matrix[t][x] /= float(sum)
        # Write the output to hmmmodel.txt
        f1.write("%s %s %f\n" % (t, x, transition_matrix[t][x]))

emission_matrix = defaultdict(dict)

for line in train_data:
    line = line[0].lower() + line[1:]
    words = line.split(" ")
    for w in words:
        tag = w[-2:]
        token = w[0:-3]
        if token in emission_matrix[tag]:
            emission_matrix[tag][token] += 1
        else:
            emission_matrix[tag][token] = 1

count = 0
for e in emission_matrix:
    for x in emission_matrix[e]:
        count += 1

f1.write("%d\n" % count)

for e in emission_matrix:
    sum = 0
    # For each corresponding end tag
    for x in emission_matrix[e]:
        # Add up total for denominator
        sum += emission_matrix[e][x]
    # Update the probability of each end tag
    for x in emission_matrix[e]:
        emission_matrix[e][x] /= float(sum)
        # Write the output to hmmmodel.txt
        f1.write("%s %s %f\n" % (e, x, emission_matrix[e][x]))
print("--- %s seconds ---" % (time.time() - start_time))
# Close the file
f1.close()
