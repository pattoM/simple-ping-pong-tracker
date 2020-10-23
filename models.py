from app import db   
from uuid import uuid4 

#association table 
game_player_assoc = db.Table("game_player_assoc",
    db.Column('user_id', db.String(32), db.ForeignKey('user.id'), primary_key=True ),
    db.Column('game_id', db.String(32), db.ForeignKey('game.id'), primary_key=True )
)

class User(db.Model):
    id = db.Column(db.String(32), default=lambda: str(uuid4().hex), primary_key=True) 
    name = db.Column(db.String(100), unique=True) 
    score_sum = db.Column(db.Integer, unique=False)
    #one to many with gamescore
    user_scores = db.relationship('GameScore',cascade="all,delete", backref='owner', lazy=True)  

    serve_gap = db.Column(db.Integer, unique=False, default=0)

    def get_score(self,id):
        entries = [i.score for i in self.user_scores if i.related_game.id == id] 
        return sum(entries)

    def get_score_in_round(self,id, r):
        entries = [i.score for i in self.user_scores if i.related_game.id == id and i.game_round==r] 
        return sum(entries)



class Game(db.Model):
    id = db.Column(db.String(32), default=lambda: str(uuid4().hex), primary_key=True)
    current_serving = db.Column(db.String(32), unique=False) 
    winner = db.Column(db.String(32), unique=False) 
    current_round = db.Column(db.Integer, unique=False, default=1)
    game_complete = db.Column(db.Boolean, unique=False, default=False)
    in_deuce = db.Column(db.Boolean, unique=False, default=False) 

    # #relationship to players in game 
    players = db.relationship('User', secondary=game_player_assoc, backref='games', cascade="all,delete", order_by='User.id')
    #link to gamescore
    game_scores = db.relationship('GameScore',cascade="all,delete", backref='related_game', lazy=True)

    def toggle_serving_player(self):
        if self.players[0].id == self.current_serving:
            self.current_serving = self.players[1].id 
        else:
            self.current_serving = self.players[0].id 
        db.session.commit() 

        return True  

    def get_player_scores_in_round(self):
        return [self.players[0].get_score_in_round(self.id, self.current_round), self.players[1].get_score_in_round(self.id, self.current_round)]


class GameScore(db.Model):
    id = db.Column(db.String(32), default=lambda: str(uuid4().hex), primary_key=True)
    score  = db.Column(db.Integer, unique=False)
    game_round = db.Column(db.Integer, unique=False)
    #link user who scored it in one to many relationship
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    #link to game in one to one relationship
    game_id = db.Column(db.String(32), db.ForeignKey('game.id'), nullable=False)

    