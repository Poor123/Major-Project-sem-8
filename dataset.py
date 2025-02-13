import pandas as pd
import random

# Possible values for placeholders in NLP queries
semesters = [1, 2, 3, 4, 5, 6, 7, 8]
years = list(range(2015, 2025))
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
levels = ["School", "District", "State", "National", "International"]

# NLP query templates (without specifying visualization type)
nlp_queries_templates_vague = [
    "How well did students perform in semester {sem}?",
    "Show me details of CGPA in semester {sem}.",
    "What are the extracurricular participation levels among students?",
    "Can you tell me about the students' SSC scores in {year}?",
    "I need information about students' HSC performance.",
    "How many students passed CET this year?",
    "Give me an overview of diploma results.",
    "What's the distribution of students' results for {month}, {year}?",
    "How many students participated at the {level} level?",
    "Tell me about students’ academic performance.",
    "What’s the trend in CGPA scores?",
    "How did students perform in semester {sem}?",
]

# Corresponding SQL query templates
sql_query_templates_vague = [
    "SELECT cgpa, COUNT(*) FROM students WHERE semester = {sem} GROUP BY cgpa;",
    "SELECT cgpa, COUNT(*) FROM students WHERE semester = {sem} GROUP BY cgpa;",
    "SELECT extracurricular_level, COUNT(*) FROM students GROUP BY extracurricular_level;",
    "SELECT ssc_score, COUNT(*) FROM students WHERE year = {year} GROUP BY ssc_score;",
    "SELECT hsc_score, COUNT(*) FROM students GROUP BY hsc_score;",
    "SELECT COUNT(*) FROM students WHERE cet_pass = 1;",
    "SELECT diploma_result, COUNT(*) FROM students GROUP BY diploma_result;",
    "SELECT semester, COUNT(*) FROM students WHERE month = '{month}' AND year = {year} GROUP BY semester;",
    "SELECT extracurricular_level, COUNT(*) FROM students WHERE extracurricular_level = '{level}';",
    "SELECT cgpa, hsc_score, cet_score FROM students;",
    "SELECT cgpa, COUNT(*) FROM students GROUP BY cgpa ORDER BY cgpa;",
    "SELECT semester, AVG(cgpa) FROM students GROUP BY semester;",
]

# Determine recommended visualization type
def get_visualization_type(sql_query):
    if "COUNT(*)" in sql_query and "GROUP BY" in sql_query:
        return "Bar Chart"
    elif "AVG(" in sql_query or "SUM(" in sql_query:
        return "Bar Chart"
    elif "GROUP BY extracurricular_level" in sql_query or "GROUP BY diploma_result" in sql_query:
        return "Pie Chart"
    elif "pass" in sql_query.lower() or "fail" in sql_query.lower():
        return "Pie Chart"
    else:
        return "Bar Chart"

# Generate dataset
data_vague = []
for _ in range(10000):
    template_index = random.randint(0, len(nlp_queries_templates_vague) - 1)
    sem = random.choice(semesters)
    level = random.choice(levels)
    year = random.choice(years)
    month = random.choice(months)

    nlp_query = nlp_queries_templates_vague[template_index].format(sem=sem, level=level, year=year, month=month)
    sql_query = sql_query_templates_vague[template_index].format(sem=sem, level=level, year=year, month=month)
    visualization_type = get_visualization_type(sql_query)

    data_vague.append([nlp_query, sql_query, visualization_type])

# Create DataFrame and save as Excel
nlp_sql_df_vague = pd.DataFrame(data_vague, columns=["NLP Query", "SQL Query", "Recommended Visualization"])
nlp_sql_df_vague.to_excel("nlp_sql_dataset_vague.xlsx", index=False)

print("Dataset generated successfully and saved as 'nlp_sql_dataset_vague.xlsx'.")
