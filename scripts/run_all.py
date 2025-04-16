# 📁 scripts/run_all.py

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.base_import import add_root_path
add_root_path()

# 📌 설정 불러오기
import json
from tools.paths import SETTING_JSON_PATH
with open(SETTING_JSON_PATH, encoding="utf-8") as f:
    config = json.load(f)

# ✅ 사용자 설정값
tool_list = list(config["study_matrix&difficulty"].keys())
difficulty_map = config["study_matrix&difficulty"]
llm = config["LLM"]
dataset_list = config["DATASET"]
count = config["count"]

# ✨ 기능 import
from generator.core.q_main import run_pipeline
from tools.store_manager import (
    save_structured_questions,
    save_llm_tags,
    save_comparison_log
)
from logs.log_reporter import save_log_report
from notion.notion_uploader import NotionUploader
from tools.clean_cache import clean_cache

# 1️⃣ 설정 출력
print("📌 설정 요약")
print(f"- 도구: {tool_list}")
print(f"- 난이도: {difficulty_map}")
print(f"- LLM: {llm}")
print(f"- 데이터셋: {dataset_list}")
print(f"- 호출 횟수: {count}")

# 2️⃣ 질문 생성 전체 파이프라인 실행 (a ~ p)
o_df, i_df, p_list = run_pipeline(
    tool_list, dataset_list, difficulty_map, count, llm
)

# 3️⃣ 결과 저장
save_structured_questions(o_df)
save_llm_tags(i_df)
save_comparison_log(p_list)

# 4️⃣ 리포트 저장
save_log_report()

# 5️⃣ Notion 업로드
uploader = NotionUploader()
uploader.upload()

# 6️⃣ 캐시 정리
clean_cache()
