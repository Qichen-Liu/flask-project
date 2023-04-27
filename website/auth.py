import pymysql
import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin

auth = Blueprint('auth', __name__)

# GET request: retrieve info
# POST request: make some change to the database

# config the database
conn = pymysql.Connect(
    host="localhost",
    port=3306,
    user="root",
    password="t00d00",
    db="cs6083",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

# define login_manager to manager user authentication
login_manager = LoginManager()


# define your User class
class User(UserMixin):
    def __init__(self, username):
        self.id = username

    def __repr__(self):
        return f'<User {self.id}>'


@login_manager.user_loader
def load_user(user_id):
    # return an instance of the User class for the given user_id
    return User(user_id)


# search for song
@auth.route('/', methods=['GET', 'POST'])
def searchSong():
    if request.method == 'POST':
        genre = request.form.get('genre')
        avgRating = request.form.get('avgRating')
        artistName = request.form.get('artistName')

        if artistName and len(artistName.split()) < 2:
            flash('You need to type in both the first name and the last name', category='error')
            return render_template("home.html")
        else:
            name = artistName.split(" ")

        # cursor used to send queries
        cursor = conn.cursor()

        # check if all exists and valid type
        if genre and not avgRating and not artistName:  # only genre
            query = "SELECT title, fname, lname, albumID, genre " \
                    "FROM song JOIN artistPerformsSong ON song.songID = artistPerformsSong.songID " \
                    "JOIN songInAlbum on song.songID = songInAlbum.songID " \
                    "JOIN artist ON artist.artistID = artistPerformsSong.artistID " \
                    "JOIN songGenre ON songGenre.songID = song.songID WHERE genre = %s"
            cursor.execute(query, (genre))
            # stores the results in data
            songs = cursor.fetchall()
            if songs:
                return render_template("home.html", songs=songs, user=current_user, genre=genre,
                                       avgRating=avgRating, artistName=artistName)
            else:
                flash('No song found, please try again!', category='error')
                return redirect(url_for('views.home'))

        elif genre and avgRating and not artistName:  # genre + avgRating
            query = "SELECT song.songID, songInAlbum.albumID, song.title, AVG(rateSong.stars) AS avg_score, artist.fname, artist.lname, songGenre.genre " \
                    "FROM song JOIN rateSong ON song.songID = rateSong.songID " \
                    "JOIN songGenre ON songGenre.songID = rateSong.songID " \
                    "JOIN artistPerformsSong ON song.songID = artistPerformsSong.songID " \
                    "JOIN songInAlbum on song.songID = songInAlbum.songID " \
                    "JOIN artist ON artist.artistID = artistPerformsSong.artistID " \
                    "GROUP BY songID, artist.fname, artist.lname, songGenre.genre, songInAlbum.albumID " \
                    "HAVING AVG(rateSong.stars) >= %s AND songGenre.genre = %s"
            cursor.execute(query, (avgRating, genre))
            # stores the results in data
            songs = cursor.fetchall()
            if songs:
                return render_template("home.html", songs=songs, user=current_user, genre=genre,
                                       avgRating=avgRating, artistName=artistName)
            else:
                flash('No song found, please try again!', category='error')
                return redirect(url_for('views.home'))

        elif genre and not avgRating and artistName:  # genre + artistName
            query = "SELECT title, fname, lname, albumID, genre " \
                    "FROM song JOIN artistPerformsSong ON song.songID = artistPerformsSong.songID " \
                    "JOIN songInAlbum on song.songID = songInAlbum.songID " \
                    "JOIN artist ON artist.artistID = artistPerformsSong.artistID " \
                    "JOIN songGenre ON songGenre.songID = song.songID " \
                    "WHERE genre = %s AND fname = %s AND lname = %s"
            cursor.execute(query, (genre, name[0], name[1]))
            # stores the results in data
            songs = cursor.fetchall()
            if songs:
                return render_template("home.html", songs=songs, user=current_user, genre=genre,
                                       avgRating=avgRating, artistName=artistName)
            else:
                flash('No song found, please try again!', category='error')
                return redirect(url_for('views.home'))

        elif not genre and avgRating and not artistName:  # only avgRating
            query = "SELECT song.songID, songInAlbum.albumID, song.title, AVG(rateSong.stars) AS avg_score, artist.fname, artist.lname, songGenre.genre " \
                    "FROM song JOIN rateSong ON song.songID = rateSong.songID " \
                    "JOIN songGenre ON songGenre.songID = rateSong.songID " \
                    "JOIN artistPerformsSong ON song.songID = artistPerformsSong.songID " \
                    "JOIN songInAlbum on song.songID = songInAlbum.songID " \
                    "JOIN artist ON artist.artistID = artistPerformsSong.artistID " \
                    "GROUP BY songID, artist.fname, artist.lname, songGenre.genre, songInAlbum.albumID " \
                    "HAVING AVG(rateSong.stars) >= %s"
            cursor.execute(query, (avgRating))
            # stores the results in song
            songs = cursor.fetchall()
            if songs:
                return render_template("home.html", songs=songs, user=current_user, genre=genre,
                                       avgRating=avgRating, artistName=artistName)
            else:
                flash('No song found, please try again!', category='error')
                return redirect(url_for('views.home'))


        elif not genre and avgRating and artistName:  # avgRating + artistName
            query = "SELECT song.songID, songInAlbum.albumID, song.title, AVG(rateSong.stars) AS avg_score, artist.fname, artist.lname, songGenre.genre " \
                    "FROM song JOIN rateSong ON song.songID = rateSong.songID " \
                    "JOIN songGenre ON songGenre.songID = rateSong.songID " \
                    "JOIN artistPerformsSong ON song.songID = artistPerformsSong.songID " \
                    "JOIN songInAlbum on song.songID = songInAlbum.songID " \
                    "JOIN artist ON artist.artistID = artistPerformsSong.artistID " \
                    "GROUP BY songID, artist.fname, artist.lname, songGenre.genre, songInAlbum.albumID " \
                    "HAVING AVG(rateSong.stars) >= %s AND artist.fname = %s AND artist.lname = %s"
            cursor.execute(query, (avgRating, name[0], name[1]))
            # stores the results in data
            songs = cursor.fetchall()
            if songs:
                return render_template("home.html", songs=songs, user=current_user, genre=genre,
                                       avgRating=avgRating, artistName=artistName)
            else:
                flash('No song found, please try again!', category='error')
                return redirect(url_for('views.home'))

        elif not genre and not avgRating and artistName:  # only artistName
            query = "SELECT title, fname, lname, albumID, genre " \
                    "FROM song JOIN artistPerformsSong ON song.songID = artistPerformsSong.songID " \
                    "JOIN songInAlbum on song.songID = songInAlbum.songID " \
                    "JOIN artist ON artist.artistID = artistPerformsSong.artistID " \
                    "JOIN songGenre ON songGenre.songID = song.songID WHERE fname = %s AND lname = %s"
            cursor.execute(query, (name[0], name[1]))
            # stores the results in songs
            songs = cursor.fetchall()
            if songs:
                return render_template("home.html", songs=songs, user=current_user, genre=genre,
                                       avgRating=avgRating, artistName=artistName)
            else:
                flash('No song found, please try again!', category='error')
                return redirect(url_for('views.home'))

        elif genre and avgRating and artistName:  # genre + avgRating + artistName
            query = "SELECT song.songID, songInAlbum.albumID, song.title, AVG(rateSong.stars) AS avg_score, artist.fname, artist.lname, songGenre.genre " \
                    "FROM song JOIN rateSong ON song.songID = rateSong.songID " \
                    "JOIN songGenre ON songGenre.songID = rateSong.songID " \
                    "JOIN artistPerformsSong ON song.songID = artistPerformsSong.songID " \
                    "JOIN songInAlbum on song.songID = songInAlbum.songID " \
                    "JOIN artist ON artist.artistID = artistPerformsSong.artistID " \
                    "GROUP BY songID, artist.fname, artist.lname, songGenre.genre, songInAlbum.albumID " \
                    "HAVING AVG(rateSong.stars) >= %s AND artist.fname = %s AND artist.lname = %s AND songGenre.genre = %s"
            cursor.execute(query, (avgRating, name[0], name[1], genre))
            # stores the results in data
            songs = cursor.fetchall()
            if songs:
                return render_template("home.html", songs=songs, user=current_user, genre=genre,
                                       avgRating=avgRating, artistName=artistName)
            else:
                flash('No song found, please try again!', category='error')
                return redirect(url_for('views.home'))
        else:
            flash("You must type in genre/avgRating/artistName to be able to search", category='error')
    return render_template("home.html")


# log in
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # get a post request
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # cursor used to send queries
        cursor = conn.cursor()
        # select the username
        query = 'SELECT username, pwd FROM user WHERE username = %s'
        cursor.execute(query, (username))
        # stores the results in a variable
        data = cursor.fetchone()

        if data:
            if check_password_hash(data['pwd'], password):
                flash('Logged in successfully!', category='success')
                # track who is logging in now
                session['username'] = username
                # update the last-time-login in database
                today = datetime.date.today()
                formatted_date = today.strftime('%Y-%m-%d')
                query = 'UPDATE user SET lastlogin = %s WHERE user.username = %s'
                cursor.execute(query, (formatted_date, username))
                conn.commit()
                cursor.close()

                # member the user
                user = User(username)
                login_user(user, remember=True)

                # check if bugggggggggg
                return redirect(url_for('views.home'))

            else:
                flash('Invalid password, try again!', category='error')
        else:
            flash('Username does not exist!', category='error')
    return render_template("login.html", user=current_user)


# log out
@auth.route('/logout')
@login_required
def logout():
    flash('Logged out successfully!')
    # pop the user in session
    session.pop('user_id', None)
    # logout
    logout_user()
    return redirect(url_for('views.home'))


# sign up
@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    # get a post request
    if request.method == 'POST':
        # get all the info of the new user
        username = request.form.get('username')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # check if input is valid
        if len(username) <= 3:
            flash('Username must be greater than 3 characters.', category='error')
        elif len(firstName) <= 1:
            flash('First name must be greater than 1 character.', category='error')
        elif len(lastName) <= 1:
            flash('Last name must be greater than 1 character.', category='error')
        elif len(password1) <= 4:
            flash('Password must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
        elif len(nickname) <= 2:
            flash('Nickname must be greater than 2 characters.', category='error')
        else:
            # cursor used to send queries
            cursor = conn.cursor()
            # select the username
            query = 'SELECT * FROM user WHERE username = %s'
            cursor.execute(query, (username))
            # stores the results in a variable
            data = cursor.fetchone()
            if data:
                flash('Username already exists! Try again!', category='error')
                return render_template("sign_up.html")
            else:
                # hash the password with sha256
                password = generate_password_hash(password1, method='sha256')
                session['username'] = username

                file = open('userinfo.txt', 'a')
                file.write(username + ', ' + password1 + ', ' + firstName + ', ' + lastName + ', ' + nickname + '\n')
                file.close()

                # the current day is the last time login for new user
                today = datetime.date.today()
                formatted_date = today.strftime('%Y-%m-%d')

                # add user to database
                ins = 'INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s)'
                cursor.execute(ins, (username, password, firstName, lastName, formatted_date, nickname))
                conn.commit()
                cursor.close()

                # member the user
                user = User(username)
                login_user(user, remember=True)

                # flash successful message
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)


@auth.route('/new-content')
@login_required
def newContent():
    username = session['username']
    print("new content user is " + username)

    # retrieve the artist the user is a fan of
    cursor = conn.cursor()
    query = 'SELECT title, releaseDate, songURL, genre ' \
            'FROM song NATURAL JOIN artistPerformsSong NATURAL JOIN userFanOfArtist ' \
            'NATURAL JOIN songGenre WHERE releaseDate >= DATE_SUB(NOW(), INTERVAL 1 YEAR) ' \
            'AND username = %s'

    # CHANGE THE YEAR TO MONTH
    cursor.execute(query, (username))
    newSongs = cursor.fetchall()

    # retrieve the new reviews
    query = 'SELECT reviewSong.username, reviewSong.reviewText, song.title, reviewSong.reviewDate ' \
            'FROM reviewSong JOIN follows ON follows.follows = reviewSong.username ' \
            'JOIN user ON user.username = follows.follower JOIN song ON song.songID = reviewSong.songID ' \
            'WHERE reviewSong.reviewDate >= DATE_SUB(NOW(), INTERVAL 1 YEAR) AND follows.follower = %s'
    cursor.execute(query, (username))
    newSongReview = cursor.fetchall()

    query = 'SELECT reviewAlbum.username, reviewAlbum.reviewText, reviewAlbum.albumID, reviewAlbum.reviewDate ' \
            'FROM reviewAlbum JOIN follows ON follows.follows = reviewAlbum.username ' \
            'JOIN user ON user.username = follows.follower ' \
            'WHERE reviewAlbum.reviewDate >= DATE_SUB(NOW(), INTERVAL 1 YEAR) AND follows.follower = %s'
    cursor.execute(query, (username))
    newAlbumReview = cursor.fetchall()

    if newSongs or newSongReview or newAlbumReview:
        return render_template("newContent.html", songs=newSongs, songReviews=newSongReview,
                               albumReviews=newAlbumReview, user=current_user)
    else:
        flash('There are no new songs posted within this month for ' + username)
    return redirect(url_for('views.home'))


@auth.route('/rate', methods=['GET', 'POST'])
@login_required
def rate():
    if request.method == 'POST':
        post_id = request.form['post_id']
        if post_id == '1':
            song_title = request.form.get('title')
            if not song_title:
                flash('Song title cannot be blank!', category='error')
                return render_template('rate.html', user=current_user)

            cursor = conn.cursor()
            query = "SELECT title, fname, lname, song.songID, genre " \
                    "FROM song JOIN artistPerformsSong ON song.songID = artistPerformsSong.songID " \
                    "JOIN songInAlbum on song.songID = songInAlbum.songID " \
                    "JOIN artist ON artist.artistID = artistPerformsSong.artistID " \
                    "JOIN songGenre ON songGenre.songID = song.songID WHERE title = %s"
            cursor.execute(query, (song_title))
            songs = cursor.fetchall()
            if songs:
                songID = songs[0]
                return render_template('rate.html', songs=songs, user=current_user)
            else:
                flash('No songs found! Please change the title!', category='error')
        elif post_id == '2':
            songID = request.form['song_id']
            review_text = request.form.get('reviewText')
            if not review_text:
                flash('Review comments cannot be blank!', category='error')
                return render_template('rate.html', user=current_user)
            # the current day is the last time login for new user
            today = datetime.date.today()
            formatted_date = today.strftime('%Y-%m-%d')
            cursor = conn.cursor()
            # select to see if user already reviewed this song
            query = 'SELECT user.username, reviewSong.songID ' \
                    'FROM reviewSong JOIN user ON reviewSong.username = user.username ' \
                    'WHERE user.username = %s'
            cursor.execute(query, (current_user.id))
            reviews = cursor.fetchall()
            if reviews:
                flash('You already left a review for this song. The previous review will be overwritten', 'warning')
                update = 'UPDATE reviewSong SET reviewText = %s, reviewDate = %s ' \
                         'WHERE reviewSong.username = %s AND reviewSong.songID = %s'
                cursor.execute(update, (review_text, formatted_date, current_user.id, songID))
                conn.commit()
                cursor.close()
            else:
                # add review to database
                ins = 'INSERT INTO reviewSong VALUES(%s, %s, %s, %s)'
                cursor.execute(ins, (current_user.id, songID, review_text, formatted_date))
                conn.commit()
                cursor.close()
                flash('Thank you for leaving a comment!', category='success')
                return render_template('rate.html', user=current_user)

        elif post_id == '3':
            songID = request.form['song_id']
            rating_star = request.form.get('stars')
            if not rating_star:
                flash('Rating cannot be blank!', category='error')
                return render_template('rate.html', user=current_user)

            # the current day is the last time login for new user
            today = datetime.date.today()
            formatted_date = today.strftime('%Y-%m-%d')
            cursor = conn.cursor()
            query = 'SELECT user.username, reviewSong.songID ' \
                    'FROM ratesong JOIN user ON ratesong.username = user.username ' \
                    'WHERE user.username = %s'
            cursor.execute(query, (current_user.id))
            rates = cursor.fetchall()
            if rates:
                flash('You already left a review for this song. The previous review will be overwritten', 'warning')
                update = 'UPDATE ratesong SET reviewText = %s, reviewDate = %s' \
                         'WHERE ratesong.username = %s AND reviewSong.songID = %s'
                cursor.execute(update, (rating_star, formatted_date, current_user.id, songID))
                conn.commit()
                cursor.close()
            else:
                # add review to database
                ins = 'INSERT INTO ratesong VALUES(%s, %s, %s, %s)'
                cursor.execute(ins, (current_user.id, songID, rating_star, formatted_date))
                conn.commit()
                cursor.close()
                flash('Thank you for the rating!', category='success')
                return render_template('rate.html', user=current_user)

    return render_template('rate.html', user=current_user)