# 📁 logs/log_reporter.py

import os, json
import pandas as pd
from datetime import datetime
from tools.paths import (
    SETTING_JSON_PATH, RAW_QUESTIONS_PATH, CLEAN_QUESTIONS_PATH,
    STRUCTURED_QUESTIONS_PATH, QUESTIONS_XLSX_PATH, LOG_REPORT_DIR
)

def count_lines(path):
    if not os.path.exists(path):
        return 0
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f if _.strip())

def count_json(path):
    if not os.path.exists(path):
        return 0
    with open(path, encoding="utf-8") as f:
        return len(json.load(f))

def save_log_report():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%Y-%m-%d %H:%M")
    log_path = LOG_REPORT_DIR / f"report_{date_str}.txt"

    with open(SETTING_JSON_PATH, encoding="utf-8") as f:
        config = json.load(f)

    raw_count = count_lines(RAW_QUESTIONS_PATH)
    clean_count = count_lines(CLEAN_QUESTIONS_PATH)
    final_count = count_json(STRUCTURED_QUESTIONS_PATH)
    deleted = raw_count - clean_count if raw_count > 0 else 0
    deletion_rate = f"{(deleted / raw_count * 100):.1f}%" if raw_count > 0 else "0%"

    lines = [
        f"📅 자동화 실행 리포트 - {time_str}\n",
        f"✅ 설정 요약:",
        f"- LLM: {config['LLM']}",
        f"- 도구: {list(config['study_matrix&difficulty'].keys())}",
        f"- 파일 형식: {config['file_type']}",
        f"- 데이터셋: {', '.join(config['DATASET'])}",
        f"- 호출 횟수: {config['count']}\n",

        f"📊 문제 생성 통계:",
        f"- raw 수집: {raw_count}개",
        f"- 전처리 후: {clean_count}개 (삭제 {deleted}개, {deletion_rate})",
        f"- 최종 구조화: {final_count}개\n"
    ]

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"📝 리포트 저장 완료 → {log_path.name}")
