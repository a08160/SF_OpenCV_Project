# 퍼스널 컬러 분류
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import KFold, train_test_split

data = pd.read_excel("lab_colors.xlsx")
df = data.drop(columns = ["image_id","skin_bgr"])

# face_Lab 값을 설명변수 / cloth_Lab 값을 종속 변수로 설정
x = data[['face_L_lab','face_a_lab','face_b_lab']]
y = data[['cloth_L_lab','cloth_a_lab','cloth_b_lab']]

