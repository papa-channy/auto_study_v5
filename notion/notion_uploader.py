import os
import json
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

from tools.paths import ENV_PATH, KEYWORDS_JSON_PATH
from notion.sec_pp import prepare_for_notion


class NotionUploader:
    def __init__(self):
        load_dotenv(dotenv_path=ENV_PATH)
        self.api_key = os.getenv("NOTION_API_KEY")
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        self.notion = Client(auth=self.api_key)

        print(f"🔐 NOTION_API_KEY 시작: {self.api_key[:10]}...")
        print(f"📘 NOTION_DATABASE_ID: {self.database_id}")

        self.keyword_map = self.load_keyword_map(KEYWORDS_JSON_PATH)
        self.fail_log_path = "logs/upload_fails.txt"

    def load_keyword_map(self, path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def classify(self, text):
        """category가 비어 있을 경우 keywords.json 기반으로 자동 분류"""
        categories = []
        for category, keywords in self.keyword_map.items():
            if any(k in text for k in keywords):
                categories.append(category)
        return list(set(categories)) or ["기타"]

    def upload(self, tool_filter=None):
        questions = prepare_for_notion(tool_filter)
        if not questions:
            print("📭 업로드할 질문이 없습니다.")
            return

        success, fail = 0, 0
        today = datetime.now().strftime("%Y-%m-%d")

        for i, q in enumerate(questions, 1):
            try:
                category_list = [q["category"]] if q["category"] else self.classify(q["question"])
                props = {
                    "id": {"title": [{"text": {"content": q["id"]}}]},
                    "날짜": {"rich_text": [{"text": {"content": today}}]},
                    "dataset": {"select": {"name": q["dataset"]}},
                    "문제": {"rich_text": [{"text": {"content": q["question"]}}]},
                    "분류": {"multi_select": [{"name": tag} for tag in category_list]},
                    "난이도": {"select": {"name": q["difficulty"]}},
                    "상태": {"select": {"name": "미풀이"}}
                }

                self.notion.pages.create(parent={"database_id": self.database_id}, properties=props)
                success += 1
                print(f"✅ {i} 업로드 성공 | [{q['id']}] | 분류: {', '.join(category_list)}")
            except Exception as e:
                fail += 1
                print(f"❌ {i} 업로드 실패 | {q['id']} → {e}")
                with open(self.fail_log_path, "a", encoding="utf-8") as f:
                    f.write(f"[{q['id']}] {q['question'][:80]}... → {e}\n")

        print(f"\n📤 업로드 요약: 성공 {success}개 / 실패 {fail}개")
