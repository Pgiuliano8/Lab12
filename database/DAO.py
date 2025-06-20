from database.DB_connect import DBConnect
from model.archi import Arco
from model.retailers import Retailer


class DAO():

    @staticmethod
    def get_countries():
        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        res = []

        query="""select distinct(gr.Country) 
                    from go_retailers gr 
                    order by gr.Country asc 
        """

        cursor.execute(query)

        for row in cursor:
            res.append(row[0])

        conn.close()
        cursor.close()

        return res

    @staticmethod
    def getNodes(country):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        query = """select *
                        from go_retailers gr 
                        where gr.Country = %s 
            """

        cursor.execute(query, (country,))

        for row in cursor:
            res.append(Retailer(**row))

        conn.close()
        cursor.close()

        return res

    @staticmethod
    def getEdges(year, country, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        query = """select gds.Retailer_code as a1, gds2.Retailer_code as a2, count(distinct(gds2.Product_number)) as peso 
                    from go_daily_sales gds, go_daily_sales gds2, go_retailers gr, go_retailers gr2 
                    where year(gds.Date)=year(gds2.`Date`) and year(gds2.`Date`)=%s and gr.Retailer_code=gds.Retailer_code
                    and  gds.Retailer_code<gds2.Retailer_code and gr2.Retailer_code=gds2.Retailer_code and gr.Country=gr2.Country
                    and gr2.Country=%s and gds.Product_number = gds2.Product_number
                    group by  gds.Retailer_code, gds2.Retailer_code
                """

        cursor.execute(query, (year, country))

        for row in cursor:
            res.append(Arco(idMap[row["a1"]], idMap[row["a2"]], row["peso"]))

        conn.close()
        cursor.close()

        return res


