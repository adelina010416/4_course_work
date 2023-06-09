from dao.genres_dao import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self, page):
        return self.dao.get_all(page)

    def create(self, genre_d):
        return self.dao.create(genre_d)

    def update(self, genre_d):
        return self.dao.update(genre_d)

    def delete(self, rid):
        self.dao.delete(rid)
