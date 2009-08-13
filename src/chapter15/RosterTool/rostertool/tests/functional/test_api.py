from rostertool.tests import *
import simplejson as json
from rostertool.model.models import Session, Player

class TestApiController(TestController):
    # Note that we're using subclasses of unittest.TestCase so we need
    # to be careful with setup/teardown camelcasing unlike nose's
    # default behavior

    def setUp(self):
        session = Session()
        for player in session.query(Player):
            session.delete(player)
        session.commit()

    def test_add_player(self):
        data = json.dumps({'first': 'Victor', 
            'last': 'Ng',
            'position': 'Goalie'})
        # Note that the content-type is set in the headers to make
        # sure that paste.test doesn't URL encode our data
        response = self.app.post(url(controller='api', action='add_player'), 
            params=data, 
            headers={'content-type': 'application/x-json'})
        obj = json.loads(response.body)
        assert obj['result'] == 'OK'

        # Do it again and fail
        response = self.app.post(url(controller='api', action='add_player'), 
            params=data, 
            headers={'content-type': 'application/x-json'})
        obj = json.loads(response.body)
        assert obj['result'] <> 'OK'

