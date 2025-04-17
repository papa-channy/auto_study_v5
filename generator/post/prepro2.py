import pandas as pd
import json
import uuid
from tools.paths import FINAL_XLSX_PATH, FINAL_PARQUET_PATH, RAW_QUESTIONS_PATH, CLEAN_QUESTIONS_PATH, COMPARISON_LOG_PATH, EX_LOG_PATH

def structure_questions(df: pd.DataFrame, i_list: list) -> pd.DataFrame:
    # 1. 예시 로그 저장
    if all(col in df.columns for col in ["ex_1", "ex_2"]):
        ex_log_df = df[["q_m", "ex_1", "ex_2"]]
        ex_log_df.to_excel(EX_LOG_PATH, index=False)
        print(f"📑 예시 로그 저장 완료 → {EX_LOG_PATH.name}")
        df.drop(columns=["ex_1", "ex_2"], inplace=True)
    else:
        print("⚠️ 예시 컬럼 없음 → 예시 로그 생략")

    # 2. q_h, q_m 저장
    df["q_h"].to_csv(RAW_QUESTIONS_PATH, index=False, header=False, mode="a")
    df["q_m"].to_csv(CLEAN_QUESTIONS_PATH, index=False, header=False, mode="a")

    # 3. 고유 ID 부여
    df["id"] = [uuid.uuid4().hex[:8] for _ in range(len(df))]

    # 4. 비교 로그 생성: {id: {LLM, tool, dataset, diffi, category}}
    log_dict = {}
    for idx, row in df.iterrows():
        llm_i = i_list[idx]  # [LLM, tool, dataset, diffi, category, ex1, ex2, ex3]
        log_dict[row["id"]] = {
            "LLM": row["LLM"],
            "tool": row["s_m"],
            "dataset": row["dataset"],
            "diffi": llm_i[3],
            "category": llm_i[4]
        }

    with open(COMPARISON_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_dict, f, indent=4, ensure_ascii=False)
    print(f"📊 비교 로그 저장 완료 → {COMPARISON_LOG_PATH.name}")

    # 5. 컬럼 정리
    df.rename(columns={"q_m": "question", "s_m": "tool", "diffi": "difficulty", "LLM": "llm"}, inplace=True)
    final_df = df[["tool", "dataset", "difficulty", "category", "llm", "question", "id"]]

    # 6. 저장
    final_df.to_excel(FINAL_XLSX_PATH, index=False)
    final_df.to_parquet(FINAL_PARQUET_PATH, index=False)
    print("✅ 구조화 및 저장 완료")

    return final_df
