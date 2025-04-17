import json
import time
from generator.prompt.conf_p import prompt_extract_tags
from LLM.llm_selector import generate_by_llm
from tools.paths import KEYWORDS_JSON_PATH


def load_keywords():
    with open(KEYWORDS_JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


def auto_classify(text: str, keyword_map: dict) -> str:
    for category, keywords in keyword_map.items():
        if any(k in text for k in keywords):
            return category
    return "기타"


def classify_questions(df, llm_name):
    results = []

    for i, row in df.iterrows():
        prompt_n = prompt_extract_tags(row["q_m"])
        success = False
        response = ""

        for try_num in range(3):
            try:
                print(f"[LLM_i] 🔁 Try {try_num+1} for row {i}")
                response = generate_by_llm(
                    prompt=prompt_n,
                    llm_name=llm_name,
                    tool=row["s_m"],
                    count=1
                ).strip()
                success = True
                break
            except Exception as e:
                print(f"[ERROR_i] row {i}, 시도 {try_num+1}: {e}")
                if "429" in str(e):
                    time.sleep(8)
                else:
                    time.sleep(2)

        if not success:
            response = "[GROQ ERROR] classify_questions 실패"

        results.append(response)
        time.sleep(1.5)

    return results
