from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import re
import torch
import nltk
import openai
import numpy as np
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from bert_score import score
import markovify
import matplotlib.pyplot as plt
from collections import Counter
import base64
from io import BytesIO
import os
import traceback
import random

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize models
try:
    # Sample data - replace with your actual datasets
    print("Loading sample data...")
    pride = "It is a truth universally acknowledged that a single man in possession of a good fortune must be in want of a wife."
    frankenstein = "You will rejoice to hear that no disaster has accompanied the commencement of an enterprise which you have regarded with such evil forebodings."
    sonnets = [
        "Shall I compare thee to a summer's day? Thou art more lovely and more temperate.",
        "My mistress' eyes are nothing like the sun; Coral is far more red than her lips' red."
    ]
    moods = ["joyful", "melancholic", "angry", "peaceful"]

    # Initialize Markov models
    print("Initializing Markov models...")
    prose_model = markovify.Text(pride + " " + frankenstein, state_size=2)
    poem_model = markovify.NewlineText("\n".join(sonnets), state_size=2)
    mood_model = markovify.Text(" ".join(moods), state_size=1)

    # Initialize GPT-2
    print("Loading GPT-2 model...")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
    model = GPT2LMHeadModel.from_pretrained('distilgpt2').to(device)
    tokenizer.pad_token = tokenizer.eos_token

    print("All models loaded successfully!")
except Exception as e:
    print(f"Initialization error: {str(e)}")
    traceback.print_exc()
    raise

def generate_gpt2(prompt, max_tokens=100, temperature=0.7):
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True,
            repetition_penalty=1.5,
            pad_token_id=tokenizer.eos_token_id
        )
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        print(f"GPT-2 generation error: {str(e)}")
        return f"Generation error: {str(e)}"

def plot_ngrams(text, n=2, top_k=15):
    try:
        if not text or not isinstance(text, str):
            raise ValueError("Invalid text input")
            
        words = nltk.word_tokenize(text.lower())
        if len(words) < n:
            raise ValueError(f"Text too short for {n}-gram analysis")
            
        ngrams = list(nltk.ngrams(words, n))
        freq = Counter(ngrams)
        
        plt.figure(figsize=(10, 5))
        labels, values = zip(*freq.most_common(top_k))
        labels = [' '.join(gram) for gram in labels]
        
        plt.barh(labels[::-1], values[::-1], color='#C5DDBC')
        plt.title(f"Top {top_k} {n}-grams")
        plt.xlabel("Frequency")
        plt.tight_layout()
        
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        return plot_base64
    except Exception as e:
        print(f"N-gram plot failed: {str(e)}")
        return None

def evaluate_text(text, reference=None, api_key=None):
    results = {}
    
    if api_key and api_key.strip():
        try:
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{
                    "role": "user",
                    "content": f"Analyze (1-5 ratings):\nCoherence\nCreativity\nGrammar\n\n{text}"
                }],
                max_tokens=150
            )
            results["gpt4_eval"] = response.choices[0].message['content'].strip()
        except Exception as e:
            results["gpt4_error"] = f"GPT-4 evaluation failed: {str(e)}"
    
    if reference:
        try:
            P, R, F1 = score([text], [reference], lang='en')
            results["bert_score"] = {
                "precision": round(P.mean().item(), 3),
                "recall": round(R.mean().item(), 3),
                "f1": round(F1.mean().item(), 3)
            }
        except Exception as e:
            results["bert_error"] = f"BERTScore failed: {str(e)}"
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    genre = data.get('genre', 'Prose')
    prompt = data.get('prompt', '')
    length = data.get('length', 100)
    creativity = data.get('creativity', 0.7)
    api_key = data.get('api_key', '')

    try:
        seed_text = ""
        generated_output = ""
        ngram_plot = None
        
        if genre == "Prose":
            default_seeds = [
                "The wind howled through the trees",
                "In a quiet corner of the world",
                "She opened the door to find",
                "The mystery began when"
            ]
            seed_text = prose_model.make_sentence(tries=50) or random.choice(default_seeds)
            generated_output = generate_gpt2(seed_text, max_tokens=length, temperature=creativity)
            ngram_plot = plot_ngrams(seed_text, 2)
            
        elif genre == "Poetry":
            default_seeds = [
                "Shall I compare thee to a summer's day",
                "The roses bloom in morning light",
                "Whispering winds tell ancient tales",
                "Silver moon on velvet night"
            ]
            seed_text = poem_model.make_short_sentence(20, tries=50) or random.choice(default_seeds)
            generated_output = generate_gpt2(f"Poem about: {seed_text}", max_tokens=length, temperature=creativity)
            ngram_plot = plot_ngrams(seed_text, 1)
            
        elif genre == "Moods":
            seed_text = mood_model.make_short_sentence(10, tries=50) or random.choice(moods)
            generated_output = generate_gpt2(f"Describe: {seed_text}", max_tokens=length, temperature=creativity)

        evaluation_results = evaluate_text(generated_output, seed_text if genre != "Moods" else None, api_key)

        return jsonify({
            'success': True,
            'seed': seed_text,
            'output': generated_output,
            'evaluation': evaluation_results,
            'plot': ngram_plot
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)