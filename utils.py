import pandas as pd
import ollama
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load embedding model
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Load dataset
df = pd.read_csv("dataset.csv")

questions = df['sinhala_question'].tolist()
answers = df['sinhala_answer'].tolist()

# Precompute embeddings
question_embeddings = model.encode(questions)


def search_answer(user_input):
    user_embedding = model.encode([user_input])

    similarities = cosine_similarity(user_embedding, question_embeddings)
    best_idx = similarities.argmax()
    best_score = similarities.max()

    return best_idx, best_score


def generate_response(user_input):
    idx, score = search_answer(user_input)

    # Fallback condition
    if score < 0.5:
        return "සමාවෙන්න, ඔබගේ ප්‍රශ්නයට සම්බන්ධ තොරතුරු සොයාගත නොහැකි විය. කරුණාකර ප්‍රශ්නය වෙනත් ආකාරයකින් හෝ වැඩි විස්තර සහිතව නැවත විමසන්න."

    matched_answer = answers[idx]

    # Domain restriction added
    prompt = f"""
    ඔබ ශ්‍රී ලංකා විශ්‍රාම වැටුප් දෙපාර්තමේන්තුවේ chatbot එකක්.

    විස්තරාත්මකව හිතන්න එපා.
    reasoning output නොදක්වන්න.
    සෘජු පිළිතුරක් දෙන්න.

    නීති:
    - පහත "සම්බන්ධ තොරතුරු" හි අන්තර්ගතය හිස් නොවේ නම්, ඒකම පදනම් කරගෙන පිළිතුර ලබා දෙන්න.
    - "සම්බන්ධ තොරතුරු" හිස් නම්, ඔබගේ සාමාන්‍ය දැනුම භාවිතා කර සරල පිළිතුරක් දෙන්න.
    - අනවශ්‍ය විස්තර එකතු නොකරන්න.

    ප්‍රශ්නය: {user_input}

    සම්බන්ධ තොරතුරු: {matched_answer}

    Sinhala භාෂාවෙන් පමණක් පිළිතුරු දෙන්න.
    """

    response = ollama.chat(
    model="gemma4:e2b",
    messages=[
        {
            "role": "system",
            "content": """
            ඔබ ශ්‍රී ලංකා විශ්‍රාම වැටුප් දෙපාර්තමේන්තුවේ chatbot එකක්.

            Thinking mode භාවිතා නොකරන්න.
            reasoning output නොදක්වන්න.
            සෘජු පිළිතුරු පමණක් දෙන්න.
            """
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    options={        
        "temperature": 0.8,
        "top_p": 0.95,
        "top_k": 64
    }
    )

    print(f"Similarity Score: {score:.4f}")
    print(f"Matched Question: {questions[idx]}")
    print(f"Matched Answer: {matched_answer}")  
    print(f"Generated Response: {response['message']['content']}")
    
    return response['message']['content']