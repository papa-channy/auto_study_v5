import pandas as pd
from generator.prompt.conf_p import df_template
from generator.prompt.p_gen import generate_prompt_j
from generator.core.q_raw_generator import generate_question_f, generate_question_g, generate_question_h
from generator.post.preprocess import preprocess_df
from generator.core.q_classifier import classify_questions
from generator.post.prepro2 import structure_questions


def run_pipeline(m_df, llm_name):
    from generator.prompt.conf_p import df_template
    print("🚀 파이프라인 실행 시작")
    # Step 1: 프롬프트 생성 (j = a + e)
    prompts_j, ex_df = generate_prompt_j(df_template, m_df)
    
    # ✅ 예시 붙이기
    df_template = df_template.reset_index(drop=True)
    ex_df = ex_df.reset_index(drop=True)
    df_template = pd.concat([df_template, ex_df], axis=1)

    # Step 2~5 동일
    df_f = generate_question_f(df_template.copy(), prompts_j, llm_name)
    df_g = generate_question_g(df_f, llm_name)
    df_h = generate_question_h(df_g, llm_name)
    df_m = preprocess_df(df_h)
    i_list = classify_questions(df_m, llm_name)
    o_df = structure_questions(df_m, i_list)
    print("✅ run_pipeline() 완료 → 문제 수:", len(o_df))
    return o_df

