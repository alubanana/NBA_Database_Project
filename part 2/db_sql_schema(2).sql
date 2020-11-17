/* create table for entity news */
create table News(
	news_id varchar(16),
	news_title text,
	new_content text,
	news_date date,
	primary key (news_id)
	);

/* create table for many-to-many relationship of news related to players */
create table News_to_Players(
	news_id varchar(16),
	player_id varchar(16),
	primary key (news_id,player_id),
	foreign key (player_id) references Players,
	foreign key (news_id) references News
	);

/* create table for entity players */
create table Players(
	player_id varchar(16),
	player_name varchar(40),
	team_name varchar(40) not null,/* every player should has a team */
	player_position varchar(8),
	height numeric(8,2),
	weight numeric(8,2),
	block numeric(8,2),
	rebounds numeric(8,2),
	assists numeric(8,2),
	steals numeric(8,2),
	twopoint_shot_percentage numeric(8,2),
	threepoint_shot_percentage numeric(8,2),
	start_year numeric(4,0) check (start_year>1950 and start_year<2100),
	salary numeric(16,2),
	primary key (player_id)
	);

create table Players_to_Team(
	player_id varchar(16),
	team_name varchar(40),
	primary key player_id,
	foreign key (team_name) references Teams,
	foreign key (player_id) references Players
	);


/* create table for entity players */
create table Teams
(
	team_name varchar(40),
	found_year numeric(4,0) check (found_year>1900 and found_year<2100),
	city varchar(40),
	state varchar(40),
	primary key (team_name)
	);

/* create table for entity coaches */
create table Coaches(
	coach_id varchar(16),
	coach_name varchar(40),
	start_year numeric(4,0) check (start_year>1900 and start_year<2100),
	number_of_champs int check (number_of_champs>=0),
	primary key (coach_id)
	);

create table Coach_to_Team(
	team_name varchar(40),
	coach_id varchar(16) not null,
	primary key (team_name),
	foreign key (coach_id) references Coaches, unique(coach_id),
	foreign key (team_name) references Teams
	);

/* create table for entity stadiums */
create table Stadiums
(
	stadium_name varchar(40),
	size numeric(8,0),
	stadium_location varchar(40) not null,
	primary key (stadium_name)
	);

create table Stadium_to_team(
	stadium_name varchar(40) not null,
	team_name varchar(40),
	primary key (team_name),
	foreign key (stadium_name) references Stadiums,
	foreign key (team_name) references Teams
	);

/* create table for entity games */
create table Games
(
	game_id varchar(16),
	game_date date,
	stadium_name varchar(20),
	final_margin int,
	winner char(4) check (winner in ('home','away')),
	primary key (game_id)
	);


create table Game_to_Team(
	game_id varchar(16),
	home_team_name varchar(40) not null,
	away_team_name varchar(40) not null, 
	primary key (game_id),
	foreign key (game_id) references Games,
	foreign key (home_team_name) references Teams,
	foreign key (away_team_name) references Teams
	);

create table Shots
(
	shot_id varchar(16),
	shot_distance numeric(8,2),
	time_clock numeric(8,2) check (time_clock>=0 and time_clock<=24) , /
	shot_result boolean,
	quarter numeric(1,0) check (quarter in (1,2,3,4,6,7,8,9)),
	primary key (shot_id)
	);


create table Shot_to_Player(
	shot_id varchar(16),
	shooter_id varchar(16) not null,
	defender_id varchar(16) not null,
	defender_distance numeric(8,2),
	primary key (shot_id),
	foreign key (shot_id) references Shots,
	foreign key (shooter_id) references Players,
	foreign key (defender_id) references Players
	);

create table Shot_to_Game(
	shot_id varchar(16),
	game_id varchar(16) not null, 
	primary key (shot_id),
	foreign key (game_id) references Games,
	foreign key (shot_id) references Shots
	);
