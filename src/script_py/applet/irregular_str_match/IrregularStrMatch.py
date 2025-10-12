import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from tqdm import tqdm

from script_py.util.GenUtil import GenUtil


class IrregularStrMatch:

    def __init__(self):
        self.foodCookbookPath = GenUtil.getValue("food-cookbook-path")
        self.foodDetailsPath = GenUtil.getValue("food-details-path")
        self.outPath = GenUtil.getValue("output-path")

    def apply(self):
        df_cookbook = pd.read_csv(self.foodCookbookPath, dtype=str)  # 防止数值被误转为 float
        df_details = pd.read_csv(self.foodDetailsPath, dtype=str)

        # ---------- 2. 构建匹配字典 ----------
        # 如果同名出现多条，保留最大的 ID（假设 ID 为字符串但能按数字比较）
        details_dict = {}
        for _, row in df_details.iterrows():
            name = row['food_details_name'].strip()
            did = int(row['food_details_id'])
            if name not in details_dict or did > details_dict[name]:
                details_dict[name] = did

        # ---------- 3. 准备候选列表 ----------
        candidate_names = list(details_dict.keys())

        new_rows = []
        for _, row in tqdm(df_cookbook.iterrows(), total=len(df_cookbook)):
            cook_name = row['food_cookbook_name'].strip()

            # ① 尝试完全匹配
            if cook_name in details_dict:
                best_name = cook_name
            else:
                # ② 模糊匹配
                best_name = self.find_best_match(cook_name, candidate_names)

            if best_name is None:
                # 未匹配到任何记录
                did = 0
                dname = '无'
            else:
                did = details_dict[best_name]
                dname = best_name

            new_row = row.copy()
            new_row['food_details_id'] = str(did)
            new_row['food_details_name'] = dname
            new_rows.append(new_row)

        df_new = pd.DataFrame(new_rows)

        # ---------- 6. 写入新文件 ----------
        df_new.to_csv(self.outPath, index=False, encoding='utf-8-sig')

        print(f"已生成 {self.outPath}，共 {len(df_new)} 行。")

    def find_best_match(self, name, candidate_names, threshold=60):
        """
        用 fuzzywuzzy 的 process.extractOne 做模糊匹配。
        返回 (best_name, score) 或 (None, 0)
        """
        # best_name, score = process.extractOne(name, candidate_names, scorer=fuzz.WRatio)
        best_names = process.extractBests(name, candidate_names, limit=5, score_cutoff=30, scorer=fuzz.token_sort_ratio)
        if len(best_names) == 0:
            return None
        else:
            return best_names[0][0]

    # def custom_scorer(self, s1, s2):
    #     return fuzz.token_sort_ratio(s1, s2)

    @staticmethod
    def run():
        irregularStrMatch = IrregularStrMatch()
        irregularStrMatch.apply()
