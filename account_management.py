from flask_login import UserMixin
class User(UserMixin):
    def __init__(self):
        self.characters = []
        self.active_character = None
        super().__init__()
    pass
