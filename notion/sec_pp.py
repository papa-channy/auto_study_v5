# 📁 notion/sec_pp.py

import pandas as pd
from tools.paths import STRUCTURED_QUESTIONS_PATH

def prepare_for_notion(tool_filter=None):
    """
    ✅ questions.json → Notion 업로드용 포맷으로 정제
    - 누락 필드 보정
    - 빈 질문 제거
    - 특정 도구만 필터링 (optional)
    - ID 포함
    """

    try:
        df = pd.read_json(STRUCTURED_QUESTIONS_PATH)
    except Exception as e:
        print(f"📭 구조화 문제 파일 로딩 실패: {e}")
        return []

    # 1. 유효 질문 필터링
    df = df[df["question"].notnull() & (df["question"].str.strip() != "")]

    # 2. tool 필터링 (선택)
    if tool_filter:
        df = df[df["tool"].isin(tool_filter)]

    # 3. 누락 필드 기본값 처리
    defaults = {
        "tool": "unknown", "dataset": "unknown", "difficulty": "중", "category": "기타", "id": "UNKNOWN"
    }
    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = default
        else:
            df[col].fillna(default, inplace=True)

    print(f"✅ Notion 업로드용 정제 완료: {len(df)}개")
    return df[["id", "tool", "dataset", "difficulty", "category", "question"]].to_dict(orient="records")
