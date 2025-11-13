"""
GRASP Low Coupling - Game System

>>> # Test ScoreService
>>> service = ScoreService()
>>> service.save_score("player1", 100)
'Saved score 100 for player1'

>>> # Test Game with ScoreService (low coupling)
>>> game = Game(service)
>>> game.finish_game("Alice", 150)
'Game finished. Saved score 150 for Alice'
"""


class Database:
    """Konkretna implementacja bazy danych"""

    def connect(self) -> str:
        return "Connected to database"

    def save(self, player: str, score: int) -> str:
        return f"Saved score {score} for {player}"


# TODO: Zaimplementuj ScoreService
# Klasa pośrednicząca między Game a bazą danych (redukuje sprzężenie)
# Metoda save_score(player, score) zwraca: "Saved score {score} for {player}"

class ScoreService:
    def __init__(self):
        self.db = Database()
        self.db.connect()

    def save_score(self, player: str, score: int) -> str:
        return self.db.save(player, score)


# TODO: Zaimplementuj Game
# Przyjmuje score_service: ScoreService w konstruktorze (dependency injection)
# Metoda finish_game(player, score):
#   - Wywołuje score_service.save_score(player, score)
#   - Zwraca "Game finished. {wynik z save_score}"
#
# Low Coupling: Game nie zna Database, tylko ScoreService (pośrednik)

class Game:
    def __init__(self, score_service: ScoreService):
        self.score_service = score_service

    def finish_game(self, player: str, score: int) -> str:
        service_res = self.score_service.save_score(player, score)

        return f"Game finished. {service_res}"


# GRASP Low Coupling:
# Minimalizuj zależności między klasami
#
# Silne sprzężenie ❌:
# Game → Database (bezpośrednia zależność)
#
# Luźne sprzężenie ✅:
# Game → ScoreService → Database (pośrednik)
#
# Korzyść: Zmiana Database nie wpływa na Game
