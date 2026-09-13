from database.DB_connect import DBConnect
from model.arco import Arco
from model.attori import Attori


class DAO():
    @staticmethod
    def getAllRatings():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct avg_rating 
                    from ratings r 
                    order by avg_rating ASC"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["avg_rating"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllNodes(voto1, voto2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct n.id,n.name, n.height,
                n.date_of_birth,n.known_for_movies, TIMESTAMPDIFF(YEAR, n.date_of_birth, CURDATE()) AS eta
                from role_mapping rm , names n , movie m, ratings r 
                WHERE rm.category IN ('actor', 'actress') 
                and n.date_of_birth is not null
                and n.id =rm.name_id and rm.movie_id =m.id 
                 AND m.id = r.movie_id
                and r.avg_rating between %s and %s
                AND n.date_of_birth <= CURDATE()  """

        cursor.execute(query, (voto1, voto2))

        for row in cursor:
            results.append(Attori(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(voto1, voto2, idMapA):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT 
                    rm1.name_id AS a1, 
                    rm2.name_id AS a2, 
                    m.worlwide_gross_income AS incasso
                FROM 
                    role_mapping rm1, 
                    role_mapping rm2, 
                    movie m, 
                    ratings r
                WHERE 
                    rm1.movie_id = rm2.movie_id          -- Hanno recitato nello STESSO film
                    AND rm1.movie_id = m.id              -- Colleghiamo al film per prendere l'incasso
                    AND m.id = r.movie_id                -- Colleghiamo al rating
                    AND rm1.name_id < rm2.name_id        -- Evita duplicati e auto-archi (A con A)
                    AND rm1.category IN ('actor', 'actress')
                    AND rm2.category IN ('actor', 'actress')
                    AND r.avg_rating BETWEEN %s AND %s
                    AND m.worlwide_gross_income IS NOT NULL; """

        cursor.execute(query, (voto1, voto2))

        for row in cursor:
            id1 = row["a1"]
            id2 = row["a2"]
            if id1 in idMapA and id2 in idMapA:
                results.append(Arco(idMapA[row["a1"]], idMapA[row["a2"]], row["incasso"]))

        cursor.close()
        return results