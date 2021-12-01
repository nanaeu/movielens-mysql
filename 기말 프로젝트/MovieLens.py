import pymysql
import pandas as pd
import sys
import numpy as np
from PyQt5.QtWidgets import * #QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QComboBox
from PyQt5.QtCore import * #QCoreApplication, Qt
from PyQt5.QtGui import QIcon

conn = pymysql.connect(host='localhost', 
                       user='root', 
                       password='Lyjn6992^^', 
                       db='db_201812839')

curs = conn.cursor(pymysql.cursors.DictCursor)

# 파일 읽어오기
u_data = pd.read_csv("u.data.tsv", delimiter = '\t', encoding='iso-8859-1', header = None)
u_genre = pd.read_csv("u.genre.tsv", delimiter = '\t', encoding='iso-8859-1', header = None)
u_item = pd.read_csv("u.item.tsv", delimiter = '\t', encoding='iso-8859-1', header = None)
u_occ = pd.read_csv("u.occupation.tsv", delimiter = '\t', encoding='iso-8859-1', header = None)
u_user = pd.read_csv("u.user.tsv", delimiter = '\t', encoding='iso-8859-1', header = None)

# 각각 list로 만들기 
datalist = u_data.values.tolist()
for i in range(0, len(datalist)):
    datalist[i][0] = int(datalist[i][0])

genrelist = u_genre.values.tolist()

for i in range(0, 18):
    arr = genrelist[i][0].split('|')
    for j in range(0, len(arr)):
        genrelist[i].append(arr[j])
for i in range(0, 18):
    genrelist[i].remove(genrelist[i][0])
for i in range(0, 18):
    genrelist[i][1] = int(genrelist[i][1])

       
itemlist = u_item.values.tolist()

for i in range(0, len(itemlist)):
    arr = itemlist[i][0].split('|')
    for j in range(0, len(arr)):
        itemlist[i].append(arr[j])
for i in range(0, len(itemlist)):
    itemlist[i].remove(itemlist[i][0])
for i in range(0, len(itemlist)):
    for j in range(5,23):
        itemlist[i][j] = int(itemlist[i][j])
     

occlist = u_occ.values.tolist()

userlist = u_user.values.tolist()
for i in range(0, len(userlist)):
    arr = userlist[i][0].split('|')
    for j in range(0, len(arr)):
        userlist[i].append(arr[j])
for i in range(0, len(userlist)):
    userlist[i].remove(userlist[i][0])
for i in range(0, len(userlist)):
    userlist[i][0] = int(userlist[i][0])
    userlist[i][1] = int(userlist[i][1])


''' 데이터베이스 구축 '''
'''
# 1. M_User table insert
user_table = []
sql = "insert into M_User (user_id, age, gender, occupation, zipcode) values (%s, %s, %s, %s, %s)"
for i in range(0, len(userlist)):
    user_tuple = (userlist[i][0], userlist[i][1], userlist[i][2], userlist[i][3], userlist[i][4])
    user_table.append(user_tuple)
curs.executemany(sql, user_table)
conn.commit()

# 2. M_Movie table insert
movie_table = []
sql = "insert into M_Movie (movie_id, title, r_date, video_r_date, url) values (%s, %s, %s, %s, %s)"
for i in range(0, len(itemlist)):
    movie_tuple = (itemlist[i][0], itemlist[i][1], itemlist[i][2], itemlist[i][3], itemlist[i][4])
    movie_table.append(movie_tuple)
curs.executemany(sql, movie_table)
conn.commit()

# 3. Genre table insert
genre_table = []
sql = "insert into genre (movie_id, genre, genre_id) values (%s, %s, %s)"
for i in range(0, len(itemlist)):
    for j in range(5, 23):
        if itemlist[i][j] == 1:
            genre_tuple = (itemlist[i][0], genrelist[j-5][0], genrelist[j-5][1])
            genre_table.append(genre_tuple)
#        if itemlist[i][5] == 1:
#            genre_tuple = (itemlist[i][0], genrelist[0][0], genrelist[0][1])
#    genre_tuple = (itemlist[i][0], genrelist[i][0], genrelist[i][1])
curs.executemany(sql, genre_table)
conn.commit()



# 4. Rate table insert
rate_table = []
sql = "insert into rate (user_id, movie_id, rating, m_timestamp) values (%s, %s, %s, %s)"
for i in range(0, len(datalist)):
    rate_tuple = (datalist[i][0], datalist[i][1], datalist[i][2], datalist[i][3])
    rate_table.append(rate_tuple)
curs.executemany(sql, rate_table)
conn.commit()
'''

