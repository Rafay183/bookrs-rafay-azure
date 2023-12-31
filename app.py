from flask import Flask, render_template, request
import pickle
import pickle4 as pickle
import numpy as np
import pandas as pd
popular_df = pd.read_pickle(open('popular.pkl','rb'))
pt = pd.read_pickle(open('pt.pkl','rb'))
books = pd.read_pickle(open('books.pkl','rb'))
similarity_scores = pd.read_pickle(open('similarity_scores.pkl','rb'))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/Recommend')
def Recommend_ui():
    return render_template('Recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
    
    data = []
    
    for i in similar_items:
        item =[]
        print(pt.index[i[0]])
        temp_df = (books[books['Book-Title'] == pt.index[i[0]]])
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)

    print(data)

    return render_template('Recommend.html', data=data)

if __name__ == "__main__":
    app.run(debug=True ,port=8080,use_reloader=False)

