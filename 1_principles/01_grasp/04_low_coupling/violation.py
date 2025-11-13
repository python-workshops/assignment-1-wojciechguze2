"""
❌ VIOLATION of GRASP Low Coupling

Problem: Game bezpośrednio zależy od Database
- Silne sprzężenie - Game "wie" o szczegółach bazy danych
- Zmiana Database wymaga modyfikacji Game
- Trudne testowanie - nie można łatwo zamockować Database
- Naruszenie Low Coupling: zbyt wiele zależności między klasami
"""


class Database:
    """
    Konkretna implementacja bazy danych

    UWAGA: Użyj tej klasy w ScoreService, NIE w Game!
    Game powinien znać tylko ScoreService (pośrednika)
    """

    def connect(self) -> str:
        return "Connected to database"

    def save(self, player: str, score: int) -> str:
        return f"Saved score {score} for {player}"


class ScoreService:
    def __init__(self, game: Game):
        ...


class Game:
    """
    ❌ PROBLEM: Bezpośrednia zależność od Database

    Konsekwencje:
    1. Silne sprzężenie - Game musi znać Database
    2. Trudne testowanie - wymaga prawdziwej bazy lub użycia patcha
    3. Zmiana Database = zmiana Game
    4. Game odpowiada za logikę gry ORAZ komunikację z bazą
    """

    def finish_game(self, player: str, score: int) -> str:
        """
        ❌ Tworzy Database bezpośrednio w metodzie
        """
        # ❌ PROBLEM: Bezpośrednie tworzenie Database
        # Game "wie" o Database - silne sprzężenie
        db = Database()

        # ❌ PROBLEM: Game zna szczegóły implementacji Database
        # Musi wiedzieć że trzeba najpierw connect(), potem save()
        result = db.connect()
        result += "\n" + db.save(player, score)

        return f"Game finished.\n{result}"


# ❌ Przykład użycia - działa, ale narusza Low Coupling
if __name__ == "__main__":
    game = Game()
    print(game.finish_game("Alice", 150))

    # ❌ Chcę przetestować Game bez prawdziwej bazy?
    # Nie mogę - Game tworzy Database bezpośrednio w finish_game() (ew. patch)
    #
    # ❌ Chcę zmienić Database na inną implementację?
    # Muszę EDYTOWAĆ Game.finish_game()
    #
    # ❌ Chcę dodać cache między Game a Database?
    # Muszę EDYTOWAĆ Game - nie ma miejsca na pośrednika
    #
    # To naruszenie Low Coupling!


"""
Dlaczego to jest ZŁE?

1. ❌ Silne sprzężenie
   - Game bezpośrednio zależy od Database
   - Game musi znać szczegóły Database (connect, save)
   - Trudno zmienić implementację

2. ❌ Trudne testowanie
   - Nie można wstrzyknąć mock Database, trzeba patchować
   - Trudno testować Game w izolacji

3. ❌ Brak elastyczności
   - Nie można dodać pośrednika (cache, logger)
   - Zmiana Database wymaga zmiany Game
   - Naruszenie Open/Closed

4. ❌ Naruszenie Single Responsibility
   - Game odpowiada za logikę gry
   - Game odpowiada za komunikację z bazą
   - Dwie odpowiedzialności w jednej klasie

5. ❌ Wysokie sprzężenie = niska "współużywalność"
   - Game nie może działać bez Database
   - Nie można użyć Game z innym storage (file, API)

Jak to naprawić?
1. Stwórz ScoreService jako pośrednika
2. Game przyjmuje ScoreService w konstruktorze (dependency injection)
3. ScoreService izoluje Game od Database
4. Game nie zna szczegółów Database - tylko wywołuje score_service.save_score()
"""
