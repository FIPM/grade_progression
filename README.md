# A voting classifier for student grade progression.

## Problem
High attrition of third-grade students in Guatemala.

## Solution
Training a model to predict the probability that a student attends higher grades, conditional on their third-grade performance at school. The identification of students at risk will allow targeting programs by the Ministry of Education.

## Technical details
- By using data engineering, I integrate into a pipeline custom classes such as a standard scaler, pca, and a voting classifier model to predict the probability of grade progression.

- By using statistics, I disaggregate the influence of third-grade students' performance on grade progression.

- By using cloud platforms, I create a webpage to inform decision-makers.

## Key technologies
Pandas, scikit-learn, Plotly, Flask, HTML, CSS, JS, Heroku.

# Installing requirements
pip install -r requirements.txt

# Running the website
python MainProgram.py

# Training the model
python scripts/model_main_program.py 