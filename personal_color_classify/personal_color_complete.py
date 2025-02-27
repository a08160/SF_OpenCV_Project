# 퍼스널 컬러 구분 기입
# 구분 기준

'''
1. face_b_lab 
141.5 이상: Warm
141.5 미만: Cool

2. face_L_lab
* Warm 의 경우
150.5 이상: Spring Warm
150.5 미만: Autumn Warm

* Cool 의 경우
138.5 이상: Summer Cool
138.5 미만: Winter Cool

'''

import pandas as pd

# 데이터 불러오기
df = pd.read_excel("lab_colors.xlsx")
df = df.drop(columns=["image_id", "skin_bgr"]).astype(int)

# 퍼스널 컬러 구분
for index, img in df.iterrows():
    if img["face_b_lab"] >= 141.5:  # Warm
        if img["face_L_lab"] >= 150.5:
            df.at[index, "Personal_Color"] = "Spring Warm"
        else:
            df.at[index, "Personal_Color"] = "Autumn Warm"
    else:  # Cool
        if img["face_L_lab"] >= 138.5:
            df.at[index, "Personal_Color"] = "Summer Cool"
        else:
            df.at[index, "Personal_Color"] = "Winter Cool"

# 결과를 엑셀 파일로 저장
df.to_excel("complete_personal_color.xlsx", index=False)
