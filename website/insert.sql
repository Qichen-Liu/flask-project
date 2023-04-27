INSERT INTO `user` (`username`, `pwd`, `fname`, `lname`, `lastlogin`, `nickname`) VALUES ('aw2222', '123yxw', 'Yuxuan', 'Wuu', '2022-02-11', 'Awuu');
INSERT INTO `user` (`username`, `pwd`, `fname`, `lname`, `lastlogin`, `nickname`) VALUES ('ql2326', '123lqc', 'Qichen', 'Liu', '2023-03-01', 'Mike');
INSERT INTO `user` (`username`, `pwd`, `fname`, `lname`, `lastlogin`, `nickname`) VALUES ('rl1832', '123rqg', 'Renqiuguo', 'Li', '2023-03-13', 'Guoguo');
INSERT INTO `user` (`username`, `pwd`, `fname`, `lname`, `lastlogin`, `nickname`) VALUES ('yw1123', '123yfw', 'Yifan', 'Wu', '2023-02-11', 'Eden');
INSERT INTO `user` (`username`, `pwd`, `fname`, `lname`, `lastlogin`, `nickname`) VALUES ('zw3451', '123ztw', 'Zetao', 'Wang', '2023-03-11', 'Gusi');

INSERT INTO `song` (`songID`, `title`, `releaseDate`, `songURL`) VALUES ('1', 'Sugar', '2019-08-12', 'https://www.youtube.com/watch?v=09R8_2nJtjg');
INSERT INTO `song` (`songID`, `title`, `releaseDate`, `songURL`) VALUES ('2', 'Believer', '2018-03-12', 'https://www.youtube.com/watch?v=oppaw2J32ow');
INSERT INTO `song` (`songID`, `title`, `releaseDate`, `songURL`) VALUES ('3', 'SINS', '2022-09-14', 'https://www.youtube.com/watch?v=hvNbMrUNtuc');
INSERT INTO `song` (`songID`, `title`, `releaseDate`, `songURL`) VALUES ('4', 'Peaches', '2021-09-14', 'https://www.youtube.com/watch?v=BydBU2pCkU8');
INSERT INTO `song` (`songID`, `title`, `releaseDate`, `songURL`) VALUES ('5', 'TesterForJazz', NULL, NULL);
INSERT INTO `song` (`songID`, `title`, `releaseDate`, `songURL`) VALUES ('6', 'JazzTester2', NULL, NULL);

INSERT INTO `artist` (`artistID`, `fname`, `lname`, `artistBio`, `artistURL`) VALUES ('123', 'Red', 'Leather', 'This is red leather bio', 'https://pianity.com/red-leather');
INSERT INTO `artist` (`artistID`, `fname`, `lname`, `artistBio`, `artistURL`) VALUES ('234', 'Imagine', 'Dragons', 'This is Imagon Dragons bio', 'https://www.imaginedragonsmusic.com/#/');
INSERT INTO `artist` (`artistID`, `fname`, `lname`, `artistBio`, `artistURL`) VALUES ('345', 'The', 'Archies', 'This is The Archies bio', 'https://en.wikipedia.org/wiki/The_Archies');
INSERT INTO `artist` (`artistID`, `fname`, `lname`, `artistBio`, `artistURL`) VALUES ('567', 'Justin', 'Bieber', 'This is Justin Bieber bio', 'https://www.justinbiebermusic.com/');
INSERT INTO `artist` (`artistID`, `fname`, `lname`, `artistBio`, `artistURL`) VALUES ('789', 'Test', 'Tester', 'This is a test for question 6', NULL);

INSERT INTO `artistPerformsSong` (`artistID`, `songID`) VALUES ('123', '1');
INSERT INTO `artistPerformsSong` (`artistID`, `songID`) VALUES ('234', '2');
INSERT INTO `artistPerformsSong` (`artistID`, `songID`) VALUES ('345', '3');
INSERT INTO `artistPerformsSong` (`artistID`, `songID`) VALUES ('567', '4');
INSERT INTO `artistPerformsSong` (`artistID`, `songID`) VALUES ('789', '5');
INSERT INTO `artistPerformsSong` (`artistID`, `songID`) VALUES ('789', '6');

