# 📁 tools/store_manager.py

import json

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 JSON 저장 완료 → {path}")

import pandas as pd
from tools.paths import (
    RAW_QUESTIONS_PATH, CLEAN_QUESTIONS_PATH,
    LLM_TAGS_PATH, STRUCTURED_QUESTIONS_PATH, QUESTIONS_XLSX_PATH,
    COMPARISON_JSON_PATH, COMPARISON_XLSX_PATH
)

# ✅ 1. Raw 질문 저장 (h)
def save_raw_questions(df: pd.DataFrame):
    df.to_csv(RAW_QUESTIONS_PATH, index=False, header=False, encoding="utf-8")
    print(f"✅ raw_questions.txt 저장 완료 ({len(df)}개)")

# ✅ 2. Clean 질문 저장 (m)
def save_clean_questions(df: pd.DataFrame):
    df.to_csv(CLEAN_QUESTIONS_PATH, index=False, header=False, encoding="utf-8")
    print(f"✅ clean_questions.txt 저장 완료 ({len(df)}개)")

# ✅ 3. LLM 분류 결과 저장 (i)
def save_llm_tags(df: pd.DataFrame):
    df.to_json(LLM_TAGS_PATH, force_ascii=False, orient="values", indent=2)
    print(f"✅ llm_tags.json 저장 완료 ({len(df)}개)")

# ✅ 4. 구조화 질문 저장 (o)
def save_structured_questions(df: pd.DataFrame):
    df.to_json(STRUCTURED_QUESTIONS_PATH, force_ascii=False, orient="records", indent=2)
    df.to_excel(QUESTIONS_XLSX_PATH, index=False)
    print(f"✅ questions.json / questions.xlsx 저장 완료 ({len(df)}개)")

# ✅ 5. 비교 로그 저장 (p)
def save_comparison_log(df: pd.DataFrame):
    df.to_json(COMPARISON_JSON_PATH, force_ascii=False, orient="records", indent=2)
    df.to_excel(COMPARISON_XLSX_PATH, index=False)
    print(f"✅ q_comparison_log.json / .xlsx 저장 완료 ({len(df)}개)")
