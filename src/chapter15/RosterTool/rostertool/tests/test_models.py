from rostertool.model import Player, Session, engine

class TestModels(object):

    def setup(self):
        self.cleanup()

    def teardown(self):
        self.cleanup()

    def cleanup(self):
        session = Session()
        for player in session.query(Player):
            session.delete(player)
        session.commit()

    def test_create_player(self):
        session = Session()
        player1 = Player('Josh', 'Juneau', 'forward')
        player2 = Player('Jim', 'Baker', 'forward')
        player3 = Player('Frank', 'Wierzbicki', 'defense')
        player4 = Player('Leo', 'Soto', 'defense')
        player5 = Player('Vic', 'Ng', 'center')
        session.add(player1)
        session.add(player2)
        session.add(player3)
        session.add(player4)
        session.add(player5)

        # But 5 are in the session, but not in the database
        assert 5 == session.query(Player).count()
        assert 0 == engine.execute("select count(id) from player").fetchone()[0]
        session.commit()

        # Check that 5 records are all in the database
        assert 5 == session.query(Player).count()
        assert 5 == engine.execute("select count(id) from player").fetchone()[0]

        # Load records up
        players = session.query(Player).filter_by(first='Josh', last='Juneau').all()
        assert len(players) == 1
        # SA keeps an identity map - this is the *same* object
        assert players[0] == player1

        # Edit the object and commit the session
        player1.position  = 'goalie'
        session.commit()

        # now just fetch the goalie
        goalie = session.query(Player).filter_by(position='goalie').one()
        assert goalie == player1

