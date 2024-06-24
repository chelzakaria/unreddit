## <img src="https://github.com/chelzakaria/unreddit/blob/main/images/Logo.png" alt="drawing" style="width:250px;"/>



## Table of Contents
- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Data Collection](#data-collection)
- [Data Cleaning & Exploratory Data Analysis (EDA)](#data-cleaning-and-eda)
- [Topic Modeling](#topic-modeling)
- [Zero-Shot Classification](#zero-shot-classification)
- [Sentiment Analysis](#sentiment-and-emotion-analysis)
- [Visualization](#visualization)
- [Conclusion](#conclusion)
- [References & Resources](#references-and-resources)


## Introduction

Unreddit is a comprehensive project aimed at analyzing and visualizing discussions from a specific subreddit ([r/morocco](https://www.reddit.com/r/morocco/)). The project includes data collection, cleaning, exploratory data analysis (EDA), topic modeling, [zero-shot classification](https://huggingface.co/tasks/zero-shot-classification), sentiment analysis, and emotion analysis. The final results are visualized through interactive dashboards and detailed plots, providing deep insights into the trends and sentiments of the subreddit community.

## Project Overview

The project is divided into several stages, each focusing on a specific aspect of the data analysis process. 

The project starts with data collection, where we scrape posts and comments from the [r/morocco](https://www.reddit.com/r/morocco/) subreddit. 

The collected data is then cleaned and preprocessed to remove irrelevant information and prepare it for analysis. The next step is exploratory data analysis (EDA). 

We then move on to topic modeling, where we use unsupervised learning techniques to identify the main topics discussed in the subreddit. 

Next, we perform [zero-shot classification](https://huggingface.co/tasks/zero-shot-classification) to classify posts based on predefined categories. We also conduct sentiment analysis to determine the sentiment of posts and comments. 

Finally, we analyze the emotions expressed in the posts and comments. The results of the analysis are visualized through interactive dashboards and detailed plots, providing a comprehensive overview of the subreddit community.

## Project Structure
![Project Structure Diagram](https://github.com/chelzakaria/unreddit/assets/80723047/1dd2a8fe-35d2-4157-970a-ee184ee47cf1)

## Data Collection

There is two main ways to collect data from Reddit: 
1. Downloading zst files from [Pushshift archives](https://the-eye.eu/redarcs/), and then extracting the data using the script `scripts/read_zst.py` (The script was taken from [PushshiftDumps](https://github.com/Watchful1/PushshiftDumps)).

2. The best way is to use the [PullPush Reddit API](https://pullpush.io/#docs). It's a free API that allows you to get data from Reddit in a very easy way. 

    N.B: You have a limit of 100 posts/comments per request.

3. Automating the data collection process using Airflow and AWS S3 bucket (Optional) :
TBA


## Data Cleaning and EDA

Data cleaning involves removing irrelevant information, handling missing values, removing duplicates, to prepare the data for analysis. EDA involves analyzing the data to identify trends, patterns, and insights.

## Topic Modeling

Topic modeling is an unsupervised learning technique that identifies the main topics discussed in a collection of text documents. 

We used [BERTopic](https://maartengr.github.io/BERTopic/api/bertopic.html), a topic modeling library that leverages BERT embeddings to identify topics in text data.

The process involves the following steps:

1. Preprocessing the text data by removing stopwords.
2. Pre-calculating BERT embeddings for the text data.
3. Applying BERTopic to identify topics in the text data.
4. Fine-tuning the topics using LLM & Generative AI to improve the quality of the topics. We used [Llama 2](https://github.com/abetlen/llama-cpp-python) for this purpose.

## Zero-Shot Classification

[Zero-shot text classification](https://huggingface.co/tasks/zero-shot-classification) is a task in natural language processing where a model is trained on a set of labeled examples but is then able to classify new examples from previously unseen classes.

We used the [🤗 Hugging Face Transformers library](https://huggingface.co/transformers/) to perform [zero-shot classification](https://huggingface.co/tasks/zero-shot-classification) on the topics resulting from the topic modeling process.

The process involves the following steps:

1. Defining a list of categories to classify the topics into.
2. Using the [zero-shot classification](https://huggingface.co/tasks/zero-shot-classification) model to classify the topics into the predefined categories.

## Sentiment and Emotion Analysis

Sentiment analysis is the process of determining the sentiment of a text document, such as positive, negative, or neutral. Emotion analysis is the process of determining the emotions expressed in a text document, such as happy, sad, angry...

We used [Twitter-roBERTa-base model](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest) and [🤗 Hugging Face Transformers library](https://huggingface.co/transformers/) to perform sentiment analysis and emotion analysis on the posts and comments from the [r/morocco](https://www.reddit.com/r/morocco/) subreddit.

But to gain a better understanding of the emotions expressed by the users, we used [DistilRoBERTa-base model](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) and [🤗 Hugging Face Transformers library](https://huggingface.co/transformers/) to perform a deeper analysis of the emotions.

## Visualization

The results of the analysis are visualized through interactive dashboards, providing deep insights into the trends and sentiments of the subreddit community.

### Visualization 1 : Topic Modeling, Categories, and Word Clouds
<img src="https://github.com/chelzakaria/unreddit/blob/main/images/viz_page1.png" alt="Visualization #1"/>

> The first visualization shows the trending topics in the subreddit, the most common categories, and the word that were used the most in the posts and comments.

*More visualizations TBA*

*Power BI files and links to the dashboards will be provided later.*

## Conclusion

The project provides a comprehensive analysis of the [r/morocco](https://www.reddit.com/r/morocco/) subreddit, including data collection, cleaning, exploratory data analysis (EDA), topic modeling, zero-shot classification, sentiment analysis, and emotion analysis. The results are visualized through interactive dashboards and detailed plots, providing deep insights into the trends and sentiments of the subreddit community.

## Technologies Used

- [Python](https://www.python.org/) - The main programming language used in the project.
- [Jupyter Notebook](https://jupyter.org/) - The interactive development environment used for data analysis.
- [BERTopic](https://maartengr.github.io/BERTopic/index.html) - The topic modeling library used in the project.
- [🤗 Hugging Face Transformers library](https://huggingface.co/transformers/) - The library used for zero-shot classification, sentiment analysis, and emotion analysis.
- [llama.cpp](https://github.com/abetlen/llama-cpp-python) - The library used for fine-tuning topics in BERTopic.
- [cuML](https://github.com/rapidsai/cuml) - The library used to speed up the topic modeling process.
- [fastText](https://fasttext.cc/) - The library used to detect the language of the text data.
- [Power BI](https://powerbi.microsoft.com/) - The business intelligence tool used to create interactive dashboards.



## References and Resources

- [r/morocco subreddit](https://www.reddit.com/r/morocco/)
- [Pushshift archives](https://the-eye.eu/redarcs/)
- [PushshiftDumps](https://github.com/Watchful1/PushshiftDumps)
- [PullPush Reddit API](https://pullpush.io/#docs)
- [BERTopic Docs](https://maartengr.github.io/BERTopic/getting_started/quickstart/quickstart.html)
- [Zero-shot classification](https://huggingface.co/tasks/zero-shot-classification)
- [Twitter-roBERTa-base model](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
- [DistilRoBERTa-base model](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base)

