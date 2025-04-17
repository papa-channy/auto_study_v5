import pandas as pd
from LLM.llm_selector import generate_by_llm
from generator.prompt.conf_p import prompt_enhance_difficulty, prompt_enhance_reasoning
import time
from LLM.llm_selector import call_llm
def generate_question_f(df_template: pd.DataFrame, prompt_dict: dict, llm_name: str) -> pd.DataFrame:
    df_template = df_template.copy()

    for i, row in df_template.iterrows():
        prompt_j = prompt_dict.get(str(row["num"]))
        if not prompt_j:
            continue

        try:
            q_f = generate_by_llm(prompt=prompt_j, tool=row["s_m"], count=1, llm_name=llm_name).strip()
        except Exception as e:
            q_f = f"[ERROR_f] {e}"

        globals()[f"q_f{row['num']}"] = q_f
        df_template.at[i, "q_f"] = q_f

    return df_template


def generate_question_g(df_template: pd.DataFrame, llm_name: str) -> pd.DataFrame:
    df_template = df_template.copy()

    for i, row in df_template.iterrows():
        f = row.get("q_f", "")
        if not f:
            continue

        try:
            prompt_k = prompt_enhance_difficulty(f)
            q_g = generate_by_llm(prompt=prompt_k, tool=row["s_m"], count=1, llm_name=llm_name).strip()
        except Exception as e:
            q_g = f"[ERROR_g] {e}"

        globals()[f"q_g{row['num']}"] = q_g
        df_template.at[i, "q_g"] = q_g

    df_template.drop(columns=["q_f"], inplace=True)
    return df_template


def generate_question_h(df_g, llm_name):
    results = []

    for i, row in df_g.iterrows():
        prompt = prompt_enhance_reasoning(row["q_g"])

        success = False
        response = ""
        for try_num in range(3):  # ✅ 최대 3번 재시도
            try:
                print(f"[LLM_h] 🔁 Try {try_num+1} for row {i}")
                response = call_llm(
                    prompt=prompt,
                    llm_name=llm_name,
                    tool=row["s_m"],  # ✅ kwargs 대응
                    count=1
                ).strip()
                success = True
                break
            except Exception as e:
                print(f"[ERROR_h] row {i}, 시도 {try_num+1}: {e}")
                time.sleep(2.5)  # ✅ 실패 시 대기 후 재시도

        if not success:
            response = "[GROQ ERROR] LLM 호출 실패 (최대 재시도 초과)"
        print(f"[LLM_h] ✅ row {i} 완료: 응답 길이 {len(response)}자")
        results.append(response)
        time.sleep(1.5)  # ✅ 호출 간 최소 대기시간 확보

    df_g["q_h"] = results
    return df_g