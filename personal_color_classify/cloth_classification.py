# 퍼스널 컬러별 어울리는 옷 구분

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

# 데이터 불러오기
df = pd.read_excel("complete_personal_color.xlsx")

# IQR을 사용하여 이상치 제거
def remove_outliers(df):
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    df_no_outliers = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
    return df_no_outliers

# X는 예측할 데이터 (cloth_L_lab, cloth_a_lab, cloth_b_lab)
X = df[['cloth_L_lab', 'cloth_a_lab', 'cloth_b_lab']]

# 이상치 제거
X_no_outliers = remove_outliers(X)

# y는 타겟 (Personal_Color)
y = df['Personal_Color']

# 이상치 제거된 X에 해당하는 y 값도 필터링
y_no_outliers = y[X_no_outliers.index]

# KFold 설정 (5 폴드)
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# 정확도를 저장할 리스트
accuracies = []
last_node_predictions = []

# KFold 교차 검증 수행
for train_index, test_index in kf.split(X_no_outliers):
    X_train, X_test = X_no_outliers.iloc[train_index], X_no_outliers.iloc[test_index]
    y_train, y_test = y_no_outliers.iloc[train_index], y_no_outliers.iloc[test_index]
    
    # Decision Tree 모델 정의 (depth 2로 설정)
    dt_model = DecisionTreeClassifier(random_state=42, max_depth=2)
    
    # 모델 학습
    dt_model.fit(X_train, y_train)
    
    # 예측
    y_pred = dt_model.predict(X_test)
    
    # 정확도 계산
    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)
    
    # 마지막 노드에서 정확하게 예측된 데이터 추출
    for i, (true_label, pred_label) in enumerate(zip(y_test, y_pred)):
        if true_label == pred_label:  # 정확하게 맞춘 예측
            # 해당 데이터의 personal_color 값을 추출
            last_node_predictions.append({
                "index": test_index[i],  # 수정된 부분
                "actual": true_label,     # 실제 값
                "predicted": pred_label   # 예측 값
            })


# 평균 정확도 계산
average_accuracy = np.mean(accuracies)

# 결과 출력
print(f"각 폴드의 정확도: {accuracies}")
print(f"전체 평균 정확도: {average_accuracy}")

# 마지막 폴드에 대해 의사결정트리 시각화
plt.figure(figsize=(12, 8))
plot_tree(dt_model, feature_names=X_no_outliers.columns, filled=True)
plt.title("Decision Tree for Personal Color Prediction")
plt.show()

# 마지막 노드에서 정확히 예측된 데이터의 personal_color
print("정확하게 맞춘 데이터의 Personal Color:")
for prediction in last_node_predictions:
    print(f"Index: {prediction['index']}, Actual: {prediction['actual']}, Predicted: {prediction['predicted']}")

# 이상치 제거 후 각 피쳐에 대한 시각화 (히스토그램)
plt.figure(figsize=(12, 6))
X_no_outliers.hist(bins=20, edgecolor='k', alpha=0.7)
plt.suptitle("Feature Distributions After Outlier Removal")
plt.show()
