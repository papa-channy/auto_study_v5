# run_all.py
import os
from generator.prompt.conf_p import df_template, llm
from generator.core.q_main import run_pipeline
# from notion.notion_uploader import upload_to_notion
# from notebooks.effitudy import EffiNotebookGenerator
import pandas as pd
import nbformat
import os
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
def main():
    # 1️⃣ 문제 생성 파이프라인 실행
    clear_terminal()
    o_df = run_pipeline(df_template, llm)

    # 2️⃣ 결과 저장
    o_df.to_parquet("data/f_data.parquet", index=False)
    o_df.to_excel("data/finaldata.xlsx", index=False)
    print("✅ 문제 생성 및 저장 완료")

    # 3️⃣ Notion 업로드 (❌ 초기엔 주석 처리)
    """
    from notion.notion_uploader import upload_to_notion
    upload_to_notion("data/finaldata.xlsx")
    print("🧠 Notion 업로드 완료")
    """

    # 4️⃣ 노트북 생성 (EffiStudy 기준, ❌ 초기엔 주석 처리)
    """
    from notebooks.effitudy import EffiNotebookGenerator

    for tool in o_df["tool"].unique():
        path = f"notebooks/{tool}.ipynb"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                nb = nbformat.read(f, as_version=4)
            existing_cells = nb.cells
        else:
            existing_cells = []

        generator = EffiNotebookGenerator(
            df=o_df[o_df["tool"] == tool],
            tool_name=tool,
            existing_cells=existing_cells
        )
        generator.run()
    print("📓 노트북 생성 완료")
    """

if __name__ == "__main__":
    main()
