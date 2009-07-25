
import formencode

class DeletePlayerForm(formencode.Schema):
    # You need the next line to drop the submit button values
    allow_extra_fields=True

    id = formencode.validators.Int(not_empty=True)
    first = formencode.validators.String(not_empty=True)
    last = formencode.validators.String(not_empty=True)
    position = formencode.validators.String(not_empty=True)


class PlayerForm(formencode.Schema):
    # You need the next line to drop the submit button values
    allow_extra_fields=True

    first = formencode.validators.String(not_empty=True)
    last = formencode.validators.String(not_empty=True)
    position = formencode.validators.String(not_empty=True)
