import re
from datetime import datetime
import pandas as pd
from tools.paths import LOGS_DIR, RAW_QUESTIONS_PATH, CLEAN_QUESTIONS_PATH

# ✅ 접두어 제거 함수
def clean_question(text: str) -> str:
    prefixes = ["Q.", "Q:", "문제", "1.", "2.", "-", "*"]
    text = text.strip()
    for prefix in prefixes:
        if text.lower().startswith(prefix.lower()):
            text = text[len(prefix):].strip()
    return text

# ✅ 영어-only 필터 함수
def is_english_only(text: str) -> bool:
    return re.fullmatch(r"[a-zA-Z0-9\s\.,\-!?\(\)\[\]\"']+", text) is not None

# ✅ 전처리 함수: q_h → q_m
def preprocess_df(df: pd.DataFrame, log_fail: bool = True) -> pd.DataFrame:
    m_list = []
    removed = []

    for i, row in df.iterrows():
        original = str(row.get("q_h", "")).strip()
        cleaned = clean_question(original)

        if not cleaned:
            removed.append(("빈문장", original))
            m = ""
        elif len(cleaned) < 8:
            removed.append(("너무 짧음", original))
            m = ""
        elif is_english_only(cleaned):
            removed.append(("영어-only", original))
            m = ""
        else:
            m = cleaned

        # ✅ 변수 저장 + 리스트 저장
        globals()[f"q_m{row['num']}"] = m
        m_list.append(m)

    df = df.copy()
    df["q_m"] = m_list

    # ✅ 비어 있는 q_m 제거
    df = df[df["q_m"] != ""].reset_index(drop=True)

    # ✅ 로그 저장
    if log_fail and removed:
        now = datetime.now().strftime("%Y%m%d_%H%M")
        log_file = LOGS_DIR / f"preprocess_fail_{now}.txt"
        with open(log_file, "w", encoding="utf-8") as f:
            for reason, text in removed:
                f.write(f"[⛔ {reason}]\n{text}\n\n")
        print(f"🧹 전처리 로그 저장 완료 → {log_file.name}")
        print(f"✅ preprocess 완료: {len(df) + len(removed)}개 중 정제 {len(df)}개 / 제거 {len(removed)}개")

    return df
