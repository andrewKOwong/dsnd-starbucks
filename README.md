# Will It Complete? Predicting Starbucks Offer Completion Rates
## Project Summary

Starbucks is a well-known coffee company operating ~32,000 stores with net revenues of 23B USD as of 2020. Starbucks customers can choose to participate in the Starbucks Rewards programs, allowing them to earn discounts on purchases as well as receive special offers from time to time. Knowing how customers react to specific offers could be valuable information, as sending the right offer to the right customer at the right time could favorably influence how much customers spend.

As part of the Udacity Data Scientist Nanodegree, a simulated dataset of 17000 rewards program customers was provided. This dataset contains customer transactions over a period of around one month, including when these customers received, viewed, and completed reward offers.

I performed basic data cleaning, exploratory data analysis, and built models to predict customer response to reward offers in three separate Jupyter notebooks. A full description is available as a blogpost [here](https://mixedconclusions.com/blog/dsnd_starbucks/).


## Instructions
### Description of Files

- `blog_post` contains figures used for the blog post.
- `notebook-basic_data_cleaning.ipynb` describes the steps I took to do some basic data cleaning. I then incorporated those processes into `pipeline-clean_data.py`, which in turn imports cleaning functions from `tools.py`.
- `notebook-EDA.ipynb` contains exploratory data analysis.
- `notebook-model_development` describe the building of machine learning models to predict customer response to offers.
- `data` contains both the raw data set and the cleaned data.
- `models` contains pickle objects saved and loaded to `notebook-model_development.ipynb`
- `archive` contains the original provided Udacity notebook.

### Libraries Required
`numpy`
`matplotlib`
`pandas`
`seaborn`
`sklearn`
`jupyter`


### Running The Notebooks
- While `notebook-basic_data_cleaning.ipynb` describes the data cleaning process, run `python pipeline-clean_data.py` in the root directory to actually generate the cleaned csvs.
- The EDA and model building notebooks should run as normal for a Jupyter notebook. Note the model building notebook has a pickle load and save step in the middle one could run parts of the notebook without retraining the models.