# Book Recommendation System
Building of a Book Recommendation System, based on user and book interactions represented in rating scores. The system should help both:
 - *book readers* to discover great content quickly,
 - *businesses* with assiting in increasing sales or engagement levels on their platforms. <br>

The system combines:
 - Non-Personilized approach, suggesting brand new users Top Rated books within statistically significant subset
   <p align="center">
   <img src="https://github.com/ValentynaK17/Books-Recommendation-System/blob/main/Output/Non_Personilized_Recommendations.png">
   </p>
 - Memory-based approach within Colaborative filtering, with Cosine Similarity technique, when the whole dataset is used directly to find similarities between books, based on rating patterns. Having user to enter a book title, the system recommends those books with highest similarity index
   <p align="center">
   <img src="https://github.com/ValentynaK17/Books-Recommendation-System/blob/main/Output/Book_Based_Recommendation.png">
   </p>
 - Model-based methods within Colaborative filtering, with SVD/SVD Funk, used for training and predictions of user rates for books. Having predictions of user rates, for recommendations sytem selects those books, which were not read by user and had highest predicted ratings
   <p align="center">
   <img src="https://github.com/ValentynaK17/Books-Recommendation-System/blob/main/Output/User_Based_Recommendations.png">
   </p>

This book recommendation system is trying to suggest books based on users' past interactions (left explicit rating scores for books from 1 to 10, or implicit interaction, represented in db as 0 rating score):
| | Book1 | Book2 | ... | BookN |
|:---:|:-----:|:-----:|:---:|:-----:|
| **User1** |   3   |    N/A   | ... |   8   |
| **User2** |   9   |   10  | ... |   0   |
| ...      |  ...  |  ...  | ... |  ...  |
| **UserN** |   4   |   4   | ... |    N/A   |

