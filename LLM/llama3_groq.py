import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# llama3_groq.py
def call_llm(prompt: str, llm_name: str, temperature: float = 0.6, **kwargs) -> str:
    try:
        
        res = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        return f"[GROQ ERROR] {e}"

