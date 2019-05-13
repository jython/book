import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate, jsonify
from rostertool.lib import helpers as h
from rostertool.lib.base import BaseController, render
from rostertool.model import Session, Player
from routes import redirect_to
import simplejson as json
from rostertool.controllers.validators import *

log = logging.getLogger(__name__)

class ApiController(BaseController):
    @jsonify
    def players(self):
        session = Session()
        players = [{'first': p.first, 
                    'last': p.last, 
                    'position': p.position, 
                    'id': p.id} for p in session.query(Player).all()]
        return players

    @jsonify
    def add_player(self):
        obj = json.loads(request.body)
        schema = PlayerForm()
        try:
            form_result = schema.to_python(obj)
        except formencode.Invalid as error:
            response.content_type = 'text/plain'
            return 'Invalid: '+unicode(error)
        else:
            session = Session()
            first, last, position = obj['first'], obj['last'], obj['position']
            if session.query(Player).filter_by(last=last, first=first,
                    position=position).count() == 0:
                session.add(Player(first, last, position))
                session.commit()
                return {'result': 'OK'}
            else:
                return {'result':'fail', 'msg': 'Player already exists'}


