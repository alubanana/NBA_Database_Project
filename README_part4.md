Team number:36
Team members:
<li> Annan Chen ac4619
<li> Jiepeng Lian jl5521

PostgreSQL account name: jl5521 PGPASSWORD=6447 psql -U jl5521 -h 35.231.103.173 -d proj1part2


Part 4 of our NBA project includes the following updates:

1. Add text type attributes "description" to table Teams, which contains the introduction to this team and some other basic infomation,
allowing full text search 

2. Create array attributes: quarter_shot_number in a new table quarter_shots. This attributes contains a four-element array that calculate each players total attempts in every quarter, 
indicating players' tendency to shot in every quarter.

3. Create composite type: stadium_type and table stadium_composite - containing all information about this stadium such as size, location and name and build a table for it.

<li>Some example query for new updating functions: 

-- Find teams that has descirption containing "NBA finals" or "champion"

select team_name, found_year from teams where plainto_tsquery('NBA finals')||plainto_tsquery('champion') @@ to_tsvector(description);

And the output will be:

       team_name        | found_year 
------------------------+------------
 New York Knicks        |       1946
 Indiana Pacers         |       1967
 Atlanta Hawks          |       1946
 Miami Heat             |       1988
 Orlando Magic          |       1989
 Washington Wizards     |       1961
 Denver Nuggets         |       1967
 Minnesota Timberwolves |       1989
 Oklahoma City Thunder  |       1967
 Portland Trail Blazers |       1970
 Utah Jazz              |       1974
 Los Angeles Lakers     |       1947
 Phoenix Suns           |       1968
 Houston Rockets        |       1967
 (It doesn't means the rest teams never enter finals)


-- Find the top 10 players that has the highest shot attempts within a quarter

select player, max(q_shot) as max_shot from 
 (select player_name as player, unnest(quarter_shot_number) as q_shot from quarter_shots q, players p where p.player_id = q.player_id) t1
 group by t1.player ORDER BY max_shot DESC limit 10;
 
 And the output will be 
 
   player       | max_shot 
-------------------+----------
 LeBron James      |       21
 LaMarcus Aldridge |       19
 Chris Paul        |       18
 Jordan Hill       |       18
 Nikola Mirotic    |       17
 Spencer Hawes     |       17
 Rudy Gay          |       16
 Isaiah Thomas     |       15
 JJ Redick         |       15
 Tyreke Evans      |       14
(10 rows)

This resulst shows that Lebron James shot in total 21 times in a single quarter in his match during our database time horizon
