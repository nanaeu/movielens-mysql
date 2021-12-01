create database db_201812839;
use db_201812839;

create table M_User(
	user_id int primary key,
    age int,
    gender varchar(1) not null,
    occupation varchar(20),
    zipcode varchar(10) not null,
	enter_date datetime default now()
    on update now()
);

create table M_Movie(
	movie_id integer primary key,
    title varchar(100) not null,
    r_date varchar(20),
    video_r_date varchar(12),
	url varchar(150),
    enter_date datetime default now()
    on update now()
);

create table rate(
	user_id integer,
    movie_id integer,
    rating integer,
    m_timestamp int,
    enter_date datetime default now()
    on update now(),
    
    primary key(user_id, movie_id),
    foreign key(user_id) references M_User(user_id)
    on update cascade
    on delete cascade,
    foreign key(movie_id) references M_Movie(movie_id)
    on update cascade
    on delete cascade,
    check(rating >=1 and rating <= 5)
);

create table genre(
	movie_id int not null,
	genre varchar(20),
    genre_id int,
    primary key(movie_id, genre_id),
    foreign key(movie_id) references M_Movie(movie_id)
);


select *
from M_User;

select count(*) as user_count
from M_User;

select *
from M_Movie;

select count(*) as movie_count
from M_Movie;

select *
from genre;

select *
from rate;

select count(*) as rate_count
from rate;

select count(*) as v_count
from rate
where rating = 4;

select r.movie_id, avg(r.rating), count(*) as vote_count 
from rate r left join M_User u 
on u.user_id = r.user_id 
where r.movie_id in (select m.movie_id from M_Movie m left join genre g on m.movie_id = g.movie_id where g.genre = "Action") and /*u.occupation = "administrator" and*/ r.rating >= 4 and r.rating <=5;


select * 
from M_Movie 
order by title;

select * 
from M_Movie m left join rate r 
on m.movie_id = r.movie_id 
order by avg(rating);

select *
from rate;

/*장르가 정해졌을 때 해당 영화 평점평균과 vote 수*/
select r.movie_id, avg(r.rating), count(*) as vote_count
from rate r left join M_User u
on u.user_id = r.user_id
where r.movie_id in (select m.movie_id 
				from M_Movie m left join genre g 
				on m.movie_id = g.movie_id 
                where g.genre = "Action");

select *
from M_Movie;

/*직업을 알 때*/

/*해당 영화에 대한 평점평균과 vote 수*/
select r.movie_id, avg(r.rating), count(*) as vote_count
from rate r left join M_User u
on r.user_id = u.user_id
where r.movie_id in (select m.movie_id from M_Movie m where m.title = "Toy Story (1995)") and u.occupation = "doctor" and r.rating >= 1 and r.rating <= 5;

select r.movie_id, avg(r.rating), count(*) as vote_count 
from rate r left join M_User u 
on u.user_id = r.user_id 
where r.movie_id in (select m.movie_id from M_Movie m where m.title = 'Toy Story (1995)') 
		and u.occupation = 'doctor' and r.rating >= 2 and r.rating <= 3; 

select g.movie_id from genre g where g.genre = "Thriller";

select r.movie_id /*, avg(r.rating), count(r.rating) as vote_count */
from rate r left join M_User u 
on u.user_id = r.user_id 
where r.movie_id in (select g.movie_id from genre g where g.genre = "Thriller");

select *
from rate r left join M_User u
on u.user_id = r.user_id;

/*and u.occupation = "doctor";*/




