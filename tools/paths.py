from pathlib import Path

# ─────────────────────────────────────────────
# 📁 프로젝트 최상위 경로
# ─────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────
# 📁 주요 폴더 경로
# ─────────────────────────────────────────────
CONFIG_DIR = ROOT_DIR / "config"
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"
EXAMPLES_DIR = ROOT_DIR / "examples"
LLM_DIR = ROOT_DIR / "LLM"
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"
GENERATOR_DIR = ROOT_DIR / "generator"
TOOLS_DIR = ROOT_DIR / "tools"
SCRIPTS_DIR = ROOT_DIR / "scripts"
OPT_SET_DIR = ROOT_DIR / "opt_set"
SETUP_DIR = ROOT_DIR / "setup"
NOTION_DIR = ROOT_DIR / "notion"

# ─────────────────────────────────────────────
# 📄 config 파일 경로
# ─────────────────────────────────────────────
SETTING_PATH = CONFIG_DIR / "setting_config.json"
AVAILABLE_OPTION_PATH = CONFIG_DIR / "available_option.json"
STORAGE_POLICY_PATH = CONFIG_DIR / "storage_policy.json"
KEYWORDS_JSON_PATH = CONFIG_DIR / "keywords.json"

# ─────────────────────────────────────────────
# 📄 데이터 저장 경로
# ─────────────────────────────────────────────
FINAL_XLSX_PATH = DATA_DIR / "finaldata.xlsx"
FINAL_PARQUET_PATH = DATA_DIR / "f_data.parquet"
RAW_QUESTIONS_PATH = DATA_DIR / "raw_questions.txt"
CLEAN_QUESTIONS_PATH = DATA_DIR / "clean_questions.txt"

# ─────────────────────────────────────────────
# 📄 로그 저장 경로
# ─────────────────────────────────────────────
EX_LOG_PATH = LOGS_DIR / "ex_log.xlsx"
COMPARISON_LOG_PATH = LOGS_DIR / "q_comparison_log.json"
PREPROCESS_FAIL_PATH = LOGS_DIR / "preprocess_fail.txt"
REPORT_DIR = LOGS_DIR / "report"

# ─────────────────────────────────────────────
# 📄 예시 저장 경로
# ─────────────────────────────────────────────
EXAMPLES_DIR = ROOT_DIR / "examples"