## Installation
1. Assuming Python and Flask are installed, run the app.py script.
2. Access the Web Application by opening a web browser and navigating to the URL generated (e.g. http://127.0.0.1:5000).
   
The home page displays the Most Popular Books, however user can switch to 'Recommend by Book'/'Recommend by User' pages for personalized recommendations. 'Search Book' would help with searching for exact book titles.

### Limitations
This engine uses a static set of data so far.

### Dataset
Our dataset was obtained from [Kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset). It included these 3 files providing metadata about users and books. We generated a fourth dataset, for further analysis and visualizations.
Books:ISBN, Book title, Book author, Year of publication, Publisher
Users: User ID, Location(country)
Ratings: User ID, ISBN, Book rating
Geo Location: Country, Latitude, Longitude

### Methodology
The project consisted of the following broad steps:
1. Data cleaning e.g.
   - Convering 'Book-Ratings' as well as 'Year of Publication' to numerical fields;
   - Leaving only those records with Year of Publication' >0;
2. Exploratory data analysis, e.g.
   - analysis of how many reviews do usually books have
   <p align="center">
   <img src="https://github.com/ValentynaK17/Books-Recommendation-System/blob/main/Output/Binning_Books.png" width="555">
   </p>
   - analysis of how many books do usually users rate/interact with
   <p align="center">
   <img src="https://github.com/ValentynaK17/Books-Recommendation-System/blob/main/Output/Binning_User.png" width="555">
   </p>
    - analysis of ratings distribution (rating score equal to 0 is an implicit user-book interaction data)
   <p align="center">
   <img src="https://github.com/ValentynaK17/Books-Recommendation-System/blob/main/Output/Book_Rating_Values.png" width="555">
   </p>
3. Data Preprocessing, e.g.
   - Handling duplicated records (e.g. use average rate per duplicated records for same userXbook ratings)
   - Normalization of rating data by mean (center method)
   - Splitting the data into training and testing sets.
4. Researching and experimenting on various recommendation system techniques, e.g.
   - Starting from pure SVD approach, as shown below:
     <p align="center">
        <img src="https://github.com/ValentynaK17/Books-Recommendation-System/blob/main/Output/SVD_Approach.png" width="555">
     </p>
     and switching to SVD Funk, using Surprise, which is a Pyhton scikit module specifically designed for building recommender systems
   - training both SVD and SVD Funk models using the training dataset. To do this the data were devided into training and test sets on a per-user basis. Approximately 80% of each user's records were aassigned to the training set, while the remaining 20% reserved for the test set. This approach helps with having both the training and test sets containing data from all users.
   - taking into account all the data, including implicit ratings VS weighted mean (shown below) instead of implicit ratings VS excluding implicit ratings at all
     <p align="center">
        <img src="https://github.com/ValentynaK17/Books-Recommendation-System/blob/main/Output/WeightedMean.png" width="777">
     </p>
   - cross-validating the model using the Surprise module
   - trying to optimize SVD Funk with hyperparameters tuning (number of latent factors, number of iterations, step size for the gradient descent optimization, regularization  term used for all parameter to prevent overfitting)
    
   <p align="center">
   <img src="https://github.com/ValentynaK17/Books-Recommendation-System/blob/main/Output/SVD_Model_RMSE_Comparison_color.png" width="555">
   </p>
   
For evaluation of the model RMSE metric was used (Root Mean Square Error)
<p align="center">
<img src="https://github.com/ValentynaK17/Books-Recommendation-System/blob/main/Output/FormulaRMSE.png" width="222">
</p>

where:
 - ***Predicted_i*** is a predicted value for the ith observation,
 - ***Actual_i*** is an observed(actual) value for the ith observation,
 - ***N*** is a total number of observations.

Accuracy measurement for test set shows that SVD produces a little  inaccurate rating predictions, with tendency to lowering rates.  <br>
It's observed that while a tuned SVD Funk improved results, the most accurate predictions emerged from  SVD Funk model with default hyperparameters and weighted mean instead of implicit rating data.
   <p align="center">
   <img src="https://github.com/ValentynaK17/Books-Recommendation-System/blob/main/Output/SVD_Models_RMSE_Comparison_Color_White.png" width="555">
   </p>

5. Building and interactive website:
    - Flask for handling HTTP requests, manage routing and serving web pages;
    - Pandas for data manipulations
    - Pickle for loadin pre-processed data and a model
    - HTML for areating frontend templates that Flask renders and serves to the client's browser
    - CSS for styling web pages
6. Creation a dashboard visualizations
![image](https://github.com/ZinDaria/BookRecomendationSystem/assets/141193973/c776b965-9122-45fd-9125-3abf24f77665)
![image](https://github.com/ZinDaria/BookRecomendationSystem/assets/141193973/9bfa4ece-1ec4-4abb-bba9-4813c9535f8f)
![image](https://github.com/ZinDaria/BookRecomendationSystem/assets/141193973/a5a7b8b7-e1f9-4fa0-80cd-197f8ef41e2c)



### Tools, Languages and Libraries
Data Preprocessing and EDA - Python, Jupyter Notebook, Pandas, Matplotlib, Numpy, Scipy, Scikit-learn
Machine Learning - Singular Value Decomposition (SVD), SVD Funk
Web Development - Flask, HTML, CSS
IDE - Visual Studio Code
Visualization - Tableau

### References
 - [Recommendation Engine Concepts](https://www.analyticsvidhya.com/blog/2018/06/comprehensive-guide-recommendation-engine-python/)
 - [Cosine Similarity in ML](https://analyticsindiamag.com/cosine-similarity-in-machine-learning/)
 - [Surprise module documantation](https://surprise.readthedocs.io)
 - [Example of the process for building Recommendation System](https://rpubs.com/Argaadya/recommender-svdf)
 - [A little of comments review for matrix factorization approach](https://stats.stackexchange.com/questions/31096/how-do-i-use-the-svd-in-collaborative-filtering)
 - [BootStrap](https://www.w3schools.com/bootstrap/bootstrap_get_started.asp)  
 - [Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/)  
 - [Jinja Template](https://jinja.palletsprojects.com/en/3.1.x/)  
 - [CSS](https://www.w3schools.com/css/)  


### Acknowledgements
Project Team:
1. Valentyna K.
2. Neha S.
3. Daria Z.
4. Seeke O.D

It has been great working and learning with you all.




 

