# 퍼스널 컬러 군집화
# 얼굴과 옷의 Lab 값을 하나의 순서쌍으로 만들어 군집화를 진행

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering

# 데이터 불러오기
data = pd.read_excel("lab_colors.xlsx")
df = data.drop(columns=["image_id", "skin_bgr"])

# face_Lab과 cloth_Lab 결합
combined_data = df[["face_L_lab", "face_a_lab", "face_b_lab", "cloth_L_lab", "cloth_a_lab", "cloth_b_lab"]].values

# 최적의 linkage 방법 찾기
linkages = ['ward', 'complete', 'average', 'single']
best_linkage = None
best_score = float('inf')

for linkage in linkages:
    clustering = AgglomerativeClustering(n_clusters=4, linkage=linkage, compute_distances=True)
    labels = clustering.fit_predict(combined_data)
    
    # 거리 정보가 없을 경우 대비
    if clustering.distances_ is not None:
        score = sum(clustering.distances_)
        if score < best_score:
            best_score = score
            best_linkage = linkage

# 최적의 linkage로 군집화 수행
agg_clustering = AgglomerativeClustering(n_clusters=4, linkage=best_linkage)
df["cluster"] = agg_clustering.fit_predict(combined_data)

# 결과 확인
print(df.head())

# 각 군집별 데이터 개수 출력
print(df["cluster"].value_counts())

# 시각화
plt.figure(figsize=(8, 6))
sns.scatterplot(x=df["face_L_lab"], y=df["face_a_lab"], hue=df["cluster"], palette='tab10')
plt.xlabel("Face L")
plt.ylabel("Face A")
plt.title("Cluster Visualization (Best Linkage: " + best_linkage + ")")
plt.legend(title="Cluster")
plt.show()