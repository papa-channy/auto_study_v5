import os
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from collections import defaultdict
from tools.paths import NOTEBOOK_DIR

class EffiNotebookGenerator:
    def __init__(self, df, tool_name: str, existing_cells: list, max_problem_per_file=20):
        self.df = df
        self.tool_name = tool_name
        self.existing_cells = existing_cells
        self.max_problem = max_problem_per_file

        self.existing_id_map = {}
        self.existing_fmt_map = {}
        self.a_group = []
        self.b_group = []
        self.sequence = []
        self._chunks = []

    def _parse_existing(self):
        for cell in self.existing_cells:
            if cell.cell_type != "markdown" or "문제 ID:" not in cell.source:
                continue
            lines = cell.source.splitlines()
            qid_line = next((line for line in lines if "문제 ID:" in line), "")
            qid = qid_line.split("문제 ID:")[1].strip()
            self.existing_id_map[qid] = True
            self.existing_fmt_map[qid] = (len(lines), sum(len(l) for l in lines))

    def _is_format_changed(self, qid: str, new_md: str):
        if qid not in self.existing_fmt_map:
            return False
        new_lines = new_md.splitlines()
        new_fmt = (len(new_lines), sum(len(l) for l in new_lines))
        return self.existing_fmt_map[qid] != new_fmt

    def _detect_format_changes(self):
        for row in self.df.itertuples(index=False):
            md = (
                f"## ❓ 문제 ID: {row.id}\n"
                f"**Dataset:** {row.dataset}  \n"
                f"**Difficulty:** {row.difficulty} | **Category:** {row.category}\n\n"
                f"**Q.** {row.question}"
            )
            if row.id not in self.existing_id_map:
                self.a_group.append(row)
            elif self._is_format_changed(row.id, md):
                self.b_group.append(row)

        if self.b_group:
            last_b = self.b_group[-1]
            self.a_group.insert(0, last_b)
            self.b_group = self.b_group[:-1]

    def _group_by_dataset(self, rows):
        buckets = defaultdict(list)
        for r in rows:
            buckets[r.dataset].append(r)
        return buckets

    def _build_sequence(self):
        a_buckets = self._group_by_dataset(self.a_group)
        b_buckets = self._group_by_dataset(self.b_group)
        sequence = self._sequence = sequence  # ← 이제 self._sequence에 저장

        for i, (ds, rows) in enumerate(a_buckets.items()):
            if i == 0 and rows and rows[0].id == self.a_group[0].id:
                self.sequence.append(("dataset", ds))
                self.sequence.append(rows[0])
                rows = rows[1:]
            if rows:
                self.sequence.append(("dataset", ds))
                self.sequence.extend(rows)

        if b_buckets:
            self.sequence.append(("div", "구조가 변경된 기존 문제들"))
            for ds, rows in b_buckets.items():
                self.sequence.append(("dataset", ds))
                self.sequence.extend(rows)

    def _generate_notebooks(self):
        self._chunks = [self._sequence[i:i + self.max_problem] for i in range(0, len(self._sequence), self.max_problem)]
        for idx, chunk in enumerate(self._chunks, start=1):

            for idx, chunk in enumerate(self.chunks, start=1):
                nb = new_notebook()
                nb.cells.append(new_markdown_cell(f"# 📘 {self.tool_name.upper()} 학습 노트북 - EffiStudy\n총 {len(chunk)}문제"))

                import_inserted = False
                q_count = 0

                for item in chunk:
                    if isinstance(item, tuple) and item[0] == "dataset":
                        nb.cells.append(new_markdown_cell(f"### 🔹 Dataset: `{item[1]}`"))
                    elif isinstance(item, tuple) and item[0] == "div":
                        nb.cells.append(new_markdown_cell("## 🔻 구조가 변경된 이전 문제들"))
                    else:
                        row = item
                        md = (
                            f"## ❓ 문제 ID: {row.id}\n"
                            f"**Dataset:** {row.dataset}  \n"
                            f"**Difficulty:** {row.difficulty} | **Category:** {row.category}\n\n"
                            f"**Q.** {row.question}"
                        )
                        nb.cells.append(new_markdown_cell(md))
                        nb.cells.append(new_code_cell(
                            f'dataset = sns.load_dataset("{row.dataset}")\n'
                            f"dataset.head(3)"
                        ))
                        nb.cells.append(new_code_cell("dataset.info()"))
                        q_count += 1
                        if q_count == 10 and not import_inserted:
                            nb.cells.insert(1, new_code_cell(
                                "import pandas as pd\nimport seaborn as sns\nimport matplotlib.pyplot as plt"
                            ))
                            import_inserted = True

                if not import_inserted:
                    nb.cells.insert(1, new_code_cell(
                        "import pandas as pd\nimport seaborn as sns\nimport matplotlib.pyplot as plt"
                    ))

                suffix = f"_{idx}" if idx > 1 else ""
                filename = f"{self.tool_name}{suffix}.ipynb"
                out_path = os.path.join(NOTEBOOK_DIR, filename)
                with open(out_path, "w", encoding="utf-8") as f:
                    nbformat.write(nb, f)

                print(f"✅ [{self.tool_name}] {filename} 저장 완료 ({q_count}문제)")

    def run(self):
        self._parse_existing()
        self._detect_format_changes()
        self._build_sequence()
        self._generate_notebooks()

# ✅ 읽기 전용 property들
    @property
    def a_group(self):
        return self._a_group

    @property
    def sequence(self):
        return self._sequence

    @property
    def chunks(self):
        return self._chunks