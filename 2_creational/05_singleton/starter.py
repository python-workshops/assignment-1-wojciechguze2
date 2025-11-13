"""
Singleton Pattern - Config Manager
Zaimplementuj wzorzec Singleton dla zarządzania konfiguracją gry.

Singleton gwarantuje że klasa ma tylko JEDNĄ instancję i zapewnia globalny punkt dostępu.

Examples:
    >>> import sys; sys.tracebacklimit = 0

    >>> # Test singleton behavior - ta sama instancja
    >>> config1 = ConfigManager()
    >>> config2 = ConfigManager()
    >>> config1 is config2
    True

    >>> # Test zarządzania konfiguracją
    >>> config1.set_config("theme", "dark")
    >>> config1.set_config("difficulty", "medium")
    >>> config1.get_config("theme")
    'dark'

    >>> # Test współdzielonego stanu - zmiana w config1 widoczna w config2
    >>> config2.get_config("theme")
    'dark'
    >>> config2.get_config("difficulty")
    'medium'

    >>> # Test wartości domyślnej
    >>> config1.get_config("nonexistent", "default_value")
    'default_value'

    >>> # Test sprawdzania istnienia klucza
    >>> config1.has_config("theme")
    True
    >>> config1.has_config("nonexistent")
    False

    >>> # Test liczby konfiguracji
    >>> len(config1.get_all_configs())
    2
"""
# %% About
# - Name: Singleton - Config Manager
# - Difficulty: easy
# - Lines: 8
# - Minutes: 12
# - Focus: Wzorzec Singleton

# %% Description

from typing import Any, Dict

# %% Hints
# - Użyj metody __new__ do kontroli tworzenia instancji
# - Przechowuj jedyną instancję w zmiennej klasowej _instance
# - Prosty if/else check - bez threading
# - Metoda __init__ i metody zarządzania są już gotowe

# %% Run
# - PyCharm: right-click and `Run Doctest in ...`
# - Terminal: `python -m doctest -f -v starter.py`
# - Tests: `python -m pytest test_basic.py -v`

# %% STEP 1: ConfigManager - metody pomocnicze - GOTOWE
# Te metody są już zaimplementowane - możesz ich używać

class ConfigManager:
    """
    Config Manager dla gry RPG

    Zarządza ustawieniami gry w sposób centralny.
    TODO: Zaimplementuj jako Singleton - jedna instancja dla całej aplikacji.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)

        return cls._instance

    # TODO: WZORZEC SINGLETON - DO IMPLEMENTACJI
    #
    # Zmienna klasowa _instance - przechowuje jedyną instancję (początkowo None)
    #
    # Metoda __new__(cls):
    #   - Kontroluje tworzenie instancji
    #   - Sprawdź czy instancja już istnieje
    #   - Jeśli nie: stwórz i zapisz w _instance
    #   - Zwróć _instance

    # ════════════════════════════════════════════════════════
    # Inicjalizacja i metody zarządzania - GOTOWE (użyj ich)
    # ════════════════════════════════════════════════════════

    def __init__(self):
        """Inicjalizuje pusty słownik konfiguracji"""
        self._config: Dict[str, Any] = {}

    def set_config(self, key: str, value: Any) -> None:
        """
        Ustawia wartość konfiguracji

        Args:
            key: Klucz konfiguracji (np. "theme", "difficulty")
            value: Wartość do ustawienia
        """
        self._config[key] = value

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Pobiera wartość konfiguracji

        Args:
            key: Klucz konfiguracji
            default: Wartość domyślna jeśli klucz nie istnieje

        Returns:
            Wartość konfiguracji lub default
        """
        return self._config.get(key, default)

    def has_config(self, key: str) -> bool:
        """
        Sprawdza czy konfiguracja istnieje

        Args:
            key: Klucz do sprawdzenia

        Returns:
            True jeśli klucz istnieje
        """
        return key in self._config

    def get_all_configs(self) -> Dict[str, Any]:
        """
        Zwraca wszystkie konfiguracje

        Returns:
            Słownik wszystkich konfiguracji
        """
        return self._config.copy()

    def reset_configs(self) -> None:
        """Resetuje wszystkie konfiguracje (przydatne do testów)"""
        self._config.clear()


# %% Example Usage
# Odkomentuj gdy zaimplementujesz
# if __name__ == "__main__":
#     # Test singleton
#     config1 = ConfigManager()
#     config2 = ConfigManager()
#
#     print(f"Same instance: {config1 is config2}")
#
#     # Test functionality
#     config1.set_config("theme", "dark")
#     config1.set_config("language", "en")
#
#     print(f"Theme from config1: {config1.get_config('theme')}")
#     print(f"Theme from config2: {config2.get_config('theme')}")
#     print(f"All configs: {config1.get_all_configs()}")
