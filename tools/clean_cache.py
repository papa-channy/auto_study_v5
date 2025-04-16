# 📁 tools/clean_cache.py

import os
import shutil

EXCLUDE_DIRS = ["venv", ".git"]
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def delete_if(pattern, path):
    if pattern in path:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            print(f"🧹 삭제됨: {path}")
        except Exception as e:
            print(f"⚠️ 삭제 실패: {path} → {e}")

def clean_cache():
    count = 0
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        # 제외할 폴더는 스킵
        if any(skip in dirpath for skip in EXCLUDE_DIRS):
            continue

        # 🔸 1. __pycache__ 폴더
        for d in dirnames:
            if d == "__pycache__" or ".ipynb_checkpoints" in d:
                delete_if(d, os.path.join(dirpath, d))
                count += 1

        # 🔸 2. .pyc, .log, .tmp, .bak 파일
        for f in filenames:
            if f.endswith((".pyc", ".log", ".tmp", ".bak")):
                delete_if(f, os.path.join(dirpath, f))
                count += 1

    print(f"\n✅ 캐시/임시 파일 정리 완료: {count}개 항목 삭제됨")

if __name__ == "__main__":
    clean_cache()
