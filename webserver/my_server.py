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



@app.route('/team',methods = ['GET', 'POST'])
def search_team():
	return 'Todo....'


@app.route('/team/<teamname>')
def team_info(teamname):
  return 'Todo....'



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