INSERT INTO `album` (`albumID`) VALUES ('111');
INSERT INTO `album` (`albumID`) VALUES ('222');
INSERT INTO `album` (`albumID`) VALUES ('333');
INSERT INTO `album` (`albumID`) VALUES ('444');

INSERT INTO `follows` (`follower`, `follows`, `createdAt`) VALUES ('ql2326', 'zw3451', '2022-09-01 09:42:40');
INSERT INTO `follows` (`follower`, `follows`, `createdAt`) VALUES ('zw3451', 'ql2326', '2022-09-01 09:42:40');
INSERT INTO `follows` (`follower`, `follows`, `createdAt`) VALUES ('yw1123', 'aw2222', '2023-02-12 09:44:11');
INSERT INTO `follows` (`follower`, `follows`, `createdAt`) VALUES ('ql2326', 'aw2222', '2023-03-20 10:37:00');
INSERT INTO `follows` (`follower`, `follows`, `createdAt`) VALUES ('ql2326', 'yw1123', NULL);
INSERT INTO `follows` (`follower`, `follows`, `createdAt`) VALUES ('ql2326', 'rl1832', NULL);
INSERT INTO `follows` (`follower`, `follows`, `createdAt`) VALUES ('rl1832', 'ql2326', NULL);

INSERT INTO `friend` (`user1`, `user2`, `acceptStatus`, `requestSentBy`, `createdAt`, `updatedAt`) VALUES ('ql2326', 'zw3451', 'Accepted', 'ql2326', '2022-09-01 09:44:42', '2022-09-10 05:44:42');
INSERT INTO `friend` (`user1`, `user2`, `acceptStatus`, `requestSentBy`, `createdAt`, `updatedAt`) VALUES ('aw2222', 'ql2326', 'Pending', 'ql2326', '2023-03-13 09:45:53', NULL);
INSERT INTO `friend` (`user1`, `user2`, `acceptStatus`, `requestSentBy`, `createdAt`, `updatedAt`) VALUES ('rl1832', 'yw1123', 'Denied', 'yw1123', '2022-11-14 09:46:21', '2022-11-18 01:14:21');
INSERT INTO `friend` (`user1`, `user2`, `acceptStatus`, `requestSentBy`, `createdAt`, `updatedAt`) VALUES ('ql2326', 'rl1832', 'Accepted', 'ql2326', '2023-03-02 10:30:47', '2023-03-04 10:30:47');
INSERT INTO `friend` (`user1`, `user2`, `acceptStatus`, `requestSentBy`, `createdAt`, `updatedAt`) VALUES ('yw1123', 'ql2326', 'Accepted', 'yw1123', '2023-03-13 10:33:38', NULL);
INSERT INTO `friend` (`user1`, `user2`, `acceptStatus`, `requestSentBy`, `createdAt`, `updatedAt`) VALUES ('rl1832', 'ql2326', 'Pending', 'ql2326', '2023-03-14 10:55:58', NULL);

INSERT INTO `rateAlbum` (`username`, `albumID`, `stars`) VALUES ('ql2326', '111', '5');
INSERT INTO `rateAlbum` (`username`, `albumID`, `stars`) VALUES ('ql2326', '444', '3');
INSERT INTO `rateAlbum` (`username`, `albumID`, `stars`) VALUES ('aw2222', '222', '1');
INSERT INTO `rateAlbum` (`username`, `albumID`, `stars`) VALUES ('rl1832', '222', '4');
INSERT INTO `rateAlbum` (`username`, `albumID`, `stars`) VALUES ('zw3451', '111', '2');
INSERT INTO `rateAlbum` (`username`, `albumID`, `stars`) VALUES ('zw3451', '333', '4');

