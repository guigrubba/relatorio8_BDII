import GameDatabase

db = GameDatabase("bolt://3.83.20.41:7687", "neo4j", "orifices-bang-harmonies")

# criar jogadores
db.create_player("p1", "Alice")
db.create_player("p2", "Bob")

# criar uma partida
db.create_match("m1", ["p1", "p2"], "Alice wins")

# obter informações
players = db.get_players()
match = db.get_match("m1")
alice_matches = db.get_player_matches("p1")
