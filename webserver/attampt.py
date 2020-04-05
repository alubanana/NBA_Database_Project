import os
from flask import Flask, request, render_template, g, redirect, Response
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__,template_folder=tmpl_dir)


@app.route('/')
def index():
  return render_template("home.html")


@app.route('/player',methods = ['GET', 'POST'])
def search_player():
  if request.method == 'POST':
    print(request.args)
    names = ['James']
    player_search_names = dict(data = names)
    
    return render_template("player_search_result.html", **player_search_names)

  return '''<form method="POST">
                  player: <input type="text" name="name of player you want to search"><br>
                  <input type="submit" value="Search"><br>
                  <p><a href="/">Back to homepage</a> </p>
                  </form>'''

@app.route('/player/<playername>')
def show_player_result(playername):
  player_stat = dict(player_id = 111,player_name=playername,team_name='11  1',player_position='F',height=111,weight=111,
      block=111,rebounds=111,assists=111,steals=111,twopoint_shot_percentage=111,threepoint_shot_percentage=111,start_year=1234,
      salary=12345,points_per_game=456)

  return render_template("play_stat.html", **player_stat)

@app.route('/player/<playername>/schedule')
def player_schedule(playername):
  return 'Todo....'


@app.route('/player/<playername>/news')
def news(playername):
  return '''<html>
  <head>
  <title>Team Infomation</title>
  <h1>News of {player_name}</h1>
  </head>
  <body>
  <table border="1">
    <tr>
      <th>news_title</th>
      <th>news_context</th>
      <th>news_date</th>
    </tr>
    {{%% for i in news_result %%}}
      <tr>
      <td>{{{{ i[1] }}}}</td>
      <td>{{{{ i[2] }}}}</td>
      <td>{{{{ i[3] }}}}</td>
      </tr>
    {{%% endfor %%}}
  </table>
  <p><br><br>
  <p><a href="/">Back to homepage</a> </p>
  <p><a href="/player">Back to player search</a> </p>
  </p>
  </body>
  </html>'''.format(player_name=playername)





@app.route('/team',methods = ['GET', 'POST'])
def search_team():
  if request.method == 'POST':
    print(request.args)
    names = ['Rockets']
    team_search_names = dict(data = names)
    
    return render_template("team_search_result.html", **team_search_names)

  return '''<form method="POST">
                  team: <input type="text" name="name of team you want to search"><br>
                  <input type="submit" value="Search"><br>
                  <p><a href="/">Back to homepage</a> </p>
                  </form>'''



@app.route('/team/<teamname>')
def team_info(teamname):
  team_stat = dict(team_name = teamname,found_year=111,city='11  1',state='F',stadiums='111',coach='111')
  return render_template("team_info.html", **team_stat)

@app.route('/team/<teamname>/schedule')
def schedule(teamname):
  return 'Todo....'

@app.route('/team/<teamname>/player_list')
def player_list(teamname):
  playerlists=['James','Paul']
  context = dict(team_name = teamname,player_list=playerlists)

  return render_template("player_list.html", **context)



if __name__ == '__main__':
    app.run(debug=True)