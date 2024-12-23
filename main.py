import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# 데이터 로드
consumption_data = pd.read_csv("소비2006.csv", encoding="euc-kr")
merged_gender_total = pd.read_csv("merge.csv", encoding="euc-kr")

# 2020년도만 필터링, 소비데이터 연도가 바뀐다면 바꿔주면된다
merged_gender_total = merged_gender_total[merged_gender_total['Year'] == 2020]

# 소비 데이터 전처리
consumption_data = consumption_data.rename(columns={
    '시군구명': 'Region', 
    '성별': 'Gender', 
    '연령별': 'AgeGroup', 
    '직업구분': 'JobType',
    '분위구분': 'IncomeGroup', 
    '최근12개월평균신용및체크카드이용금액합계': 'AvgTotalCardUsage',
    '최근12개월신용및체크카드이용금액합계': 'TotalCardUsage',
    '최근12개월전체체크카드이용금액합계': 'TotalCheckCardUsage',
    '최근12개월해외이용금액합계': 'OverseasUsage'
})

# 공백 제거 및 필요한 데이터만 유지
consumption_data['Region'] = consumption_data['Region'].str.strip()
consumption_data = consumption_data[[
    'Region', 'Gender', 'AgeGroup', 'JobType', 'IncomeGroup',
    'TotalCardUsage', 'AvgTotalCardUsage', 'TotalCheckCardUsage', 'OverseasUsage'
]]

# 공백 제거 및 Region 컬럼 정리
merged_gender_total['Region'] = merged_gender_total['Region'].str.strip()

#  분석 준비: 병합
# 병합: Region 기준으로 합치고, 필요한 경우 연도 및 소비 데이터를 추가로 조정
analysis_data = pd.merge(
    merged_gender_total, 
    consumption_data, 
    on="Region", 
    how="inner"
)

print(analysis_data.head())

#  인구 밀도와 소비의 상관관계 분석
# 지역별 Population과 TotalCardUsage를 사용
population_vs_consumption = analysis_data.groupby('Region')[['Population', 'TotalCardUsage']].mean()
correlation = population_vs_consumption.corr().loc['Population', 'TotalCardUsage']
print(f"인구 밀도와 소비 간 상관계수: {correlation:.2f}")

#  성별에 따른 소비 차이 분석
# Gender 기준으로 소비 금액 평균 계산
gender_consumption = analysis_data.groupby('Gender')[['TotalCardUsage', 'AvgTotalCardUsage']].mean()
print("\n성별 소비 차이 분석:")
print(gender_consumption)

# **연령대와 소비 경향 분석**
# AgeGroup 기준으로 소비 금액 평균 계산
agegroup_consumption = analysis_data.groupby('AgeGroup')[['TotalCardUsage', 'AvgTotalCardUsage']].mean()
print("\n연령대 소비 경향 분석:")
print(agegroup_consumption)

# HTML 저장 디렉토리 설정
output_html = "analysis_results.html"

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False    # 마이너스 기호 깨짐 방지

# 플롯 저장 경로 설정
plots = []

# 인구 밀도와 소비의 상관관계
plt.figure(figsize=(10, 6))
sns.scatterplot(data=population_vs_consumption, x="Population", y="TotalCardUsage")
plt.title("Population vs Total Card Usage")
plt.xlabel("Population")
plt.ylabel("Total Card Usage")
plt.savefig("population_vs_consumption.png")
plots.append("population_vs_consumption.png")
plt.close()

# Gender 값에서 0(전체)를 제외
filtered_data = analysis_data[analysis_data['Gender'].isin([1, 2])]

# 성별 소비 차이 분석 및 그래프 생성
gender_consumption_plot = filtered_data.groupby(['Region', 'Gender'])['TotalCardUsage'].mean().unstack()
gender_consumption_plot.plot(kind='bar', figsize=(12, 8))
plt.title("Gender-wise Consumption Difference by Region")
plt.xlabel("Region")
plt.ylabel("Average Total Card Usage")
plt.legend(["Male", "Female"])
plt.savefig("gender_consumption.png")
plots.append("gender_consumption.png")
plt.close()

# 지역별 연령대와 소비 경향 분석
agegroup_consumption_plot = analysis_data.groupby(['Region', 'AgeGroup'])['TotalCardUsage'].mean().unstack()
agegroup_consumption_plot.plot(kind='bar', figsize=(14, 8), stacked=True)
plt.title("Age Group-wise Consumption by Region")
plt.xlabel("Region")
plt.ylabel("Average Total Card Usage")
plt.legend(title="Age Group")
plt.savefig("agegroup_consumption.png")
plots.append("agegroup_consumption.png")
plt.close()

# KMeans 군집화 시각화
data_for_clustering = analysis_data[['Population', 'TotalCardUsage', 'AvgTotalCardUsage', 'OverseasUsage']].dropna()
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_for_clustering)

kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(data_pca)

plt.figure(figsize=(10, 6))
plt.scatter(data_pca[:, 0], data_pca[:, 1], c=clusters, cmap='viridis', alpha=0.7)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='red', marker='X', s=200, label='Centroids')
plt.title("KMeans Clustering Visualization")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend()
plt.savefig("kmeans_clustering.png")
plots.append("kmeans_clustering.png")
plt.close()

# 상관관계 히트맵
plt.figure(figsize=(10, 6))
correlation_matrix = analysis_data[['Population', 'TotalCardUsage', 'AvgTotalCardUsage', 'OverseasUsage']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.savefig("correlation_heatmap.png")
plots.append("correlation_heatmap.png")
plt.close()



html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analysis Results</title>
</head>
<body>
    <h1>Analysis Results</h1>
    <h2>Plots</h2>
"""

for plot in plots:
    plot_title = plot.split('.')[0].replace('_', ' ').title()
    html_content += f"""
    <div>
        <h3>{plot_title}</h3>
        <img src="{plot}" alt="{plot}" style="max-width:100%;height:auto;">
    </div>
    """

html_content += """
</body>
</html>
"""

# HTML 저장
output_html = "analysis_results.html"
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Analysis results saved to {output_html}")