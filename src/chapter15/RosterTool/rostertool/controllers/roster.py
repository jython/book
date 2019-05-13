import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from rostertool.lib import helpers as h
from rostertool.lib.base import BaseController, render
from rostertool.model import Session, Player
import formencode

log = logging.getLogger(__name__)

class PlayerForm(formencode.Schema):
    # You need the next line to drop the submit button values
    allow_extra_fields=True

    first = formencode.validators.String(not_empty=True)
    last = formencode.validators.String(not_empty=True)
    position = formencode.validators.String(not_empty=True)


class RosterController(BaseController):
    def index(self):
        db_session = Session()
        c.page_title = 'Player List'
        c.players = session.query(Player).all()
        return render('list_players.html')

    @validate(schema=PlayerForm(), form='index', post_only=False, on_get=True)
    def add_player(self):
        first = self.form_result['first']
        last = self.form_result['last']
        position = self.form_result['position']
        session = Session()
        if session.query(Player).filter_by(first=first, last=last).count() > 0:
            h.flash("Player already exists!")
            return h.redirect_to(controller='roster')
        player = Player(first, last, position)
        session.add(player)
        session.commit()
        return h.redirect_to(controller='roster', action='index')

    @validate(schema=PlayerForm(), form='edit_player', post_only=False, on_get=True)
    def save_player(self):
        id = self.form_result['id']
        first = self.form_result['first']
        last = self.form_result['last']
        position = self.form_result['position']
        session = Session()
        player = session.query(Player).filter_by(id=id).one()
        player.first = first
        player.last = last
        player.last = last
        player.position = position
        session.commit()
        return h.redirect_to(controller='roster')

    def edit_player(self, id):
        session = Session()
        player = session.query(Player).filter_by(id=id).one()
        c.player = player
        return render('edit_player.html')

    @validate(schema=PlayerForm(), form='edit_player', post_only=False, on_get=True)
    def delete_player(self):
        session = Session()
        id = self.form_result['id']
        first = self.form_result['first']
        last = self.form_result['last']
        position = self.form_result['position']

        players = session.query(Player).filter_by(id=id,
                first=first,
                last=last,
                position=position).all()
        if len(players) != 1:
            h.flash("The player was modified by someone else while you were staring at the screen!")
        else:
            player = players[0]
            session.delete(player)
            session.commit()
            h.flash("Player %s was deleted" % player.id)

        return h.redirect_to(controller='roster')

