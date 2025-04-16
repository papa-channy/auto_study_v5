# 📁 tools/paths.py

from pathlib import Path

# 🔹 루트 디렉토리
BASE_DIR = Path(__file__).resolve().parent.parent

# ───────────────────────────────────────────────
# 📁 config (설정)
CONFIG_DIR = BASE_DIR / "config"
SETTING_JSON_PATH = CONFIG_DIR / "setting_config.json"
KEYWORDS_JSON_PATH = CONFIG_DIR / "keywords.json"
AVAILABLE_OPTION_PATH = CONFIG_DIR / "available_option.json"
STORAGE_POLICY_PATH = CONFIG_DIR / "storage_policy.json"

# ───────────────────────────────────────────────
# 📁 data (질문 및 태그 저장)
DATA_DIR = BASE_DIR / "data"
RAW_QUESTIONS_PATH = DATA_DIR / "raw_questions.txt"           # h
CLEAN_QUESTIONS_PATH = DATA_DIR / "clean_questions.txt"       # m
STRUCTURED_QUESTIONS_PATH = DATA_DIR / "questions.json"       # o
QUESTIONS_XLSX_PATH = DATA_DIR / "questions.xlsx"             # o
LLM_TAGS_PATH = DATA_DIR / "llm_tags.json"                    # i

# ───────────────────────────────────────────────
# 📁 examples (예시)
EXAMPLES_DIR = BASE_DIR / "examples"
EX_PDS_PATH = EXAMPLES_DIR / "ex_pds.json"
EX_SQL_PATH = EXAMPLES_DIR / "ex_sql.json"
EX_MPL_PATH = EXAMPLES_DIR / "ex_matplotlib.json"

# ───────────────────────────────────────────────
# 📁 generator 경로 (프롬프트, 예시 등)
GENERATOR_DIR = BASE_DIR / "generator"
PROMPT_DIR = GENERATOR_DIR / "prompt"

# ───────────────────────────────────────────────
# 📁 logs
LOG_DIR = BASE_DIR / "logs"
LOG_REPORT_DIR = LOG_DIR / "report"
COMPARISON_JSON_PATH = LOG_DIR / "q_comparison_log.json"      # p
COMPARISON_XLSX_PATH = LOG_DIR / "q_comparison_log.xlsx"      # p
UPLOAD_FAIL_LOG_PATH = LOG_DIR / "upload_fails.txt"
NOTION_MISSING_LOG_PATH = LOG_DIR / "notion_missing_log.txt"

# ───────────────────────────────────────────────
# 📁 notebooks
NOTEBOOK_DIR = BASE_DIR / "notebooks"
NOTEBOOK_PDS_PATH = NOTEBOOK_DIR / "qpds.ipynb"
NOTEBOOK_SQL_PATH = NOTEBOOK_DIR / "qsql.ipynb"
NOTEBOOK_VIZ_PATH = NOTEBOOK_DIR / "qviz.ipynb"
NOTEBOOK_MPL_PATH = NOTEBOOK_DIR / "matplotlib.ipynb"

# ───────────────────────────────────────────────
# 🧪 기타
ENV_PATH = BASE_DIR / ".env"
