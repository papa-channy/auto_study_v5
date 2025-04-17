import pandas as pd
from tools.paths import FINAL_XLSX_PATH

def load_final_df() -> pd.DataFrame:
    """최종 o 파일 불러오기"""
    return pd.read_excel(FINAL_XLSX_PATH)

def format_for_notion(df: pd.DataFrame, tool_filter=None) -> pd.DataFrame:
    """
    노션 업로드용 포맷으로 정리:
    - 빈 질문 제거
    - 도구(tool) 필터 가능
    - 컬럼명 정리 (LLM 제거)
    """
    df = df.copy()

    # 1. 필터링
    df = df[df["question"].notnull() & (df["question"].str.strip() != "")]
    if tool_filter:
        df = df[df["s_m"].isin(tool_filter)]

    # 2. 필요 컬럼만 추리고 LLM 제거
    df = df[["id", "s_m", "dataset", "diffi", "category", "question"]]

    # 3. 컬럼명 통일
    df.rename(columns={
        "s_m": "Tool",
        "dataset": "Dataset",
        "diffi": "Difficulty",
        "category": "Category",
        "question": "Question"
    }, inplace=True)

    # 4. index 설정
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    df.index.name = "No"

    return df

# 테스트
if __name__ == "__main__":
    df = load_final_df()
    notion_df = format_for_notion(df)
    print(notion_df.head())
