import json
import pandas as pd
from pathlib import Path
from a import prompt_settings
# ─────────────────────────────────────
# 📁 설정 파일 로딩
# ─────────────────────────────────────
SETTING_PATH = Path("config/setting_config.json")
with open(SETTING_PATH, "r", encoding="utf-8") as f:
    setting = json.load(f)

difficulty_map = setting["study_matrix&difficulty"]
tool_list = list(difficulty_map.keys())  # ✅ tool_list 자동 추출
dataset_list = setting["DATASET"]
count = setting["count"]
llm = setting["LLM"]
filetype = setting["file_type"]

# ─────────────────────────────────────
# 📄 df_template 생성 (q_a ~ q_m 컬럼 포함)
# ─────────────────────────────────────
columns = [
    "num", "s_m", "dataset", "diffi", "category", "LLM", "f_t", "id", "q_m",
    "q_a", "q_j", "q_k", "q_l", "q_n", "q_f", "q_g", "q_h"
]

rows = []
idx = 1
for tool in tool_list:
    for dataset in dataset_list:
        for difficulty in difficulty_map.get(tool, []):  # ✅ 안전하게 get() 사용
            for _ in range(count): # count 만큼 반복
                row = {
                    "num": idx,
                    "s_m": tool,
                    "dataset": dataset,
                    "diffi": difficulty,
                    "category": "",
                    "LLM": llm,
                    "f_t": filetype,
                    "id": "",
                    "q_m": "",
                    "q_a": "",
                    "q_j": "",
                    "q_k": "",
                    "q_l": "",
                    "q_n": "",
                    "q_f": "",
                    "q_g": "",
                    "q_h": ""
                }
                rows.append(row)
                idx += 1

df_template = pd.DataFrame(rows, columns=columns)


# ─────────────────────────────────────
# 🎯 프롬프트 생성 함수들
# ─────────────────────────────────────

def prompt_question_generation(row):
    a = """{kor_tool}라이브러리 를 {dataset_line} 데이터셋으로
{count}개 만들거야. 문제는 반드시 한국어로 작성하고 용어만 영어로 하고 한국어로 해줘
예시 참고 다양한 키워드로 질문 문장만 생성해줘()
예시:"""
    return a.format(
        kor_tool=row["s_m"],
        dataset_line=row["dataset"],
        difficulty_line=row["diffi"],
        count=1
    )

def prompt_enhance_difficulty(question_f: str):
    return f"""아래의 기본 문제의 복잡도, 추론 수준을 높여서
    중상급 수준의 문제로 발전시켜줘
    반드시 한국어로 작성(일부 영어는 사용 가능)
    {question_f}
"""

def prompt_enhance_reasoning(question_g: str):
    return f"""
    {question_g}
    해당 문제가 영어로 되어있으면 한글로 바꿔주고 중급자가 풀 수 있도록 해줘줘

"""

def prompt_extract_tags(question_m: str):
    return f"""{question_m} 이 문제는 데이터 분석 관련 문제야야
- 키워드는는 문제에서 필요한 분석 기술, 개념 (예: groupby, 회귀, 시각화 등)
- 키워드는 최대 3개만
📝 문제:

"""
