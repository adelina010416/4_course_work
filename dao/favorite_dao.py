from dao.model.favorite_movie import FovoriteMovie


class FavoriteDAO:
    def __init__(self, session):
        self.session = session

    def create(self, new_data):
        ent = FovoriteMovie(**new_data)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, mid, user_id):
        self.session.query(FovoriteMovie).filter(FovoriteMovie.user_id == user_id, FovoriteMovie.movie_id == mid).delete()
        self.session.commit()

