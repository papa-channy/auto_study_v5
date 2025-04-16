# 📁 generator/core/q_main.py
import pandas as pd
from generator.prompt.p_gen import generate_prompt_question
from generator.core.q_raw_generator import generate_raw_questions
from generator.core.q_enhancer import enhance_difficulty, enhance_reasoning
from generator.core.q_classifier import classify_questions
from generator.post.preprocess import preprocess_questions
from generator.post.prepro2 import structure_questions
from generator.post.connected_log import connect_setting_vs_llm

def run_pipeline(tool_list, dataset_list, difficulty_map, count, llm):
    # 1️⃣ 초기 df 선언
    o_df = pd.DataFrame(columns=["tool", "dataset", "difficulty", "category", "question", "id"])
    i_df = pd.DataFrame(columns=["tool", "dataset", "difficulty", "category", "keywords"])

    p_list = []

    # 2️⃣ 루프 돌면서 row 생성 & 누적
    for tool in tool_list:
        kor_tool = tool.upper()
        difficulty_list = difficulty_map[tool]
        recent_examples = "- (중) 샘플 예시 없음"

        # j = a + e
        j = generate_prompt_question(kor_tool, dataset_list, difficulty_list, count, recent_examples)

        # f → g → h
        f = generate_raw_questions(j, llm)
        g = enhance_difficulty(f, llm)
        h = enhance_reasoning(g, llm)

        # h → m → o
        m = preprocess_questions(h)
        o_rows = structure_questions(m, tool)  # ✅ list of dict
        i_rows = classify_questions(o_rows, llm)  # ✅ list of dict

        # ➕ DataFrame으로 한 줄씩 append
        for o_row, i_row in zip(o_rows, i_rows):
            next_idx = len(o_df)
            o_df.loc[next_idx] = [
                o_row["tool"], o_row["dataset"], o_row["difficulty"],
                o_row["category"], o_row["question"], o_row["id"]
            ]
            i_df.loc[next_idx] = [
                i_row["tool"], i_row["dataset"], i_row["difficulty"],
                i_row["category"], i_row["keywords"]
            ]

        # 🔁 p 생성 → 누적
        p_list.extend(connect_setting_vs_llm(o_df.iloc[-len(o_rows):], i_df.iloc[-len(i_rows):], llm))

        print(f"✅ [{tool}] 처리 완료: {len(o_rows)}문제")

    # 3️⃣ 리턴
    return o_df, i_df, p_list
