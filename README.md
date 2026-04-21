# Sinhala Chatbot for Sri Lanka Department of Pensions

A modular, Retrieval-Augmented Generation (RAG) based AI Chatbot System designed to assist citizens with inquiries related to the Sri Lanka Department of Pensions in the Sinhala language.

---

## Table of Contents
- [1. The Problem and Objective](#1-the-problem-and-objective)
- [2. System Design and Architecture](#2-system-design-and-architecture)
- [3. Project Structure](#3-project-structure)
- [4. Getting Started](#4-getting-started)
- [5. Usage](#5-usage)

---

## 1. The Problem and Objective

### 1.1. Background and Context
The Sri Lanka Department of Pensions is a prime government institution responsible for handling, managing, and distributing pensions, Widows' and Orphans' Pension benefits, and other related social security allowances to retired government servants and their dependents. Given the vast number of retirees and beneficiaries spread across the country, the department frequently receives thousands of inquiries daily. These inquiries range from simple administrative questions, such as finding out the status of a pension application, to more complex questions regarding disability benefits, death gratuities, rules surrounding remarriage, and necessary documentation for setting up a trustee.

Currently, citizens rely on manual channels, such as physically visiting regional secretariats (Pradeshiya Sabhas), making phone calls lines which are often congested, or writing formal letters. The department features an online FAQ on their official website (https://pensions.gov.lk/index.php/si/faqs), which contains vital information. However, navigating a large FAQ database can be challenging for elderly citizens who may lack the technical literacy to search for specific sections.

### 1.2. The Problem Definition
The primary problem addressed by this project is the **Information Accessibility Gap**. There is an abundance of written guidelines, rules, and procedures, but accessing the correct piece of information instantaneously requires manual effort. 
Furthermore, implementing a chatbot in the Sinhala language poses a unique Natural Language Processing (NLP) challenge. Sinhala is a morphologically rich and relatively low-resource language in the NLP sphere. Traditional keyword-matching chatbots or rule-based conversational agents often fail because users construct queries using various colloquialisms, misspellings, and complex grammatical structures.

### 1.3. System Objective
The goal of this project is to design, develop, and deploy a **Retrieval-Augmented Generation (RAG) based AI Chatbot System** specialized in addressing inquiries related to the Sri Lanka Department of Pensions using the Sinhala language.

The specific objectives of the project are as follows:
1. **Semantic Understanding:** To move beyond simple keyword searches by utilizing a multilingual sentence embedding model (`paraphrase-multilingual-MiniLM-L12-v2`) that understands the semantic meaning behind a user's Sinhala query.
2. **Context-Aware Response Generation:** To utilize a Large Language Model (`gemma4:e2b` via Ollama) capable of generating highly accurate, polite, and context-specific direct answers based only on the retrieved official information.
3. **Domain Restriction (Hallucination Prevention):** To enforce strict rules preventing the model from hallucinating or answering out-of-domain questions by utilizing an optimized Sinhala system prompt.
4. **User-Friendly Interface:** To provide a visually appealing, easily accessible, and responsive user interface using the `Streamlit` framework, styled specifically to meet government standard aesthetics.
---

## 2. System Design and Architecture

### 2.1. Architectural Overview
The system employs a classic Retrieval-Augmented Generation (RAG) architecture. RAG bridges the gap between static retrieval systems and generative models by retrieving facts from an external database and passing them to an LLM to formulate a grounded response. This is essentially split into two main pipelines: the **Indexing/Retrieval Pipeline** and the **Generation Pipeline**.

#### 2.1.1. Data Ingestion and Indexing
The official and verified knowledge base is stored in a structured dataset (`dataset.csv`). This file acts as the single source of truth and contains data extracted from `https://pensions.gov.lk/index.php/si/faqs`. Upon initialization, the system loads this dataset, extracting the `sinhala_question` and `sinhala_answer` columns. The embedding model translates every question into a high-dimensional vector representation and stores it in memory.

#### 2.1.2. Semantic Search Retrieval
When a user asks a question, their raw string input is encoded into a vector utilizing the exact same pre-trained embedding model (`MiniLM-L12-v2`). The system then computes the Cosine Similarity between the user's vector and all pre-computed vectors. The highest-scoring query indicates the contextually closest match in the database.

#### 2.1.3. Generation Pipeline (Ollama LLM)
Once the best match is retrieved, the corresponding official answer is injected into a meticulously crafted Sinhala-language prompt. The prompt acts as a boundary for the Large Language Model (`gemma4:e2b`). The LLM is instructed not to output any chain-of-thought or "reasoning" traces but rather to distill the retrieved context into a polished, conversational, natural Sinhala response.

---

## 3. Project Structure

- `app.py`: The main Streamlit web application providing the sleek, mobile-responsive user interface. Handles user input, state management, and real-time frontend rendering.
- `utils.py`: Encapsulates the core NLP backend logic:
  - Loads the `dataset.csv`.
  - Generates vector embeddings via `sentence-transformers`.
  - Calculates Cosine Similarity using `scikit-learn` for retrieval.
  - Constructs the strictly domain-bound prompt and queries the local LLM via `ollama` library.
- `dataset.csv`: The knowledge base acting as the single source of truth, loaded with verified FAQ entries (Sinhala questions & answers). 
- `requirements.txt`: Key Python module dependencies required to build and run the application footprint smoothly.

---

## 4. Getting Started

### Prerequisites
- **Python 3.8+**
- **Ollama**: Required to run the local LLM. Download and install from [Ollama.com](https://ollama.com/).

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bahasuru-naya/Sinhala-Chatbot-for-Sri-Lanka-Department-of-Pensions.git
   cd Sinhala-Chatbot-for-Sri-Lanka-Department-of-Pensions
   ```

2. **Install the Python requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and Pull the local Language Model via Ollama**:
   Ensure the Ollama service is running. Pull the required model specific to this application:
   ```bash
   ollama pull gemma4:e2b
   ```

---

## 5. Usage

Launch the chatbot application by executing the Streamlit run command from the root directory:

```bash
streamlit run app.py
```

- A browser tab will automatically open directed to `http://localhost:8501`.
- Type your pension-related queries in Sinhala directly into the interface.
- The system will rapidly process the intent, retrieve the top answer contextually matching the query, and present a concise, helpful localized response generated via the language model.
