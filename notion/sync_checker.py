# 📁 notion/sync_checker.py

import os
import pandas as pd
from dotenv import load_dotenv
from notion_client import Client
from tools.paths import STRUCTURED_QUESTIONS_PATH, ENV_PATH

def load_notion_ids(notion, database_id):
    """Notion DB에서 현재 등록된 문제 ID들 추출"""
    ids = []
    has_more = True
    start_cursor = None

    while has_more:
        response = notion.databases.query(
            database_id=database_id,
            start_cursor=start_cursor
        ) if start_cursor else notion.databases.query(database_id=database_id)

        for row in response["results"]:
            props = row.get("properties", {})
            notion_id = props.get("id", {}).get("title", [])
            if notion_id and notion_id[0]["plain_text"]:
                ids.append(notion_id[0]["plain_text"])

        has_more = response.get("has_more", False)
        start_cursor = response.get("next_cursor")

    return set(ids)

def check_sync_status():
    # 1. questions.json 로드
    df = pd.read_json(STRUCTURED_QUESTIONS_PATH)

    # 2. Notion API 설정
    load_dotenv(dotenv_path=ENV_PATH)
    notion = Client(auth=os.getenv("NOTION_API_KEY"))
    db_id = os.getenv("NOTION_DATABASE_ID")

    # 3. Notion에서 업로드된 ID 수집
    notion_ids = load_notion_ids(notion, db_id)
    local_ids = set(df["id"].dropna().astype(str))

    # 4. 비교
    missing = sorted(list(local_ids - notion_ids))
    print(f"\n✅ 총 문제 수: {len(local_ids)}")
    print(f"📤 Notion 등록: {len(notion_ids)}")
    print(f"⚠️ 누락된 ID: {len(missing)}개")

    if missing:
        with open("logs/notion_missing_log.txt", "w", encoding="utf-8") as f:
            for mid in missing:
                f.write(mid + "\n")
        print("📁 누락 로그 저장: logs/notion_missing_log.txt")

    return missing