''' 검색 프로그램 만들기 '''
class MovieSearch(QMainWindow):
    
    
    def __init__(self):
        super().__init__()
        self.sgenre = QLabel(self)
        self.soccu = QLabel(self)
        self.smin = QLabel(self)
        self.smax = QLabel(self)
        self.ssort = QLabel(self)
        self.initUI()
    
    def initUI(self):
        # Icon
        self.setWindowIcon(QIcon('movie.png'))
        
        # Label
        self.genre = QLabel('장르 : ', self)
        self.genre.move(100, 60)
        genre_font = self.genre.font()
        genre_font.setPointSize(20)
        
        self.occu = QLabel('사용자의 직업 : ', self)
        self.occu.move(36, 100)
        occu_font = self.occu.font()
        occu_font.setPointSize(20)
        
        self.rating = QLabel('평점', self)
        self.rating.move(50, 140)
        rating_font = self.rating.font()
        rating_font.setPointSize(20)
        
        self.min_rate = QLabel('MIN : ', self)
        self.min_rate.move(110, 140)
        min_font = self.min_rate.font()
        min_font.setPointSize(20)
        
        self.max_rate = QLabel('MAX : ', self)
        self.max_rate.move(500,140)
        max_font = self.max_rate.font()
        max_font.setPointSize(20)
        
        self.sorting = QLabel('Sorting by :', self)
        self.sorting.move(65,180)
        sort_font = self.sorting.font()
        sort_font.setPointSize(20)
        
        
        # Line Edit 
        min_line = QLineEdit(self)
        min_line.move(150, 140)
        min_line.textChanged[str].connect(self.getText_min)

        max_line = QLineEdit(self)
        max_line.move(550, 140)
        max_line.textChanged[str].connect(self.getText_max)
        
        
        # Give Options
        genre_cb = QComboBox(self)
        genre_cb.addItem('None')
        for i in range(0, len(genrelist)):
            genre_cb.addItem(genrelist[i][0])
        genre_cb.move(150, 60)
        genre_cb.activated[str].connect(self.getText_genre)
        
        occu_cb = QComboBox(self)
        occu_cb.addItem('None')
        for i in range(0, len(occlist)):
            occu_cb.addItem(occlist[i][0])
        occu_cb.move(150, 100)
        occu_cb.activated[str].connect(self.getText_occu)
        
        sort_cb = QComboBox(self)
        sort_cb.addItem('None')
        sort_cb.addItem('Title')
        sort_cb.addItem('Average Rate')
        sort_cb.addItem('Vote')
        sort_cb.move(150, 180)
        sort_cb.activated[str].connect(self.getText_sort)
        
        btn = QPushButton('Search Movie', self)
        btn.setCheckable(True)
        btn.move(390, 250)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.filtering)
        
        self.setWindowTitle('Movielens - Search Movie (201812839 이유진)')
        self.move(800, 300)
        self.resize(800, 300)
        self.show()
        
    def getText_genre(self, text):
        #self.genre.setText(text)
        #self.genre.adjustSize()
        #self.sgenre = QLabel(self)
        self.sgenre.setText(text)
    
    def getText_occu(self, text):
        #self.occu.setText(text)
        #self.occu.adjustSize()
        #self.soccu = QLabel(self)
        self.soccu.setText(text)
    
    def getText_min(self, text):
        #self.min_rate.setText(text)
        #self.min_rate.adjustSize()
        #self.smin = QLabel(self)
        self.smin.setText(text)
                   
    def getText_max(self, text):
        #self.max_rate.setText(text)
        #self.max_rate.adjustSize()
        #self.smax = QLabel(self)
        self.smax.setText(text)
    
    def getText_sort(self, text):
        #self.sorting.setText(text)
        #self.sorting.adjustSize()
        #self.ssort = QLabel(self)
        self.ssort.setText(text)
    
    def filtering(self):
        
        str_g = self.sgenre.text()
        str_o = self.soccu.text()
        str_sort = self.ssort.text()
        
        rg_table = []
        ro_table = []
        mid = []
        count = 0
        if str_g != "None":
            sql = "select m.movie_id, m.title from M_Movie m left join genre g on g.movie_id = m.movie_id where g.genre = '%s' " %(str_g)
            curs.execute(sql)
            conn.commit()
            count = 0
            row = curs.fetchone()
            while(row):
                rg_tuple = (row['movie_id'], row['title'], str_g)
                rg_table.append(rg_tuple)
                count += 1
                row = curs.fetchone()
            if self.soccu.text() != "None": # Rating과 관련있음
                if self.smin.text() == '' and self.smax.text() == '':
                    #for i in range(len(rg_table)):
                    sql = "select g.movie_id from genre g where g.genre = '%s' " %(str_g)
                    curs.execute(sql)
                    conn.commit()
                    index = 0
                    row = curs.fetchone()
                    while(row):
                        mid.append(row['movie_id'])
                        index += 1
                        row = curs.fetchone()
                    
                    for i in range(0, index):
                        sql = "select avg(r.rating), count(*) as vote_count from rate r left join M_User u on u.user_id = r.user_id where r.movie_id = '%d' and u.occupation = '%s' " %(mid[i], str_o)
                        
                        curs.execute(sql)
                        conn.commit()
                
                        row = curs.fetchone()
                        while(row):
                            ro_tuple = (row['avg(r.rating)'], row['vote_count'])
                            ro_table.append(ro_tuple)
                            row = curs.fetchone()

                else: # Error...
                    if self.smin.text() == '':
                        self.smin.setText('-99')
                    elif self.smax.text() == '':
                        self.smax.setText('99')
                    sql = "select g.movie_id from genre g where g.genre = '%s' " %(str_g)
                    curs.execute(sql)
                    conn.commit()
                    index = 0
                    row = curs.fetchone()
                    while(row):
                        mid.append(row['movie_id'])
                        index += 1
                        row = curs.fetchone()
                    
                    for i in range(len(rg_table)):
                        sql = "select r.movie_id, avg(r.rating), count(*) as vote_count from rate r left join M_User u on u.user_id = r.user_id where r.movie_id = '%d' and u.occupation = '%s' and r.rating >= '%f' and r.rating <= '%f' "%(mid[i], str_o, float(self.smin.text()), float(self.smax.text()))
                        curs.execute(sql)
                        conn.commit()
                        
                        row = curs.fetchone()
                        while(row):
                            ro_tuple = (row['avg(r.rating)'], row['vote_count'])
                            ro_table.append(ro_tuple)
                            row = curs.fetchone()

            
            else:
                if self.smin.text() == '' and self.smax.text() == '':
                    self.smin.setText('-99')
                    self.smax.setText('99')
                    sql = "select g.movie_id from genre g where g.genre = '%s' " %(str_g)
                    curs.execute(sql)
                    conn.commit()
                    index = 0
                    row = curs.fetchone()
                    while(row):
                        mid.append(row['movie_id'])
                        index += 1
                        row = curs.fetchone()
                    for i in range(0, index):
                        sql = "select r.movie_id, avg(r.rating), count(*) as vote_count from rate r left join M_User u on u.user_id = r.user_id where r.movie_id  = '%d' "%(mid[i])
                        curs.execute(sql)
                        conn.commit()
                        
                        row = curs.fetchone()
                        while(row):
                            ro_tuple = (row['avg(r.rating)'], row['vote_count'])
                            ro_table.append(ro_tuple)
                            row = curs.fetchone()

                else:
                    if self.smin.text() == '':
                        self.smin.setText('-99')
                    elif self.smax.text() == '':
                        self.smax.setText('99')
                    sql = "select g.movie_id from genre g where g.genre = '%s' " %(str_g)
                    curs.execute(sql)
                    conn.commit()
                    index = 0
                    row = curs.fetchone()
                    while(row):
                        mid.append(row['movie_id'])
                        index += 1
                        row = curs.fetchone()
                    for i in range(0, index):
                        sql = "select r.movie_id, avg(r.rating), count(*) as vote_count from rate r left join M_User u on u.user_id = r.user_id where r.movie_id = '%d' and r.rating >= '%f' and r.rating <= '%f' "%(mid[i], float(self.smin.text()), float(self.smax.text()))
                        curs.execute(sql)
                        conn.commit()
                            
                        row = curs.fetchone()
                        while(row):
                            ro_tuple = (row['avg(r.rating)'], row['vote_count'])
                            ro_table.append(ro_tuple)
                            row = curs.fetchone()

            
        elif str_g == "None":
            sql = "select m.movie_id, m.title, g.genre from M_Movie m left join genre g on g.movie_id = m.movie_id"
            curs.execute(sql)
            conn.commit()
            count = 0
            row = curs.fetchone()
            while(row):
                rg_tuple = (row['movie_id'], row['title'], row['genre'])
                rg_table.append(rg_tuple)
                count += 1
                row = curs.fetchone()
            if self.soccu.text() != "None": # Rating과 관련있음
                if self.smin.text() == '' and self.smax.text() == '':
                    #for i in range(len(rg_table)):
                    sql = "select g.movie_id from genre g where g.genre = '%s' " %(str_g)
                    curs.execute(sql)
                    conn.commit()
                    index = 0
                    row = curs.fetchone()
                    while(row):
                        mid.append(row['movie_id'])
                        index += 1
                        row = curs.fetchone()
                    
                    for i in range(0, index):
                        sql = "select avg(r.rating), count(*) as vote_count from rate r left join M_User u on u.user_id = r.user_id where r.movie_id = '%d' and u.occupation = '%s' " %(mid[i], str_o)
                        
                        curs.execute(sql)
                        conn.commit()
                            
                        row = curs.fetchone()
                        while(row):
                            ro_tuple = (row['avg(r.rating)'], row['vote_count'])
                            ro_table.append(ro_tuple)
                            row = curs.fetchone()

                else: # Error...
                    if self.smin.text() == '':
                        self.smin.setText('-99')
                    elif self.smax.text() == '':
                        self.smax.setText('99')
                    sql = "select g.movie_id from genre g where g.genre = '%s' " %(str_g)
                    curs.execute(sql)
                    conn.commit()
                    index = 0
                    row = curs.fetchone()
                    while(row):
                        mid.append(row['movie_id'])
                        index += 1
                        row = curs.fetchone()
                        
                    for i in range(0, index):
                        sql = "select r.movie_id, avg(r.rating), count(*) as vote_count from rate r left join M_User u on u.user_id = r.user_id where r.movie_id = '%d' and u.occupation = '%s' and r.rating >= '%f' and r.rating <= '%f' "%(mid[i], str_o, float(self.smin.text()), float(self.smax.text()))
                        curs.execute(sql)
                        conn.commit()
                            
                        row = curs.fetchone()
                        while(row):
                            ro_tuple = (row['avg(r.rating)'], row['vote_count'])
                            ro_table.append(ro_tuple)
                            row = curs.fetchone()

            
            else:
                if self.smin.text() == '' and self.smax.text() == '':
                    self.smin.setText('-99')
                    self.smax.setText('99')
                    sql = "select g.movie_id from genre g where g.genre = '%s' " %(str_g)
                    curs.execute(sql)
                    conn.commit()
                    index = 0
                    row = curs.fetchone()
                    while(row):
                        mid.append(row['movie_id'])
                        index += 1
                        row = curs.fetchone()
                    for i in range(0, index):
                        sql = "select r.movie_id, avg(r.rating), count(*) as vote_count from rate r left join M_User u on u.user_id = r.user_id where r.movie_id  = '%d' "%(mid[i])
                        curs.execute(sql)
                        conn.commit()
                        
                        row = curs.fetchone()
                        while(row):
                            ro_tuple = (row['avg(r.rating)'], row['vote_count'])
                            ro_table.append(ro_tuple)
                            row = curs.fetchone()

                else:
                    if self.smin.text() == '':
                        self.smin.setText('-99')
                    elif self.smax.text() == '':
                        self.smax.setText('99')
                    sql = "select g.movie_id from genre g where g.genre = '%s' " %(str_g)
                    curs.execute(sql)
                    conn.commit()
                    index = 0
                    row = curs.fetchone()
                    while(row):
                        mid.append(row['movie_id'])
                        index += 1
                        row = curs.fetchone()
                    for i in range(0, index):
                        sql = "select r.movie_id, avg(r.rating), count(*) as vote_count from rate r left join M_User u on u.user_id = r.user_id where r.movie_id = '%d' and r.rating >= '%f' and r.rating <= '%f' "%(mid[i], float(self.smin.text()), float(self.smax.text()))
                        curs.execute(sql)
                        conn.commit()
                            
                        row = curs.fetchone()
                        while(row):
                            ro_tuple = (row['avg(r.rating)'], row['vote_count'])
                            ro_table.append(ro_tuple)
                            row = curs.fetchone()

            
                
        
        result_table = []
        for i in range(0, len(rg_table)):
            result_tuple = (rg_table[i][0], rg_table[i][1], rg_table[i][2], ro_table[i][0], ro_table[i][1])
            result_table.append(result_tuple)
        
        # Sorting
        if self.ssort.text() == "Title": # ok
            result_table.sort(key = lambda x:x[1])
            print('sort done - title\n')
        elif self.ssort.text() == "Average Rate": 
            result_table.sort(key = lambda x:x[3], reverse = True)
            print('sort done - avg rate\n')
        elif self.ssort.text() == "Vote": 
            result_table.sort(key = lambda x:x[4], reverse = True)
            print('sort done - vote\n')
        
        for i in range(0, len(result_table)):
            print('[영화 ID : %s, 제목 : %s, 장르 : %s, 평균평점 : %f, Vote 수 : %d' %(result_table[i][0], result_table[i][1], result_table[i][2], result_table[i][3], result_table[i][4]) )
            print('\n')
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MovieSearch()
    sys.exit(app.exec_())




