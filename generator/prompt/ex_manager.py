import os
import json
import pandas as pd
from pathlib import Path
from tools.paths import EXAMPLES_DIR


def get_example_series(kor_tool: str, m_df: pd.DataFrame, total_required: int, max_cache: int = 30) -> tuple[pd.DataFrame, int]:
    """
    kor_tool에 해당하는 예시 시리즈를 반환한다.
    없거나 부족할 경우 m_df를 참고해 예시를 채우고, 최대 max_cache개까지만 유지한다.
    반환: 예시 3개를 ex_1~3 컬럼으로 갖는 DataFrame
    """
    path = EXAMPLES_DIR / f"ex_{kor_tool}.json"

    # 1. 예시 파일 없으면 생성
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)

    # 2. 예시 불러오기 or 비어있을 경우 채우기
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    if not data:
        if "question" not in m_df.columns:
            raise ValueError("m_df에는 'question' 열이 있어야 합니다")
        sample_questions = m_df["question"].dropna().tolist()[:max_cache]
        data = {str(i + 1): q for i, q in enumerate(sample_questions)}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # 3. 오래된 예시 삭제
    s = pd.Series(data)
    s.index = s.index.astype(int)
    s = s.sort_index()
    if len(s) > max_cache:
        s = s.iloc[-max_cache:]
        trimmed = {str(i + 1): v for i, v in enumerate(s.values)}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(trimmed, f, indent=4, ensure_ascii=False)

    # 4. 예시 반복 확장 후 3개씩 분배
    reps = (total_required * 3 + len(s) - 1) // len(s)
    extended = (s.tolist() * reps)[:total_required * 3]

    rows = []
    for i in range(total_required):
        ex1 = f"ex_{extended[i*3]}"
        ex2 = f"ex_{extended[i*3+1]}"
        rows.append({"ex_1": ex1, "ex_2": ex2})

    ex_df = pd.DataFrame(rows, index=range(1, total_required + 1))
    return ex_df, total_required
