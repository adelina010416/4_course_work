from dao.model.user import User


class AuthDAO:
    def __init__(self, session):
        self.session = session

    def create(self, data):
        ent = User(**data)
        self.session.add(ent)
        self.session.commit()
        return ent
