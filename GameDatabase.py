from neo4j import GraphDatabase

class GameDatabase:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def _execute_query(self, query, parameters=None):
        with self._driver.session() as session:
            return session.run(query, parameters)

    def create_player(self, player_id, name):
        query = "CREATE (p:Player {player_id: $player_id, name: $name})"
        self._execute_query(query, {"player_id": player_id, "name": name})

    def update_player(self, player_id, name):
        query = "MATCH (p:Player {player_id: $player_id}) SET p.name = $name"
        self._execute_query(query, {"player_id": player_id, "name": name})

    def delete_player(self, player_id):
        query = "MATCH (p:Player {player_id: $player_id}) DETACH DELETE p"
        self._execute_query(query, {"player_id": player_id})

    def create_match(self, match_id, player_ids, result):
        query = "CREATE (m:Match {match_id: $match_id, result: $result})"
        for player_id in player_ids:
            query += f" MATCH (p{player_id}:Player {{player_id: '{player_id}'}}) CREATE (m)-[:HAS_PLAYER]->(p{player_id})"
        self._execute_query(query, {"match_id": match_id, "result": result})

    def update_match(self, match_id, result):
        query = "MATCH (m:Match {match_id: $match_id}) SET m.result = $result"
        self._execute_query(query, {"match_id": match_id, "result": result})

    def delete_match(self, match_id):
        query = "MATCH (m:Match {match_id: $match_id}) DETACH DELETE m"
        self._execute_query(query, {"match_id": match_id})

    def get_players(self):
        query = "MATCH (p:Player) RETURN p"
        return [record['p'] for record in self._execute_query(query)]

    def get_match(self, match_id):
        query = "MATCH (m:Match {match_id: $match_id}) RETURN m"
        return self._execute_query(query, {"match_id": match_id}).single()['m']

    def get_player_matches(self, player_id):
        query = "MATCH (p:Player {player_id: $player_id})-[:HAS_PLAYER]->(m:Match) RETURN m"
        return [record['m'] for record in self._execute_query(query, {"player_id": player_id})]
