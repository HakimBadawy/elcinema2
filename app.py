from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import re
app = Flask(__name__)



app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= 'Kwalid@92'
app.config['MYSQL_DB']= 'egmovieindex'

mysql = MySQL(app)



@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method == 'POST': 
        #fetch form details:
        formAns = request.form['options']
        if formAns == 'Reg':
            return redirect('/SignUp')
        elif formAns== 'Login':
            return redirect('/Login')
    return render_template('index.html')
    
#-------------------------------------------------------
#-------------------------------------------------------
#-------------------------------------------------------

@app.route('/SignUp', methods=['GET', 'POST'])
def SignUp():
    if request.method == 'POST':
        #fetch form data
        userDetails = request.form
        username = userDetails['Username']
        email = userDetails['Email']
        age =  userDetails['Age']
        birthdate =  userDetails['Birthdate']
        gender = userDetails['Gender']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(`Email Address`, Username, Age, Birthdate, Gender) values (%s, %s, %s, %s, %s)", (email, username, age, birthdate, gender[0]))
        mysql.connection.commit()
        cur.close()
        return redirect('/home')
    return render_template('SignUp.html')

#-------------------------------------------------------
#-------------------------------------------------------
#-------------------------------------------------------

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        #fetch form data
        userDetails = request.form
        email = userDetails['Email']
        cur = mysql.connection.cursor()
        cur.execute("Select `Email Address` FROM user WHERE `Email Address` = %s", [email])
        mysql.connection.commit()
        if len(cur.fetchall()) != 0:
            cur.close()
            return redirect('/home')
        else:
            cur.close()
            return redirect('/SignUp')

    return render_template('Login.html')

#-------------------------------------------------------
#-------------------------------------------------------
#-------------------------------------------------------
@app.route('/addReview', methods=['GET', 'POST'])
def addReview():
    if request.method == 'POST':    
        mName = request.form['movieName']
        review = request.form['review']
        rating = request.form['rating']
        email = request.form['email']
        #check if user is registered
        cur2 = mysql.connection.cursor()
        cur2.execute("select `Email address` from user where `Email address` = %s", [email])
        mysql.connection.commit()
        if len(cur2.fetchall()) == 0:    #user not registered
            cur2.close()
            return redirect('/SignUp')
        cur2.close()
        cur = mysql.connection.cursor()
        cur.execute("select Name from movies where Name = %s", [mName])
        mysql.connection.commit()

        if len(cur.fetchall())>0:
            cur.close()
            cur = mysql.connection.cursor()
            cur.execute("select `Release Date` from movies where Name = %s", [mName] )
            mysql.connection.commit()
            release_date = cur.fetchall()[0]
            cur.close()
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO userreviews(`Email Address`, `Movie Name`, `Movie Release Date`, `Review`, `Rating`) Values (%s, %s, %s, %s, %s)", [email, mName, release_date, review, rating])
            mysql.connection.commit()
            cur.close()
            return redirect('/home')
        else:
            return "Movie does not exist in our database. Check spelling try again"
    return render_template('addReview.html')
#-------------------------------------------------------
@app.route('/viewReviews', methods=['GET', 'POST'])
def viewReviews():
    if request.method == 'POST':
        mName= request.form['mName']
        cur = mysql.connection.cursor()
        cur.execute("select `Movie Name`, Review, Rating, `Email address` from userreviews where `Movie Name` = %s", [mName])
        mysql.connection.commit()
        results = cur.fetchall()

        if len(results)>0:
            cur.close()
            return render_template('viewReviews.html', results = results)
        else: 
            return "No reviews for movie"
    return render_template('viewReviews.html')
#view reviews of a given movie
    #search by movie name
    #if movie exists: display user reviews and ratings
    #else: search again
#-------------------------------------------------------
@app.route('/castMovies', methods=['GET', 'POST'])
def castMovies():
    if request.method == 'POST':
        cName= request.form['cName']
        cur = mysql.connection.cursor()
        cur.execute("select `Movie Name`, role from castinmovie where `Cast name` = %s", [cName])
        mysql.connection.commit()
        results = cur.fetchall()
        if len(results)>0:
            cur.close()
            return render_template('castMovies.html', results = results)
        else: 
            cur.close()
            return "No movies for this cast member or cast member does not exist in our database"
    return render_template('castMovies.html')
