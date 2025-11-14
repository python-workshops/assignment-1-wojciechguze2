"""
Strategy Pattern - Task Processing Strategies

>>> # Test tworzenia zadania
>>> task = WorkflowTask("Fix database bug", TaskPriority.HIGH, "Bug in user login")
>>> task.title
'Fix database bug'
>>> task.priority
<TaskPriority.HIGH: 'high'>

>>> # Test strategii urgent
>>> urgent_processor = UrgentTaskProcessor()
>>> manager = TaskManager(urgent_processor)
>>> urgent_task = WorkflowTask("Security breach", TaskPriority.URGENT, "Critical fix needed")
>>> result = manager.execute_task(urgent_task)
>>> result["status"]
'completed'
>>> result["processing_time"] < 1.0
True

>>> # Test zmiany strategii w runtime
>>> background_processor = BackgroundTaskProcessor()
>>> manager.set_strategy(background_processor)
>>> low_task = WorkflowTask("Update docs", TaskPriority.LOW, "Documentation update")
>>> result = manager.execute_task(low_task)
>>> result["strategy_used"]
'background'
"""

from abc import ABC, abstractmethod
from enum import Enum
import time
from typing import Dict, Any
from datetime import datetime


# %% Helper Classes - GOTOWE

class TaskPriority(Enum):
    """Priorytety zadań w workflow"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Strategies(Enum):
    STANDARD = "standard"
    BACKGROUND = "background"
    URGENT = "urgent"

    @staticmethod
    def get_values() -> list[str]:
        return [s.value for s in Strategies]


class WorkflowTask:
    """Zadanie w workflow system"""

    def __init__(self, title: str, priority: TaskPriority, description: str):
        self.title = title
        self.priority = priority
        self.description = description
        self.created_at = datetime.now()
        self.completed_at = None

    def mark_completed(self):
        """Oznacz zadanie jako ukończone"""
        self.completed_at = datetime.now()

    def get_status(self) -> str | None:
        if self.completed_at:
            return 'completed'
        else:
            return None


# %% Strategy Interface - GOTOWE
# WZORZEC: Strategy (interfejs strategii)

class TaskProcessor(ABC):
    """Interface dla strategii przetwarzania zadań"""

    @abstractmethod
    def __str__(self) -> str:
        """Zwróć nazwę strategii"""
        ...

    @abstractmethod
    def process_task(self, task: WorkflowTask) -> Dict[str, Any]:
        """Przetworz zadanie i zwróć wynik"""
        pass


class TaskTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start_timer(self):
        self.start_time = time.time()

    def end_timer(self):
        self.end_time = time.time()

    def get_processing_time(self) -> float:
        if self.end_time is None:
            self.end_timer()

        return self.end_time - self.start_time



# %% Concrete Strategies - DO IMPLEMENTACJI
# WZORZEC: Concrete Strategy (konkretna strategia)

# TODO: Zaimplementuj klasę UrgentTaskProcessor
# Dziedziczy po TaskProcessor
# Metoda process_task(task: WorkflowTask) -> Dict[str, Any]:
#   - Zapisz start time (time.time())
#   - Walidacja: sprawdź czy task.priority == URGENT i description nie jest puste
#   - Natychmiastowe przetwarzanie (bez delay, bez time.sleep)
#   - Oznacz zadanie jako completed (task.mark_completed())
#   - Zwróć dict z kluczami: "status" (str), "processing_time" (float), "strategy_used" (str = "urgent"), "validation_passed" (bool)

class UrgentTaskProcessor(TaskProcessor, TaskTimer):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return Strategies.URGENT.value

    def validate_task(self, task: WorkflowTask) -> bool:
        return bool(task.priority == TaskPriority.URGENT and task.description)

    def process_task(self, task: WorkflowTask) -> Dict[str, Any]:
        self.start_timer()

        validation_passed = self.validate_task(task)
        task.mark_completed()

        return {
            'status': task.get_status(),
            'processing_time': self.get_processing_time(),
            'strategy_used': str(self),
            'validation_passed': validation_passed
        }


# TODO: Zaimplementuj klasę StandardTaskProcessor
# Dziedziczy po TaskProcessor
# Metoda process_task(task: WorkflowTask) -> Dict[str, Any]:
#   - Zapisz start time (time.time())
#   - Walidacja: sprawdź czy title ma przynajmniej 3 znaki
#   - Symuluj przetwarzanie: time.sleep(1)
#   - Oznacz zadanie jako completed (task.mark_completed())
#   - Zwróć dict z kluczami: "status" (str), "processing_time" (float), "strategy_used" (str = "standard"), "validation_passed" (bool)

class StandardTaskProcessor(TaskProcessor, TaskTimer):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return Strategies.STANDARD.value

    def validate_task(self, task: WorkflowTask) -> bool:
        return task.title and len(task.title) >= 3

    def process_task(self, task: WorkflowTask) -> Dict[str, Any]:
        self.start_timer()

        time.sleep(1)
        validation_passed = self.validate_task(task)
        task.mark_completed()

        return {
            'status': task.get_status(),
            'processing_time': self.get_processing_time(),
            'strategy_used': str(self),
            'validation_passed': validation_passed
        }


# TODO: Zaimplementuj klasę BackgroundTaskProcessor
# Dziedziczy po TaskProcessor
# Metoda process_task(task: WorkflowTask) -> Dict[str, Any]:
#   - Zapisz start time (time.time())
#   - Walidacja: sprawdź czy priority != URGENT (zadania pilne nie mogą być w tle)
#   - Symuluj wolne przetwarzanie: time.sleep(0.1)
#   - Oznacz zadanie jako completed (task.mark_completed())
#   - Zwróć dict z kluczami: "status" (str), "processing_time" (float), "strategy_used" (str = "background"), "validation_passed" (bool)

class BackgroundTaskProcessor(TaskProcessor, TaskTimer):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return Strategies.BACKGROUND.value

    def validate_task(self, task: WorkflowTask) -> bool:
        return task.priority != TaskPriority.URGENT

    def process_task(self, task: WorkflowTask) -> Dict[str, Any]:
        self.start_timer()

        validation_passed = self.validate_task(task)
        time.sleep(0.1)
        task.mark_completed()

        return {
            'status': task.get_status(),
            'processing_time': self.get_processing_time(),
            'strategy_used': str(self),
            'validation_passed': validation_passed
        }


# %% Context - DO IMPLEMENTACJI
# WZORZEC: Context (kontekst używający strategii)

# TODO: Zaimplementuj klasę TaskManager
# Konstruktor przyjmuje strategy: TaskProcessor = None (opcjonalna strategia)
#   - Przechowuje strategię jako self.strategy
#
# Metoda set_strategy(strategy: TaskProcessor) -> None:
#   - Ustawia nową strategię przetwarzania (self.strategy = strategy)
#
# Metoda execute_task(task: WorkflowTask) -> Dict[str, Any]:
#   - Sprawdza czy strategia jest ustawiona (jeśli nie - raise ValueError("No strategy set"))
#   - Deleguje do self.strategy.process_task(task)
#   - Zwraca wynik z process_task()

class TaskManager:
    def __init__(self, strategy: TaskProcessor | None = None):
        self.strategy = strategy

    def set_strategy(self, strategy: TaskProcessor) -> None:
        self.strategy = strategy

    def execute_task(self, task: WorkflowTask) -> Dict[str, Any]:
        if not self.strategy or str(self.strategy) not in Strategies.get_values():
            raise ValueError(f'No strategy set')

        return self.strategy.process_task(task)
