# Rossmann Sales Prediction

## Business Challenge
The company is planning to do some refurbishment in their 1115 stores. However, the magnitude of those refurbishments depends on the sales for the next six weeks. As a data scientist, my challenge was to help the CFO having a sales prediction to make an accurate budget for the store's refurbishment.

## Business Result
Overall, the performance of the model follows below:

![Alt text](/result.png?raw=true)

The solution that I found to give access to the final users to the model was via TelegramBot. The model was deployed on Heroku, and the sales forecast for the next six weeks for each store is available for the user online on Telegram.

## Solution Strategy
The project had a total of eight steps as follow:
1) Description and cleaning data: treating NA, change types, descriptive statistics and data filtering 
2) Feature engineering: creating a hypothesis list, creating new features for further analysis.
3) Exploratory data analysis: guided (but not limited) by the hypothesis list, I did some univariate, bivariate and multivariate data analysis to see what I could learn from the dataset beyond common sense.
4) Data preparation: rescaling numerical data, encoding and I did some data changes using mathematical trigonometrical functions. 
5) Feature selection: to select the most relevant feature, I used the Boruta module.
6) Machine learning modelling: after testing some models, I decided to use XGBoost Regressor as it had a good performance and also I was curious to learn more about it. 
7) From model to business: after I have tuned the model, the result and the error were analysed from the business point of view.  
8) Deploy model: using Heroku, Flask and the TelegramBot, I deployed the model in the clouds to allow stakeholders to access the result.

## Machine Learning models
In this project, I have applied the following machine learning models:
- Linear Regression
- Regularised Linear Regression
- Random Forest Regressor
- XGBoost Regressor

## Conclusions
In a real-world situation, I would be pleased with the result that my model returned. As a CFO, I could make an accurate budget for each store's refurbishment.

## Lessons learned
The EDA provide insight that contradicts the hypothesis list, which was surprising. Some other teams across the company can use this result to plan the next steps in their goals.

## Next steps and improvement
I did this project having in mind the CRISP process. As more people join this project, some results can be improved. For example, more hypotheses can be raised by others who have experience in this business and then tested by me.  Furthermore, as my knowledge in data science expands, I can use other machine learning models and other techniques.
Also, the stakeholder could have access to the best scenario and the worst scenario instead of having only the sales prediction. 
