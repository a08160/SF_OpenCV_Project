import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

# 데이터 불러오기
data = pd.read_excel("lab_colors.xlsx")
df = data.drop(columns=["image_id", "skin_bgr"])

# 이상치 제거 (IQR 방법)
def remove_outliers(df):
    for col in df.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df

df = remove_outliers(df)

# face_Lab 값을 설명변수 / cloth_Lab 값을 종속 변수로 설정
X = df[['face_L_lab', 'face_a_lab', 'face_b_lab']] 
y = df[['cloth_L_lab', 'cloth_a_lab', 'cloth_b_lab']]

# KFold 교차 검증의 분할 수를 변경하여 최적의 n_splits 찾기
kf_splits_range = range(2, 11)  # n_splits를 2부터 10까지 시도
best_n_splits = None
best_accuracy = float('-inf')
best_accuracies = {}

# KFold 교차 검증
for n_splits in kf_splits_range:
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    # 각 폴드의 정확도를 저장할 리스트
    accuracies = {col: [] for col in y.columns}
    
    # KFold 교차 검증 수행
    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
        # 의사결정트리 모델 정의 (depth를 3으로 설정)
        dt_model = DecisionTreeClassifier(random_state=42, max_depth=3)
        
        # 다중 특성을 고려한 커스텀 분할 방법 적용 (특성들의 조합 사용)
        # 각 'cloth_L_lab', 'cloth_a_lab', 'cloth_b_lab'에 대해 모델 학습 및 예측
        for col in y.columns:
            dt_model.fit(X_train, y_train[col])
            y_pred = dt_model.predict(X_test)
            accuracies[col].append(accuracy_score(y_test[col], y_pred))
    
    # 각 열에 대한 평균 정확도 계산
    mean_accuracies = {col: np.mean(accuracies[col]) for col in accuracies}
    
    # 전체 평균 정확도 계산
    average_accuracy = np.mean(list(mean_accuracies.values()))
    
    # 최적의 n_splits 갱신
    if average_accuracy > best_accuracy:
        best_accuracy = average_accuracy
        best_n_splits = n_splits
        best_accuracies = mean_accuracies

# 최적의 n_splits와 해당 정확도 출력
print(f"최적의 n_splits: {best_n_splits}")
print("각 열에 대한 평균 정확도:", best_accuracies)
print("전체 평균 정확도:", best_accuracy)

# 의사결정트리 시각화 (class_names 없이)
plt.figure(figsize=(12, 8))
plot_tree(dt_model, feature_names=X.columns, filled=True)
plt.title("Decision Tree for Cloth Lab Color Prediction")
plt.show()
