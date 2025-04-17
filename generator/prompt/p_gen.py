import pandas as pd
from generator.prompt.ex_manager import get_example_series
from generator.prompt.conf_p import prompt_question_generation

def generate_prompt_j(df_template, m_df) -> tuple[dict, pd.DataFrame]:
    """
    df_template과 예시 시리즈를 이용해 j 프롬프트 (a + e) 딕셔너리 반환
    + ex_1~3이 q_m을 유도한 예시로 정확히 동기화된 ex_df 반환
    """
    total = len(df_template)
    kor_tool = df_template.iloc[0]["s_m"]

    # ✅ 예시 생성
    ex_df, _ = get_example_series(kor_tool, m_df, total_required=total)

    # ✅ index 동기화
    df = df_template.copy()
    df.index = range(1, len(df) + 1)
    ex_df.index = df.index

    # ✅ 프롬프트 딕셔너리 생성 + 예시 추출
    prompt_j_dict = {}

    for i, (row, ex_row) in enumerate(zip(df.itertuples(), ex_df.itertuples()), start=1):
        prompt_a = prompt_question_generation(row._asdict())
        examples = [ex_row.ex_1, ex_row.ex_2]
        examples_str = "\n\n".join(f"- {ex}" for ex in examples)

        prompt_j = f"{prompt_a}\n\n📌 최근 예시:\n{examples_str}"
        prompt_j_dict[str(row.num)] = prompt_j

    return prompt_j_dict, ex_df

