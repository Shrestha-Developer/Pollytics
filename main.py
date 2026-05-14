import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from wordcloud import WordCloud

# Make results reproducible
np.random.seed(42)

# Sample values
regions = ['North', 'South', 'East', 'West']
age_groups = ['18-25', '26-35', '36-45', '46+']
genders = ['Male', 'Female']
options = ['Product A', 'Product B', 'Product C']
feedbacks = [
    "Very useful and easy to use",
    "Good product and nice experience",
    "Needs improvement",
    "Excellent and highly recommended",
    "Average experience",
    "Very satisfied with the product"
]

# Create synthetic responses
data = []

for i in range(100):
    response = {
        'Respondent_ID': i + 1,
        'Region': np.random.choice(regions),
        'Age_Group': np.random.choice(age_groups),
        'Gender': np.random.choice(genders),
        'Selected_Option': np.random.choice(options, p=[0.5, 0.3, 0.2]),
        'Satisfaction': np.random.randint(1, 6),
        'Feedback': np.random.choice(feedbacks)
    }
    data.append(response)

# Convert into DataFrame
df = pd.DataFrame(data)
# Convert into DataFrame
df = pd.DataFrame(data)

# Save raw data
df.to_csv('data/raw_poll_data.csv', index=False)

# -------------------------
# Data Cleaning
# -------------------------

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows with missing values
df = df.dropna()

# Standardize text columns
df['Region'] = df['Region'].str.strip().str.title()
df['Gender'] = df['Gender'].str.strip().str.title()
df['Selected_Option'] = df['Selected_Option'].str.strip()

# Save cleaned data
df.to_csv('data/cleaned_poll_data.csv', index=False)

print("Raw dataset shape:", pd.read_csv('data/raw_poll_data.csv').shape)
print("Cleaned dataset shape:", df.shape)

print("\nFirst 5 cleaned rows:")
print(df.head())
# -------------------------
# Poll Analysis
# -------------------------

vote_summary = df['Selected_Option'].value_counts().reset_index()
vote_summary.columns = ['Option', 'Votes']

vote_summary['Percentage'] = (
    vote_summary['Votes'] / vote_summary['Votes'].sum() * 100
).round(2)

print("\nVote Summary:")
print(vote_summary)

# Save summary
vote_summary.to_csv('outputs/vote_summary.csv', index=False)
# -------------------------
# Bar Chart Visualization
# -------------------------

sns.set_style("whitegrid")

plt.figure(figsize=(8, 5))
sns.barplot(data=vote_summary, x='Option', y='Votes')

plt.title('Poll Results by Option')
plt.xlabel('Selected Option')
plt.ylabel('Number of Votes')

plt.tight_layout()

# Save chart
plt.savefig('outputs/bar_chart.png')

# Show chart
plt.show()
# -------------------------
# Pie Chart Visualization
# -------------------------

plt.figure(figsize=(6, 6))

plt.pie(
    vote_summary['Votes'],
    labels=vote_summary['Option'],
    autopct='%1.1f%%'
)

plt.title('Vote Share Percentage')

plt.savefig('outputs/pie_chart.png')
plt.show()
# -------------------------
# Region-wise Analysis
# -------------------------

region_summary = pd.crosstab(df['Region'], df['Selected_Option'])

print("\nRegion-wise Summary:")
print(region_summary)

# Stacked Bar Chart
region_summary.plot(kind='bar', stacked=True, figsize=(8, 5))

plt.title('Region-wise Product Preference')
plt.xlabel('Region')
plt.ylabel('Number of Votes')
plt.legend(title='Product')

plt.tight_layout()

plt.savefig('outputs/region_chart.png')
plt.show()
# -------------------------
# Age Group Analysis
# -------------------------

age_summary = pd.crosstab(df['Age_Group'], df['Selected_Option'])

print("\nAge Group Summary:")
print(age_summary)

age_summary.plot(kind='bar', figsize=(8, 5))

plt.title('Product Preference by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Number of Votes')
plt.legend(title='Product')

plt.tight_layout()

plt.savefig('outputs/age_group_chart.png')
plt.show()
# -------------------------
# Satisfaction Distribution
# -------------------------

plt.figure(figsize=(8, 5))

sns.countplot(data=df, x='Satisfaction')

plt.title('Satisfaction Rating Distribution')
plt.xlabel('Satisfaction Rating')
plt.ylabel('Number of Respondents')

plt.tight_layout()

plt.savefig('outputs/satisfaction_chart.png')
plt.show()
# -------------------------
# Feedback Word Cloud
# -------------------------

text = " ".join(df['Feedback'])

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white'
).generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Common Words in Feedback')

plt.tight_layout()
plt.savefig('outputs/wordcloud.png')
plt.show()
# -------------------------
# Automatic Insights
# -------------------------

top_option = vote_summary.iloc[0]['Option']
top_percentage = vote_summary.iloc[0]['Percentage']

least_option = vote_summary.iloc[-1]['Option']
least_percentage = vote_summary.iloc[-1]['Percentage']

avg_satisfaction = round(df['Satisfaction'].mean(), 2)

print("\n--- Insights ---")
print(f"The most preferred product is {top_option} with {top_percentage}% of votes.")
print(f"The least preferred product is {least_option} with {least_percentage}% of votes.")
print(f"The average satisfaction rating is {avg_satisfaction} out of 5.")

highest_region = region_summary[top_option].idxmax()
print(f"{top_option} is most popular in the {highest_region} region.")