#show all movies of a cast member
    #search by castmember
    #if castmember exists: display all movies
    #else: search again
#-------------------------------------------------------
@app.route('/genreMovies', methods=['GET', 'POST'])
def genreMovies():
    if request.method == 'POST':
        genre= request.form['genre']
        if genre == 'كوميدي':
            genre = 'ﻛﻮﻣﻴﺪﻱ'
        elif genre =='رياضي':
            genre = 'ﺭﻳﺎﺿﻲ'
        elif genre == 'تشويق و إثارة':
            genre = 'ﺗﺸﻮﻳﻖ ﻭﺇﺛﺎﺭﺓ '
        elif genre == 'خيال علمي':
            genre = 'ﺧﻴﺎﻝ ﻋﻠﻤﻲ '
        elif genre == 'قصير':
            genre = 'ﻗﺼﻴﺮ'
        elif genre == 'دراما':
            genre = 'ﺩﺭاﻣﺎ'
        elif genre == 'رومانسي':
            genre = 'ﺭﻭﻣﺎﻧﺴﻲ'
        elif genre == 'وثائقي':
            genre = 'ﻭﺛﺎﺋﻘﻲ'
        elif genre == 'حركة':
            genre = 'ﺣﺮﻛﺔ'
        elif genre == 'رعب':
            genre = 'ﺭﻋﺐ'
        elif genre == 'غموض':
            genre = 'ﻏﻤﻮﺽ'
        elif genre == 'تاريخي':
            genre = 'تاريخي'
        elif genre == 'حرب':
            genre = 'ﺣﺮﺏ'
        elif genre == 'سيرة ذاتية':
            genre = 'ﺳﻴﺮﺓ ﺫاﺗﻴﺔ'
        elif genre == 'ديني':
            genre = 'ديني'
        elif genre == 'مغامرات':
            genre = 'ﻣﻐﺎﻣﺮاﺕ'
        elif genre == 'رسوم متحركة':
            genre = 'ﺭﺳﻮﻡ ﻣﺘﺤﺮﻛﺔ'

        cur = mysql.connection.cursor()
        cur.execute("select `Movie Name`, `Movie Release Date` from moviegenre where Genre = %s", [genre])
        mysql.connection.commit()
        results = cur.fetchall()
        if len(results)>0:
            cur.close()
            return render_template('genreMovies.html', results = results)
        else: 
            cur.close()
            return "Please check the spelling of the genre."
    return render_template('genreMovies.html')
#show movies of a specific genre
#-------------------------------------------------------

@app.route('/top10', methods=['GET', 'POST'])
def top10():
    cur = mysql.connection.cursor()
    cur.execute("select movies.Name, movies.`Total revenue(EGP)` from egmovieindex.movies order by movies.`Total revenue(EGP)` desc limit 10")
    mysql.connection.commit()
    results = cur.fetchall()
    return render_template('top10.html', results = results)
#top 10 by revenue
#-------------------------------------------------------

@app.route('/movieInfo', methods=['GET', 'POST'])
def movieInfo():
    if request.method == 'POST':
        mName= request.form['mName']
        cur = mysql.connection.cursor()
        cur.execute("select * from movies where Name = %s", [mName])
        mysql.connection.commit()
        results = cur.fetchall()
        if len(results)>0:
            cur.close()
            return render_template('movieInfo.html', results = results)
        else: 
            cur.close()
            return "Movie does not exist in our database"
    return render_template('movieInfo.html')
#view movie information
#-------------------------------------------------------

@app.route('/castInfo', methods=['GET', 'POST'])
def castInfo():
    if request.method == 'POST':
        cName= request.form['cName']
        cur = mysql.connection.cursor()
        cur.execute("select * from castmember where Name = %s", [cName])
        mysql.connection.commit()
        results = cur.fetchall()
        if len(results)>0:
            cur.close()
            return render_template('castInfo.html', results = results)
        else: 
            cur.close()
        return "Cast member does not exist in our database"
    return render_template('castInfo.html')
#view cast member information
#-------------------------------------------------------

@app.route('/home', methods=['GET', 'POST'])
def Home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)