# scripts/gpt_refiner.py

from transformers import pipeline, set_seed
import random

# Set up the GPT-2 pipeline
generator = pipeline('text-generation', model='gpt2')
set_seed(42)

# Sample Markov-style prompts
prompts = [
    "The young girl was occupied in fixing the boat and",
    "By all that I can get them",
    "I am truly glad, dearest Lizzy, that you have resumed",
    "We felt that they were not to be intimidated",
    "It is because he will not allow you to perish"
]

print("\n🔮 Refined with GPT-2:")
for prompt in prompts:
    output = generator(prompt, max_length=60, num_return_sequences=1)
    print(f"\n📝 Prompt: {prompt}")
    print(f"✨ GPT-2: {output[0]['generated_text']}")
