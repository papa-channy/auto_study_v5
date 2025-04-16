# 📁 generator/post/connected_log.py

import pandas as pd

def connect_setting_vs_llm(o_df: pd.DataFrame, i_df: pd.DataFrame, llm_name: str) -> list:
    """
    ✅ 사용자 설정 vs LLM 태그 비교 로그 생성 (user/llm 나란히 저장)
    - 마지막 행은 ["id", "llm"]만 리스트로 info 필드에 저장
    """
    log_list = []

    for idx in range(len(o_df)):
        o_row = o_df.iloc[idx][["tool", "dataset", "difficulty", "category"]]
        i_row = i_df.iloc[idx][["tool", "dataset", "difficulty", "category"]]

        combined = pd.concat([o_row, i_row], axis=1)
        combined.columns = ["user", "llm"]

        # 🔧 딕셔너리 형태를 [user, llm] 리스트로 변환
        formatted = {
            k: [v["user"], v["llm"]]
            for k, v in combined.to_dict(orient="index").items()
        }

        # 🎯 마지막 info는 리스트로만 저장
        formatted["info"] = [o_df.iloc[idx]["id"], llm_name]

        log_list.append(formatted)

    return log_list
