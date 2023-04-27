import pymysql
import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin

auth = Blueprint('auth', __name__)

# test for push
# GET request: retrieve info
# POST request: make some change to the database

# config the database
conn = pymysql.Connect(
    host="localhost",
    port=8889,
    user="root",
    password="root",
    db="FatEar",
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
                return render_template("searchResult.html", songs=songs, user=current_user)
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
                return render_template("searchResult.html", songs=songs, user=current_user)
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
                return render_template("searchResult.html", songs=songs, user=current_user)
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
                return render_template("searchResult.html", songs=songs, user=current_user)
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
                return render_template("searchResult.html", songs=songs, user=current_user)
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
                return render_template("searchResult.html", songs=songs, user=current_user)
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
                return render_template("searchResult.html", songs=songs, user=current_user)
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
            query = "SELECT song.songID, title, fname, lname, albumID, genre " \
                    "FROM song JOIN artistPerformsSong ON song.songID = artistPerformsSong.songID " \
                    "JOIN songInAlbum on song.songID = songInAlbum.songID " \
                    "JOIN artist ON artist.artistID = artistPerformsSong.artistID " \
                    "JOIN songGenre ON songGenre.songID = song.songID WHERE title = %s"
            cursor.execute(query, (song_title))
            songs = cursor.fetchall()
            if songs:
                return render_template('rate.html', songs=songs, user=current_user)
            else:
                flash('No songs found! Please change the title!', category='error')

        elif post_id == '2':
            # get review text and songID form frontend
            review_text = request.form.get('reviewText')
            songID = request.form.get('song_id')

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
                    'WHERE user.username = %s AND rateSong.songID = %s'
            cursor.execute(query, (current_user.id, songID))
            reviews = cursor.fetchall()
            if reviews:
                flash('You already left a review for this song. The previous review will be overwritten', 'error')
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
            rating_star = request.form.get('stars')
            songID = request.form.get('song_id')
            if not rating_star:
                flash('Rating cannot be blank!', category='error')
                return render_template('rate.html', user=current_user)

            # the current day is the last time login for new user
            today = datetime.date.today()
            formatted_date = today.strftime('%Y-%m-%d')
            cursor = conn.cursor()
            # select to see if user already reviewed this song
            query = 'SELECT user.username, rateSong.songID ' \
                    'FROM rateSong JOIN user ON rateSong.username = user.username ' \
                    'WHERE user.username = %s AND rateSong.songID = %s'
            cursor.execute(query, (current_user.id, songID))
            ratings = cursor.fetchall()
            if ratings:
                flash('You already left a review for this song. The previous review will be overwritten', 'error')
                update = 'UPDATE rateSong SET stars = %s, ratingDate = %s ' \
                         'WHERE rateSong.username = %s AND rateSong.songID = %s'
                cursor.execute(update, (rating_star, formatted_date, current_user.id, songID))
                conn.commit()
                cursor.close()
            else:
                # add user to database
                ins = 'INSERT INTO rateSong VALUES(%s, %s, %s, %s)'
                cursor.execute(ins, (current_user.id, songID, rating_star, formatted_date))
                conn.commit()
                cursor.close()
                flash('Thank you for rating a song!', category='success')
                return render_template('rate.html', user=current_user)
    return render_template('rate.html', user=current_user)


@auth.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    username = current_user.id
    cursor = conn.cursor()
    friends_query = 'SELECT user2 AS friend FROM friend ' \
                    'WHERE user1 = %s AND acceptStatus = %s ' \
                    'UNION SELECT user1 AS friend FROM friend ' \
                    'WHERE user2 = %s AND acceptStatus = %s'
    cursor.execute(friends_query, (username, 'Accepted', username, 'Accepted'))
    user_friends = cursor.fetchall()

    friend_request_query = 'SELECT user2 AS user FROM friend ' \
                           'WHERE user1 = %s AND requestSentBy != %s AND acceptStatus = %s ' \
                           'UNION SELECT user1 AS user FROM friend ' \
                           'WHERE user2 = %s AND requestSentBy != %s AND acceptStatus = %s'
    cursor.execute(friend_request_query, (username, username, 'Pending', username, username, 'Pending'))
    friend_request_result = cursor.fetchall()

    if request.method == 'POST':
        post_id = request.form['post_id']

        # search user to add friend
        if post_id == '1':
            username = request.form.get('username')
            if not username:
                flash('Username cannot be blank!', category='error')
                return render_template('friends.html', user=current_user, friends=user_friends,
                                       friend_request=friend_request_result)

            cursor = conn.cursor()
            query = 'SELECT username, fname, lname, nickname FROM user WHERE username = %s'
            cursor.execute(query, (username))
            users = cursor.fetchall()
            if users:
                return render_template('friends.html', users=users, user=current_user, friends=user_friends,
                                       friend_request=friend_request_result)
            else:
                flash('No user found! Please change the username!', category='error')

        # add/check friend
        elif post_id == '2':
            username = current_user.id
            friend = request.form['user_id']
            cursor = conn.cursor()
            query = 'SELECT user2 AS friend FROM friend ' \
                    'WHERE user1 = %s AND user2 = %s AND acceptStatus = %s ' \
                    'UNION ' \
                    'SELECT user1 AS friend FROM friend ' \
                    'WHERE user2 = %s AND user1 = %s AND acceptStatus = %s'
            cursor.execute(query, (username, friend, 'Accepted', username, friend, 'Accepted'))
            users = cursor.fetchall()

            if users:
                flash('You are already friends', 'error')
                return render_template('friends.html', user=current_user, friends=user_friends,
                                       friend_request=friend_request_result)
            else:
                # need to send a request, update database
                # add a feature to look at the request
                # if deny it, update the request
                # if accept it, update friend table and update follow table

                # check if already send the request
                check_request_exist = 'SELECT acceptStatus FROM friend ' \
                                      'WHERE user1 = %s AND user2 = %s AND requestSentBy = %s ' \
                                      'UNION SELECT acceptStatus FROM friend ' \
                                      'WHERE user1 = %s AND user2 = %s AND requestSentBy = %s'
                cursor.execute(check_request_exist, (username, friend, username, friend, username, username))
                status_result = cursor.fetchone()

                if status_result:
                    friend_status = status_result['acceptStatus']

                    if friend_status == 'Pending':
                        flash('You have already sent the friend request', 'error')
                        return render_template('friends.html', user=current_user, friends=user_friends,
                                               friend_request=friend_request_result)
                    elif friend_status == 'Denied':
                        # update status to Pending again
                        set_pending_request = 'UPDATE friend SET acceptStatus = %s, updatedAt = %s ' \
                                              'WHERE (friend.user1 = %s AND friend.user2 = %s) ' \
                                              'OR (friend.user1 = %s AND friend.user2 = %s)'
                        # update the status at current time
                        now = datetime.datetime.now()
                        formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
                        cursor.execute(set_pending_request,
                                       ('Pending', formatted_time, username, friend, friend, username))
                        conn.commit()
                        cursor.close()
                        flash('Friend request send successfully', 'success')
                        return render_template('friends.html', user=current_user, friends=user_friends,
                                               friend_request=friend_request_result)
                else:
                    # insert a new friend request
                    send_new_request = 'INSERT INTO friend VALUES(%s, %s, %s, %s, %s, NULL)'
                    now = datetime.datetime.now()
                    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute(send_new_request, (username, friend, 'Pending', username, formatted_time))
                    conn.commit()
                    cursor.close()
                    flash('Friend request send successfully', 'success')
                    return render_template('friends.html', user=current_user, friends=user_friends,
                                           friend_request=friend_request_result)

        # accept request
        elif post_id == '3':
            requestSentBy = request.form['RequestSendBy']

            # update status to become/deny friend request
            accept_request = 'UPDATE friend SET acceptStatus = %s, updatedAt = %s ' \
                             'WHERE (friend.user1 = %s AND friend.user2 = %s AND friend.requestSentBy = %s) ' \
                             'OR (friend.user1 = %s AND friend.user2 = %s AND friend.requestSentBy = %s)'
            now = datetime.datetime.now()
            formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(accept_request, (
            'Accepted', formatted_time, username, requestSentBy, requestSentBy, requestSentBy, username, requestSentBy))
            conn.commit()
            cursor.close()
            flash('You and ' + requestSentBy + ' are now friends!', 'success')

            cursor = conn.cursor()
            friends_query = 'SELECT user2 AS friend FROM friend ' \
                            'WHERE user1 = %s AND acceptStatus = %s ' \
                            'UNION SELECT user1 AS friend FROM friend ' \
                            'WHERE user2 = %s AND acceptStatus = %s'
            cursor.execute(friends_query, (username, 'Accepted', username, 'Accepted'))
            user_friends = cursor.fetchall()

            friend_request_query = 'SELECT user2 AS user FROM friend ' \
                                   'WHERE user1 = %s AND requestSentBy != %s AND acceptStatus = %s ' \
                                   'UNION SELECT user1 AS user FROM friend ' \
                                   'WHERE user2 = %s AND requestSentBy != %s AND acceptStatus = %s'
            cursor.execute(friend_request_query, (username, username, 'Pending', username, username, 'Pending'))
            friend_request_result = cursor.fetchall()

            return render_template('friends.html', user=current_user, friends=user_friends,
                                   friend_request=friend_request_result)

            # deny request
        elif post_id == '4':
            requestSentBy = request.form['RequestSendBy']

            # update status to become/deny friend request
            accept_request = 'UPDATE friend SET acceptStatus = %s, updatedAt = %s ' \
                             'WHERE (friend.user1 = %s AND friend.user2 = %s AND friend.requestSentBy = %s) ' \
                             'OR (friend.user1 = %s AND friend.user2 = %s AND friend.requestSentBy = %s)'
            now = datetime.datetime.now()
            formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(accept_request, ('Denied', formatted_time, username, requestSentBy, requestSentBy, requestSentBy, username, requestSentBy))
            conn.commit()
            cursor.close()
            flash('You have denied the friend request sent by ' + requestSentBy, 'warning')

            cursor = conn.cursor()
            friends_query = 'SELECT user2 AS friend FROM friend ' \
                            'WHERE user1 = %s AND acceptStatus = %s ' \
                            'UNION SELECT user1 AS friend FROM friend ' \
                            'WHERE user2 = %s AND acceptStatus = %s'
            cursor.execute(friends_query, (username, 'Accepted', username, 'Accepted'))
            user_friends = cursor.fetchall()

            friend_request_query = 'SELECT user2 AS user FROM friend ' \
                                   'WHERE user1 = %s AND requestSentBy != %s AND acceptStatus = %s ' \
                                   'UNION SELECT user1 AS user FROM friend ' \
                                   'WHERE user2 = %s AND requestSentBy != %s AND acceptStatus = %s'
            cursor.execute(friend_request_query, (username, username, 'Pending', username, username, 'Pending'))
            friend_request_result = cursor.fetchall()

            return render_template('friends.html', user=current_user, friends=user_friends, friend_request=friend_request_result)
    return render_template('friends.html', user=current_user, friends=user_friends, friend_request=friend_request_result)


@auth.route('/profile')
@login_required
def profile():
    username = current_user.id
    cursor = conn.cursor()
    query = 'SELECT username, fname, lname, nickname FROM user WHERE username = %s'
    cursor.execute(query, (username))
    user_profile = cursor.fetchone()
    friends_query = 'SELECT user2 AS friend FROM friend ' \
                    'WHERE user1 = %s AND acceptStatus = %s ' \
                    'UNION SELECT user1 AS friend FROM friend ' \
                    'WHERE user2 = %s AND acceptStatus = %s'
    cursor.execute(friends_query, (username, 'Accepted', username, 'Accepted'))
    user_friends = cursor.fetchall()
    query = 'SELECT follows FROM follows WHERE follower = %s'
    cursor.execute(query, (username))
    followings = cursor.fetchall()
    query = 'SELECT follower FROM follows WHERE follows = %s'
    cursor.execute(query, (username))
    followers = cursor.fetchall()
    return render_template('profile.html', profile=user_profile, friends=user_friends,
                           followings=followings, followers=followers, user=current_user)


@auth.route('/followers', methods=['GET', 'POST'])
@login_required
def followers():
    username = current_user.id
    cursor = conn.cursor()

    # query current followers and followings
    query = 'SELECT follows FROM follows WHERE follower = %s'
    cursor.execute(query, (username))
    followings = cursor.fetchall()
    query = 'SELECT follower FROM follows WHERE follows = %s'
    cursor.execute(query, (username))
    followers = cursor.fetchall()

    if request.method == 'POST':
        post_id = request.form['post_id']

        # search user to follow
        if post_id == '1':
            username = request.form.get('username')
            if not username:
                flash('Username cannot be blank!', category='error')
                return render_template('follower.html', user=current_user, followings=followings, followers=followers)

            cursor = conn.cursor()
            query = 'SELECT username, fname, lname, nickname FROM user WHERE username = %s'
            cursor.execute(query, (username))
            users = cursor.fetchall()
            if users:
                return render_template('follower.html', users=users, user=current_user, followings=followings,
                                       followers=followers)
            else:
                flash('No user found! Please change the username!', category='error')
        # follow users
        elif post_id == '2':
            follower = current_user.id
            followee = request.form['user_id']

            cursor = conn.cursor()
            query = 'SELECT follows FROM follows WHERE follower = %s AND follows = %s'
            cursor.execute(query, (follower, followee))
            users = cursor.fetchall()

            if users:
                flash('You have already followed this user', 'error')
                return render_template('follower.html', user=current_user, followings=followings, followers=followers)
            else:
                # the current day is the last time login for new user
                now = datetime.datetime.now()
                formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
                ins = 'INSERT INTO follows VALUES(%s, %s, %s)'
                cursor.execute(ins, (follower, followee, formatted_time))
                conn.commit()

                # reselect to display new results
                query = 'SELECT follows FROM follows WHERE follower = %s'
                cursor.execute(query, (username))
                followings = cursor.fetchall()
                cursor.close()
                flash('You are following ' + followee, 'success')

                return render_template('follower.html', user=current_user, followings=followings, followers=followers)

    return render_template('follower.html', user=current_user, followings=followings, followers=followers)
