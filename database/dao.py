from database.DB_connect import DBConnect


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    def read_rifugi(self):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = ''' select id, nome, localita
                    from rifugio '''
        cursor.execute(query)
        for row in cursor: result.append(row)
        cursor.close()
        conn.close()
        return result

    def read_connessioni(self,year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """
        select id_rifugio1, id_rifugio2, anno, difficolta, distanza
        from connessione
            where anno <= %s
        """
        cursor.execute(query,(year,))
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result
