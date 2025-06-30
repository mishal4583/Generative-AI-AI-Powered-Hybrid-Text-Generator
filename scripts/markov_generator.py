import markovify

# Load cleaned texts
with open("outputs/pride_sentences.txt") as f:
    text1 = f.read()
with open("outputs/frankenstein_sentences.txt") as f:
    text2 = f.read()
with open("outputs/markov_sentences.txt", "w", encoding="utf-8") as out_file:
    for i in range(20):
        sentence = combined_model.make_sentence()
        if sentence:
            out_file.write(sentence + "\n")

# Create Markov models
model1 = markovify.Text(text1, state_size=3)
model2 = markovify.Text(text2, state_size=3)

# Combine models with equal weight
combined_model = markovify.combine([model1, model2], [1, 1])

# Generate sentences
print("\n🔹 Generated Sentences:")
for i in range(5):
    print(combined_model.make_sentence())

print("\n🔹 Short Sentences (<100 chars):")
for i in range(5):
    print(combined_model.make_short_sentence(100))
