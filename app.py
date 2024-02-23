# Import the dependencies.
import pandas as pd
from flask import Flask, jsonify, render_template, request
from sklearn.metrics.pairwise import cosine_similarity
import pickle

popular_df=pickle.load(open('popular.pkl', 'rb'))
rating_input_df=pickle.load(open('rating_input.pkl', 'rb'))
books_df=pickle.load(open('books_df.pkl', 'rb'))
search_df=pickle.load(open('search.pkl', 'rb'))
ratings_df_all_cols=pickle.load(open('ratings_df_all_cols.pkl', 'rb'))
ratings_df_algo_input=pickle.load(open('ratings_df_algo_input.pkl', 'rb'))
books_df_algo_input=pickle.load(open('books_df_algo_input.pkl', 'rb'))

#import model
svd_default_model_mean = pickle.load(open('svd_default_model_mean.pickle', 'rb'))

#################################################
# Flask Setup
#################################################
app=Flask(__name__)

# #################################################
# # Flask Routes
# #################################################

@app.route("/")
def index():
    return render_template("index.html" ,
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           ratings_count=list(popular_df['count_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route("/recommend_book_ui")
def recommend_by_book_ui():
    return render_template("recommend_by_book.html")

@app.route("/recommend_book", methods=['post'])
def recommend_book():
    user_book=request.form.get("user_book")
    df_books_ratigs_user=rating_input_df.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
    # filling n/a with 0 so far, assuming it means that no interest for a book by a user,
    df_books_ratigs_user=df_books_ratigs_user.fillna(0)
    # create a dictionary for mapping between row number ans Book-Title
    index_title_dict=dict(df_books_ratigs_user.reset_index()['Book-Title'])
    # apply cosine_similarity
    books_similarity = cosine_similarity(df_books_ratigs_user)
    # convert output of cosine_similarity into df
    books_similarity_df=pd.DataFrame(books_similarity)
    # introduce title here
    books_similarity_df=books_similarity_df.rename(columns=index_title_dict)
    books_similarity_df.index=books_similarity_df.index.map(index_title_dict)
    # find a similarity list for the book
    recommendations=pd.DataFrame(books_similarity_df.loc[user_book,:])
    # remove the actual book
    book_title_list=[user_book]
    recommendations=recommendations[~recommendations.index.isin(book_title_list)].sort_values(by=user_book, ascending=False)
    # select top top_X_recommendations
    top_recommendations=recommendations[:6].rename(columns={user_book:'similarity rate'})
    top_recommendations=top_recommendations.rename_axis('Book-Title', axis='index')
    recommendations_full_info=pd.merge(top_recommendations, books_df, left_on='Book-Title',right_on='Book-Title', how='left')
    dict_years=dict(recommendations_full_info.groupby('Book-Title')['Year-Of-Publication'].max())
    for i, row in recommendations_full_info.iterrows():
        if row['Year-Of-Publication']!=dict_years[row['Book-Title']]:
            recommendations_full_info.loc[i,'Year-Of-Publication']=0
    recommendations_full_info=recommendations_full_info[recommendations_full_info['Year-Of-Publication'] != 0]
    recommendations_full_info=recommendations_full_info.drop_duplicates(subset=['Book-Title'])
    data = recommendations_full_info.to_dict('records')
    book_data=ratings_df_all_cols[ratings_df_all_cols['Book-Title']==user_book]
    average_book_rating=0
    count=0
    for i in book_data['Book-Rating']:
        if i!=0:
            average_book_rating+=i
            count+=1
    if count>0: 
        average_book_rating=round(average_book_rating/count,2)
    else: average_book_rating=None
    return render_template("recommend_by_book.html",data = data, book=user_book, book_d=book_data.iloc[1,:], avg_r=average_book_rating)

@app.route("/recommend_user_ui")
def recommend_user_ui():
    return render_template("recommend_by_user.html")

@app.route("/recommend_user", methods=['post'])
def recommend_user():
    user_id=int(request.form.get("user_id"))
        ## Find books prediction for a specific user and recommend top recommendations_count books
    recommendations_count=4
    model=svd_default_model_mean
    # find those titles that we consider for predictions (e.g. not read by a user)
    # find the books (titles) that were rated and presumably read by a user
    rated_titles=[i for i in ratings_df_algo_input.loc[ratings_df_algo_input['User-ID']==user_id,'Book-Title']]
    # find all the titles
    all_titles=ratings_df_algo_input['Book-Title'].unique()
    # separate those titles that were not read
    titles_input_to_recommend=[i for i in all_titles if i not in rated_titles]

    # find predictions for a user
    predictions=[model.predict(uid=user_id, iid=i) for i in titles_input_to_recommend]
    # get ratings estimate for books by the user
    ratings=[i.est for i in predictions]
    # convert predicted estimates by the user for not read books into df
    pred_dict={
        'Book-Title':titles_input_to_recommend,
        'Estimated_Rate':ratings}
    predictions_book=pd.DataFrame(pred_dict).sort_values('Estimated_Rate',ascending = False)
    top_recommendations=predictions_book.head(recommendations_count)
        
    # populate books with full info, selecting those books with the most recent year of publication
    recommendations_full_info=pd.merge(top_recommendations, books_df_algo_input, left_on='Book-Title',right_on='Book-Title', how='left')
    dict_years=dict(recommendations_full_info.groupby('Book-Title')['Year-Of-Publication'].max())
    for i, row in recommendations_full_info.iterrows():
        if row['Year-Of-Publication']!=dict_years[row['Book-Title']]:
            recommendations_full_info.loc[i,'Year-Of-Publication']=0
    recommendations_full_info=recommendations_full_info[recommendations_full_info['Year-Of-Publication'] != 0]
    recommendations_full_info=recommendations_full_info.drop_duplicates(subset=['Book-Title'])
    data = recommendations_full_info.to_dict('records')
     # find original user ratings
    u_data=ratings_df_all_cols[ratings_df_all_cols['User-ID']==user_id].sort_values(by='Book-Rating', ascending=False)
    u_data=u_data[['Book-Title','Book-Rating','Book-Author','Publisher']]
    if u_data.shape[0]>10:
        u_data=u_data.head(10)
    user_history = u_data.to_dict('records')
    return render_template("recommend_by_user.html", data=data, datau=user_history, user_id=user_id)

@app.route('/search', methods=['GET'])
def view_books():
    search_query = request.args.get('search', '')      
    if search_query:
        filtered_books_df = search_df[search_df['Book-Title'].str.contains(search_query, case=False, na=False)]
        books = filtered_books_df.to_dict('records')
    else:
        books = search_df.to_dict('records')

    return render_template('search.html', books=books)

@app.route('/tableau')
def view_tableau():
    return render_template('tableau.html')



if __name__== "__main__":
    app.run(debug=True)