INSERT INTO `rateSong` (`username`, `songID`, `stars`, `ratingDate`) VALUES ('ql2326', '1', '5', '2023-03-13');
INSERT INTO `rateSong` (`username`, `songID`, `stars`, `ratingDate`) VALUES ('ql2326', '4', '5', '2022-11-06');
INSERT INTO `rateSong` (`username`, `songID`, `stars`, `ratingDate`) VALUES ('aw2222', '2', '1', '2023-01-16');
INSERT INTO `rateSong` (`username`, `songID`, `stars`, `ratingDate`) VALUES ('yw1123', '3', '3', '2022-11-21');
INSERT INTO `rateSong` (`username`, `songID`, `stars`, `ratingDate`) VALUES ('zw3451', '1', '3', '2022-12-12');
INSERT INTO `rateSong` (`username`, `songID`, `stars`, `ratingDate`) VALUES ('yw1123', '2', '4', '2023-03-21');
INSERT INTO `rateSong` (`username`, `songID`, `stars`, `ratingDate`) VALUES ('zw3451', '5', '4', '2023-03-21');
INSERT INTO `rateSong` (`username`, `songID`, `stars`, `ratingDate`) VALUES ('ql2326', '5', '2', '2023-03-22');
INSERT INTO `rateSong` (`username`, `songID`, `stars`, `ratingDate`) VALUES ('ql2326', '6', '5', NULL);
INSERT INTO `rateSong` (`username`, `songID`, `stars`, `ratingDate`) VALUES ('zw3451', '6', '5', NULL);

INSERT INTO `reviewAlbum` (`username`, `albumID`, `reviewText`, `reviewDate`) VALUES ('ql2326', '111', 'Good', '2023-03-22');
INSERT INTO `reviewAlbum` (`username`, `albumID`, `reviewText`, `reviewDate`) VALUES ('ql2326', '222', 'Relex', '2023-02-22');
INSERT INTO `reviewAlbum` (`username`, `albumID`, `reviewText`, `reviewDate`) VALUES ('aw2222', '222', 'Bad song!', '2023-01-08');
INSERT INTO `reviewAlbum` (`username`, `albumID`, `reviewText`, `reviewDate`) VALUES ('aw2222', '333', 'I do not like the artist but the album is ok.', '2023-01-29');
INSERT INTO `reviewAlbum` (`username`, `albumID`, `reviewText`, `reviewDate`) VALUES ('zw3451', '222', 'I like it', '2023-03-04');

INSERT INTO `reviewSong` (`username`, `songID`, `reviewText`, `reviewDate`) VALUES ('ql2326', '1', 'I love it so much', '2023-03-22');
INSERT INTO `reviewSong` (`username`, `songID`, `reviewText`, `reviewDate`) VALUES ('zw3451', '4', 'A good song to listen to on a road trip', '2023-03-12');
INSERT INTO `reviewSong` (`username`, `songID`, `reviewText`, `reviewDate`) VALUES ('aw2222', '4', 'Make me feel relax', '2023-01-02');

INSERT INTO `songGenre` (`songID`, `genre`) VALUES ('1', 'pop');
INSERT INTO `songGenre` (`songID`, `genre`) VALUES ('2', 'rock');
INSERT INTO `songGenre` (`songID`, `genre`) VALUES ('3', 'dance');
INSERT INTO `songGenre` (`songID`, `genre`) VALUES ('4', 'pop');
INSERT INTO `songGenre` (`songID`, `genre`) VALUES ('5', 'Jazz music');
INSERT INTO `songGenre` (`songID`, `genre`) VALUES ('6', 'Jazz');

INSERT INTO `songInAlbum` (`albumID`, `songID`) VALUES ('111', '1');
INSERT INTO `songInAlbum` (`albumID`, `songID`) VALUES ('222', '2');
INSERT INTO `songInAlbum` (`albumID`, `songID`) VALUES ('333', '3');
INSERT INTO `songInAlbum` (`albumID`, `songID`) VALUES ('444', '4');

INSERT INTO `userFanOfArtist` (`username`, `artistID`) VALUES ('ql2326', '345');
INSERT INTO `userFanOfArtist` (`username`, `artistID`) VALUES ('aw2222', '123');
INSERT INTO `userFanOfArtist` (`username`, `artistID`) VALUES ('yw1123', '123');
INSERT INTO `userFanOfArtist` (`username`, `artistID`) VALUES ('zw3451', '567');
INSERT INTO `userFanOfArtist` (`username`, `artistID`) VALUES ('rl1832', '345');


INSERT INTO `songInPlaylist` (`listID`, `songID`) VALUES ('101', '3');

INSERT INTO `playlist` (`listID`, `listName`, `createdAt`, `createdBy`) VALUES ('102', 'road', '2023-02-12 09:44:11', 'ql2326');
INSERT INTO `playlist` (`listID`, `listName`, `createdAt`, `createdBy`) VALUES ('101', 'my favorite', '2023-04-27 16:23:09', 'ql2326');