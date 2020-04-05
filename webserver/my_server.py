import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


DATABASEURI = "postgresql://jl5521:6447@35.231.103.173/proj1part2"
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
  return render_template("home.html")

@app.route('/player',methods = ['GET', 'POST'])
def search_player():
	if request.method == 'POST':
		player_name = request.form.get('player')
		sql = "select player_name from players where player_name ilike '%%{name}%%'".format(name=player_name)
		cursor = g.conn.execute(sql)
		names = []
		for result in cursor:
			names.append(result[0])  
		cursor.close()

		player_search_names = dict(data = names)
		return render_template("player_search_result.html", **player_search_names)

	return '''<form method="POST">
                  player: <input type="text" name="player"><br>
                  <input type="submit" value="Submit"><br>
                  </form>'''

@app.route('/player/<playername>')
def show_player_result(playername):
	sql = "select * from players where player_name = '{name}'".format(name=playername)
	cursor = g.conn.execute(sql)
	record = cursor.fetchone()
	player_stat = dict(player_id = record['player_id'],player_name=record['player_name'],team_name=record['team_name'],player_position=record['player_position'],
		height=record['height'],weight=record['weight'],block=record['block'],rebounds=record['rebounds'],assists=record['assists'],steals=record['steals'],
		twopoint_shot_percentage=record['twopoint_shot_percentage'],threepoint_shot_percentage=record['threepoint_shot_percentage'],start_year=record['start_year'],
		salary=record['salary'],points_per_game=record['points_per_game'])
	cursor.close()

	return render_template("play_stat.html", **player_stat)



@app.route('/player/<playername>/schedule')
def player_schedule(playername):
	return 'Todo....'


@app.route('/player/<playername>/news')
def news(playername):
	sql = """select news_title,news_context,news_date from players,news_to_players,news 
			where players.player_name = '{name}' and players.player_id = news_to_players.player_id 
			and news_to_players.news_id = news.news_id""".format(name=playername)
	cursor = g.conn.execute(sql)
	record = cursor.fetchall()
	context = dict(player_name=playername,news_result=record)
	cursor.close()
	return render_template("player_news.html", **context)


@app.route('/team',methods = ['GET', 'POST'])
def search_team():
	if request.method == 'POST':
		team_name = request.form.get('team')
		sql = "select team_name from teams where player_name team_name '%%{team}%%'".format(team=team_name)
		cursor = g.conn.execute(sql)
		names = []
		for result in cursor:
			names.append(result[0])  
		cursor.close()
		team_search_names = dict(data = names)
	return render_template("team_search_result.html", **team_search_names)
	
	return '''<form method="POST">
                  team: <input type="text" name="team"><br>
                  <input type="submit" value="Search"><br>
                  <p><a href="/">Back to homepage</a> </p>
                  </form>'''



@app.route('/team/<teamname>')
def team_info(teamname):
	sql = """select teams.team_name,found_year,city,state,stadium_name,coach_name from teams,coaches,stadium_to_team,coach_to_team 
			where teams.team_name = '{name}' and coaches.coach_id = coach_to_team.coach_id and coach_to_team.team_name = teams.team_name 
			and teams.team_name = stadium_to_team.team_name""".format(name=teamname)
	cursor = g.conn.execute(sql)
	record = cursor.fetchone()
	team_stat = dict(team_name = record['team_name'],found_year=record['found_year'],city=record['city'],
					state=record['state'],stadiums=record['stadium_name'],coach=record['coach_name'])
	cursor.close()
	return render_template("team_info.html", **team_stat)

@app.route('/team/<teamname>/schedule')
def schedule(teamname):
	return 'Todo....'

@app.route('/team/<teamname>/player_list')
def player_list(teamname):
	sql = """select player_name from players,teams,players_to_team where teams.team_name = '{name}' 
			and players_to_team.player_id = players.player_id and players_to_team.team_name = teams.team_name""".format(name=teamname)
	cursor = g.conn.execute(sql)
	names = []
	for result in cursor:
		names.append(result[0])  
	cursor.close()
	playerlists = dict(data = names)
	context = dict(team_name = teamname,player_list=playerlists)
	return render_template("player_list.html", **context)



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()