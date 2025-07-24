# AI-Powered Hybrid Text Generator

---

## ✨ Project Overview

**Hybrid Text Generator** is a cutting-edge, full-stack web application designed to generate rich, human-like text across multiple genres. It uniquely combines the **statistical power of Markov Chains for structural coherence** with the **fluency and creativity of a pre-trained GPT-2 model**.

Developed meticulously within a Google Colab environment and deployed locally with Flask, TextCraft AI serves as a powerful demonstration of hybrid text generation and full-stack AI development.

---

## 🎯 Task Objective

The primary objective of this task was to implement a robust text generation solution using Markov Chains, then expand upon it to create a sophisticated statistical model that predicts character or word probability based on previous context, and finally integrate it into a comprehensive web application for versatile text generation.

---

## 🔍 Key Features

### **✅ Core AI Functionality:**
* **Hybrid Text Generation:** Combines Markov Chains (for initial seed/structure generation based on corpus patterns) and GPT-2 (for expanding the seed into coherent, fluent text).
* **Multi-Genre Support:** Generate text in distinct styles for:
    * **Prose:** For narrative or descriptive text.
    * **Poetry:** For poetic forms or lyrical content.
    * **Moods:** For text reflecting specific emotional tones.
* **Customizable Output:** Control the `Output Length` and `Creativity` (GPT-2 temperature) via interactive sliders.
* **Seed Text Input:** Provide an optional custom seed text to guide the generation, ensuring more controlled outputs.

### **✅ UI/UX Highlights:**
* **Full-stack Flask Application:** A responsive web interface built with Flask for the backend and HTML/CSS/JavaScript for the frontend.
* **Intuitive Design:** Clean, modern, and user-friendly interface powered by Tailwind CSS for rapid styling.
* **Real-time Feedback:**
    * Live loader with status messages and a progress bar during text generation.
    * Dynamic display of generated text.
    * Interactive character counter for prompt input.
* **Output Analysis:**
    * **N-gram Visualization:** Generate interactive bar charts of N-gram frequencies from the generated text, providing insights into linguistic patterns.
    * **Evaluation Metrics (Optional):** Integration points for BERTScore (for coherence against a reference) and GPT-4 analysis (for subjective ratings of Coherence, Creativity, and Grammar using an OpenAI API Key).

### **✅ Data & Performance Management:**
* **Model Caching:** Efficiently loads and caches language models (GPT-2, Markovify instances) in memory to reduce latency on subsequent generations.
* **Asynchronous Processing:** Utilizes background threading (Flask-Executor) for text generation and evaluation, ensuring the web UI remains responsive.
* **JSON Persistence:** Automatically saves generation history and usage statistics to `history.json` and `stats.json` files, ensuring data persists across server restarts.
* **Periodic Cleanup:** Background threading task for cleaning up old generated content (e.g., n-gram plots) to manage disk space.

---

## ⚙️ Tech Stack

* **Languages:** Python, HTML5, CSS3, JavaScript
* **Web Framework:** Flask
* **Text Generation:**
    * **Markov Chains:** `markovify` (for initial text seeds/structure)
    * **GPT-2:** `transformers` (for fluent text expansion), `torch`
* **NLP & Preprocessing:** `nltk`
* **Evaluation:** `bert_score` (for objective metrics), `openai` (for optional GPT-4 evaluation)
* **Data Handling:** `json`, `collections` (defaultdict)
* **Utilities:** `re`, `base64`, `io`, `os`, `random`, `threading`, `time`
* **Plotting:** `matplotlib`
* **UI/Styling:** Tailwind CSS
* **Development Environment:** Google Colab (leveraging GPU inference)

---

## 🎯 Learning Outcomes

Through this task, I gained comprehensive understanding and practical experience in:

* **Statistical vs. Neural Text Generation:** Bridging the gap between traditional NLP models (Markov Chains) and modern deep learning models (GPT-2), and understanding their respective strengths and weaknesses.
* **Model Fusion Techniques:** Learning how to combine different generative models effectively to leverage their best qualities (e.g., Markov for structure/style, GPT-2 for coherence/fluency).
* **NLP Evaluation Metrics:** Implementing and interpreting both objective (BERTScore) and subjective (GPT-4 feedback) evaluation metrics for generative text.
* **Full-Stack ML Deployment:** Designing and building a complete web application around a machine learning model, including frontend-backend communication (AJAX), asynchronous task management, and data persistence.
* **Google Colab Workflow:** Mastering development, prototyping, and resource management within a cloud-based GPU environment for complex AI tasks.
* **Code Organization & Robustness:** Implementing thread-safe global data handling and robust error management for a more stable application.

---

## 🚀 Setup & Installation

Follow these steps to get TextCraft AI up and running on your local machine.

### **1. Prerequisites**
* Python 3.8+ installed (Ensure `python` and `pip` commands work in your terminal).
* Git (for cloning the repository).

### **2. Clone the Repository**
```bash
git clone [https://github.com/mishal4583/Generative-AI-AI-Powered-Hybrid-Text-Generator]
