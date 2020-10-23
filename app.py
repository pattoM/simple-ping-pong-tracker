from flask import Flask, render_template, jsonify,redirect, request, session , url_for, flash
import os 
from config import * 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from forms import * 

#instance 
app = Flask(__name__) 

#config 
if os.getenv('FLASK_DEBUG', None):
    app.config.from_object(DevelopmentConfig) 
else:
    app.config.from_object(ProductionConfig) 


db = SQLAlchemy(app) 

from models import * #avoiding circular import hell 

#migrations 
migrate = Migrate(app,db)


#main route 
@app.route('/')
@app.route('/leaderboard', methods=["GET"]) 
def leaderboard():
    #query users ordering by score sum 

    leads = User.query.order_by(User.score_sum.desc()).all()
    return render_template("index.html", leads=leads)

@app.route('/add_user', methods=["GET","POST"])
def add_user():
    form = AddUserForm() 

    if form.validate_on_submit():
        #unique check from db 
        user = User.query.filter_by(name=form.name.data).first() 
        if not user:
            new_user = User(name=form.name.data)
            db.session.add(new_user)
            db.session.commit()
            flash("User added successfully") 
            return redirect(url_for('add_user'))
        else:
            flash("Username needs to be unique")
    return render_template("add-user.html", form=form)


@app.route('/new-game', methods=["GET","POST"]) 
def new_game():
    form = NewGameForm() 

    #query all users
    users = User.query.all() 

    #add users to form choices 
    form.player_one.choices = [(i.id,i.name) for i in users]
    form.player_two.choices = [(i.id,i.name) for i in users]
    form.starting_player.choices = [(i.id,i.name) for i in users]

    if form.validate_on_submit():
        new_game = Game(current_serving=form.starting_player.data) 
        #add players to game 
        p1 = User.query.filter_by(id=form.player_one.data).first() 
        p2 = User.query.filter_by(id=form.player_two.data).first() 
        
        #reset serve gaps to zero for new game 
        p1.serve_gap = 0 
        p2.serve_gap = 0 
        new_game.players.append(p1) 
        new_game.players.append(p2) 
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for("running_game", id=new_game.id)) 

    return render_template("new-game.html", form=form) 

@app.route('/game/<id>', methods=["GET", "POST"]) 
def running_game(id):
    form1 = ScoreForm() 
    form2 = ScoreForm2() 
    #get the game in store 
    game  = Game.query.filter_by(id=id).first() 
    
    if not game:
        flash("That game does not exist ")
        return redirect('/')
    if game.game_complete:
        #redirect to stats
        return redirect(url_for("game_stats", id=game.id))

    #recording serve in get request 
    serv = request.args.get("serving_id", None) 
    if serv:
        user  = User.query.filter_by(id=serv).first()
        user.serve_gap = user.serve_gap + 1
        #switch  player if serve gap exceeded 2 - when not in deuce, else every other turn 
        if game.in_deuce:
            user.serve_gap = 0
            game.toggle_serving_player()
        else:
            if user.serve_gap >= 2:
                game.toggle_serving_player()
                user.serve_gap = 0 

        db.session.commit()
        return redirect(url_for('running_game', id=id))

    if form1.validate_on_submit() and request.args.get('form_tagger',None) == 'f1':
        user  = User.query.filter_by(id=form1.user_id.data).first() 
        if user.score_sum:
            user.score_sum = User.score_sum + int(form1.score.data) 
        else:
            user.score_sum = int(form1.score.data)

        new_gamescore = GameScore(score=form1.score.data,owner=user, related_game=game, game_round=game.current_round) 
        db.session.add(new_gamescore) 
        db.session.commit() 

        #proceed round or win 
        #get scores in round in list to check for deuce 
        player_scores = game.get_player_scores_in_round() 
        if player_scores[0] == player_scores[1] and player_scores[0] == app.config['LIM']:
            game.in_deuce = True 
            db.session.commit()
        elif player_scores[0] > app.config['LIM']:
            if game.current_round == app.config['MAX_ROUNDS']:
                #game has ended, redirect to status page 
                if not game.in_deuce:
                    game.game_complete = True 
                    db.session.commit()
                    return redirect(url_for("game_stats",id=game.id)) 
                else:
                    #gap of two is what can count  
                    if abs(player_scores[0]-player_scores[1]) >= 2:
                        game.game_complete = True 
                        db.session.commit()
                        return redirect(url_for("game_stats",id=game.id)) 
                        
            else:
                if not game.in_deuce:
                    game.current_round = game.current_round + 1 
                else:
                    if abs(player_scores[0]-player_scores[1]) >= 2:
                        game.current_round = game.current_round + 1 

                db.session.commit()

        return redirect(url_for('running_game',id=id)) 


    if form2.validate_on_submit() and request.args.get('form_tagger',None) == 'f2':
        user  = User.query.filter_by(id=form2.user_id2.data).first() 
        if user.score_sum:
            user.score_sum = User.score_sum + int(form2.score2.data) 
        else:
            user.score_sum = int(form2.score2.data)

        new_gamescore = GameScore(score=form2.score2.data,owner=user, related_game=game, game_round=game.current_round) 
        db.session.add(new_gamescore) 
        db.session.commit() 

        

        #proceed round or win 
        player_scores = game.get_player_scores_in_round() 
        if player_scores[0] == player_scores[1] and player_scores[0] == app.config['LIM']:
            game.in_deuce = True 
            db.session.commit()
        elif player_scores[1] > app.config['LIM']:
            if game.current_round == app.config['MAX_ROUNDS']:
                #game has ended, redirect to status page 
                if not game.in_deuce:
                    game.game_complete = True 
                    db.session.commit()
                    return redirect(url_for("game_stats",id=game.id)) 
                else:
                    #gap of two is what can count  
                    if abs(player_scores[0]-player_scores[1]) >= 2:
                        game.game_complete = True 
                        db.session.commit()
                        return redirect(url_for("game_stats",id=game.id)) 
                        
            else:
                if not game.in_deuce:
                    game.current_round = game.current_round + 1 
                else:
                    if abs(player_scores[0]-player_scores[1]) >= 2:
                        game.current_round = game.current_round + 1 

                db.session.commit()

        return redirect(url_for('running_game',id=id)) 

    return render_template("running-game.html",id=game.id, game=game, form1=form1, form2=form2) 


@app.route('/game-stats/<id>', methods=["GET", "POST"]) 
def game_stats(id): 
    game  = Game.query.filter_by(id=id).first()  


    #breakdown of points by round then determining winner 
    data = []
    for i in range(1,app.config['MAX_ROUNDS']+1):
        u1 = game.players[0].get_score_in_round(game.id, i) 
        u2 = game.players[1].get_score_in_round(game.id, i) 
        data.append([f"Round {i}",u1,u2,game.players[0].name if u1 > u2 else game.players[1].name]) 
        
    return render_template("game-stats.html", game=game, data=data)