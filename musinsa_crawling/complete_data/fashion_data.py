import pandas as pd
import glob

file_list = glob.glob("./musinsa_crawling/complete_data/*.xlsx")

df_list = [pd.read_excel(file) for file in file_list]
print(df_list)

df_merged = pd.concat(df_list, ignore_index=True)  # index 초기화

# 4. 통합된 파일 저장
df_merged.to_excel("fashion_data.xlsx", index=False)