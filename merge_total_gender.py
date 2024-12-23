import pandas as pd

# gender.csv와 total.csv 파일을 로드
gender_data = pd.read_csv("gender.csv", encoding="euc-kr")
total_population_data = pd.read_csv("total.csv", encoding="euc-kr")

# gender.csv 데이터를 long format으로 변환
gender_long = pd.melt(
    gender_data, 
    id_vars=["행정구역(자치구)별(1)"],  # '행정구역(자치구)별(1)' 열을 고정
    var_name="Category_Year",  # 새로운 변수 이름
    value_name="Value"  # 값이 들어갈 열 이름
)

# "Category_Year"에서 "Category" (남, 여, 성비)와 "Year"를 추출
gender_long["Category"] = gender_long["Category_Year"].str.split("_").str[0]  # "남", "여", "성비" 추출
gender_long["Year"] = gender_long["Category_Year"].str.split("_").str[1].astype(int)  # 연도 추출

# gender_long 데이터를 피벗하여 "MalePopulation", "FemalePopulation", "GenderRatio" 컬럼 생성
gender_pivot = gender_long.pivot_table(
    index=["행정구역(자치구)별(1)", "Year"],  # '행정구역(자치구)별(1)'과 'Year'를 인덱스로 설정
    columns="Category",  # 'Category' 기준으로 컬럼 생성
    values="Value"  # "Value" 컬럼을 값으로 사용
).reset_index()

# 컬럼 이름을 일관성 있게 변경
gender_pivot = gender_pivot.rename(columns={
    "행정구역(자치구)별(1)": "Region",  # '행정구역(자치구)별(1)'을 'Region'으로 변경
    "남": "MalePopulation",  # '남'을 'MalePopulation'으로 변경
    "여": "FemalePopulation",  # '여'를 'FemalePopulation'으로 변경
    "성비": "GenderRatio"  # '성비'를 'GenderRatio'로 변경
})

# total.csv 데이터를 long format으로 변환
total_long = pd.melt(
    total_population_data, 
    id_vars=["Unnamed: 0", "Unnamed: 1"],  # 'Unnamed: 0', 'Unnamed: 1' 열을 고정
    var_name="Region",  # 새로운 변수 이름
    value_name="Population"  # 값이 들어갈 열 이름
)

# 인구 데이터만 필터링
total_population = total_long[total_long["Unnamed: 1"] == "인구 (명)"]
total_population = total_population.rename(columns={"Unnamed: 0": "Year"})  # 'Unnamed: 0'을 'Year'로 변경
total_population = total_population[["Year", "Region", "Population"]]  # 필요한 열만 선택
total_population["Year"] = total_population["Year"].astype(int)  # 'Year'를 정수형으로 변환

# 성별 데이터와 인구 데이터를 병합
merged_data = pd.merge(gender_pivot, total_population, on=["Region", "Year"], how="inner")

# 데이터 정리 및 정렬
final_data = merged_data[["Region", "Year", "Population", "MalePopulation", "FemalePopulation", "GenderRatio"]]  # 필요한 열만 선택
final_data = final_data.sort_values(by=["Region", "Year"]).reset_index(drop=True)  # 'Region'과 'Year' 기준으로 정렬

print(final_data.head())  # 결과 출력

# CSV 파일로 저장
final_data.to_csv("merge.csv", index=False, encoding="euc-kr")
