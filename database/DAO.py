from database.DB_connect import DBConnect
from model.Arco import Arco
from model.Pilota import Pilota


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    def getPiloti(d1,d2):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct d.*
                    from races r, results re, drivers d 
                    where r.raceId = re.raceId and d.driverId = re.driverId 
                    and r.year between %s and %s
                    and re.position is not null"""

        cursor.execute(query, (d1,d2))

        for row in cursor:
            results.append(Pilota(**row))


        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges( d1, d2, idMapP):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT r1.driverId as id1, r2.driverId as id2, count(*) as peso
                    from races ra, results r1, results r2
                    where r1.raceId = ra.raceId  and r2.raceId = ra.raceId
                    and r1.constructorId = r2.constructorId
                    and r1.driverId > r2.driverId
                    and r1.position is not null
                    and r2.position is not null
                    and ra.year between %s and %s
                    group by r1.driverId, r2.driverId
                    order by peso desc"""


        cursor.execute(query, (d1, d2, ))

        for row in cursor:
            results.append(Arco(idMapP[row["id1"]], idMapP[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results
