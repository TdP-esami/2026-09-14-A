from database.DB_connect import DBConnect
from model.actor import Actor


class DAO:

    @staticmethod
    def getActorsInRatingRange(val_min, val_max):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct n.id, n.name, n.date_of_birth
                from names n, role_mapping rm, movie m, ratings r
                where n.id = rm.name_id
                and rm.movie_id = m.id
                and m.id = r.movie_id
                and (rm.category = 'actor' or rm.category = 'actress')
                and r.avg_rating between %s and %s
                order by n.name
                """

        cursor.execute(query, (val_min, val_max))

        for row in cursor:
            results.append(Actor(row["id"], row["name"], row["date_of_birth"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getMoviesForActorInRange(actor, val_min, val_max):
        """
        Dato un attore, lo popolo con la lista dei film (con valutazione media compresa
        nell'intervallo scelto) in cui recita. I film sono dict con campi:
        {"movie_id", "title", "year", "rating" (float)}.
        """
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """
                select m.id, m.title, m.year, r.avg_rating
                from movie m, role_mapping rm, ratings r
                where m.id = rm.movie_id
                and m.id = r.movie_id
                and rm.name_id = %s
                and (rm.category = 'actor' or rm.category = 'actress')
                and r.avg_rating between %s and %s
                """
        cursor.execute(query, (actor.NameId, val_min, val_max))

        movies = []
        for row in cursor:
            movies.append({
                "movie_id": row["id"],
                "title": row["title"],
                "year": row["year"],
                "rating": float(row["avg_rating"]),
            })

        actor.Movies = movies

        cursor.close()
        conn.close()
