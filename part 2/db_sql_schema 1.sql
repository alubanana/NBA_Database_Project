/* create table for entity news */
create table News(
	news_id varchar(16),
	news_title varchar(64),
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
	player_name varchar(20),
	team_name varchar(20) not null,/* every player should has a team */
	player_position varchar(8),
	height numeric(8,2),
	weight numeric(8,2),
	block numeric(8,2),
	rebounds numeric(8,2),
	assists numeric(8,2),
	steals numeric(8,2),
	twopoint_shot_percentage numeric(8,2),
	threepoint_shot_percentage numeric(8,2),
	start_year numeric(4,0) check (start_year>1950 and start_year<2100), /* the start year of players' careers should in this interval */
	salary numeric(8,2),
	primary key (player_id)
	);

create table Players_to_Team(
	player_id varchar(16),
	team_name varchar(20),
	primary key player_id,
	foreign key (team_name) references Teams,
	foreign key (player_id) references Players
	);


/* create table for entity players */
create table Teams
(
	team_name varchar(20),
	found_year numeric(4,0) check (found_year>1900 and found_year<2100),
	city varchar(16),
	manager varchar(20),
	primary key (team_name)
	);

/* create table for entity coaches */
create table Coaches(
	coach_id varchar(16),
	coach_name varchar(16),
	start_year numeric(4,0) check (start_year>1900 and start_year<2100),/* the start year of coaches' careers should in this interval */
	number_of_champs int check (number_of_champs>=0),/* the number of championship should be positive */
	primary key (coach_id)
	);


create table Coach_to_Team(
	team_name varchar(20),
	coach_id varchar(16) not null,
	primary key (team_name),
	foreign key (coach_id) references Coaches, unique(coach_id),
	foreign key (team_name) references Teams
	);

/* create table for entity stadiums */
create table Stadiums
(
	stadium_name varchar(20),
	size numeric(8,0),
	stadium_location varchar(20) not null,
	primary key (stadium_name)
	);

create table Stadium_to_team(
	stadium_name varchar(20) not null,
	team_name varchar(20),
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
	result_score varchar(20),
	winner char(4) check (winner in ('home','away')),
	primary key (game_id)
	);


create table Game_to_Team(
	game_id varchar(16),
	home_team_name varchar(20) not null,
	away_team_name varchar(20) not null, 
	primary key (game_id),
	foreign key (game_id) references Games,
	foreign key (home_team_name) references Teams,
	foreign key (away_team_name) references Teams
	);

create table Shots
(
	shot_id varchar(16),/* represent a full participation of shooter and player_id, which indicates that every shots should has a shooter */
	shot_distance numeric(8,2),
	time_clock int check (time_clock>=0 and time_clock<=24) , /* shots clock should be integer between 0 to 24*/
	shot_result boolean,
	quarter numeric(1,0) check (quarter in (1,2,3,4)),/* there are only 4 quarters*/
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

/* One of the constraints we have not yet covered is that the team of the shooter/defender should be one of the home team or away team of the game that the shot is related. 
Similarly, Another constraint that we have not yet covered is that the stadium of a game should be indentical to the stadium of the home team.*/
