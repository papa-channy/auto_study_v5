import os
from datetime import datetime
from tools.paths import LOGS_DIR

# ✅ 터미널 클리어 함수
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

# ✅ 터미널 + 파일 동시 출력 함수
def print_and_log(text, file_path):
    print(text)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(text + "\n")

# ✅ 최근 리포트 읽기 (report_YYYY-MM-DD.txt)
def get_latest_report():
    report_dir = LOGS_DIR / "report"
    if not report_dir.exists():
        return None

    reports = sorted(report_dir.glob("report_*.txt"), reverse=True)
    return reports[0] if reports else None

# ✅ 메인 실행
def main():
    clear_terminal()
    print("📋 최신 실행 로그 요약\n")

    latest = get_latest_report()
    if latest is None:
        print("❌ 실행 로그 파일이 없습니다.")
        return

    log_path = LOGS_DIR / "log_reporter_history.txt"
    print_and_log(f"🕒 [{datetime.now().strftime('%Y-%m-%d %H:%M')}] 읽은 로그: {latest.name}", log_path)
    print()

    with open(latest, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            print_and_log(line, log_path)

if __name__ == "__main__":
    main()
