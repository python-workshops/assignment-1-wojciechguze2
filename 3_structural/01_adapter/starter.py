"""
Adapter Pattern - Payment Systems Integration
Zaimplementuj wzorzec Adapter do integracji różnych systemów płatności.

Adaptery konwertują niekompatybilne interfejsy zewnętrznych API na wspólny interfejs PaymentProcessor.

Examples:
    >>> # Test PayPal adapter
    >>> paypal_service = PayPalService()
    >>> adapter = PayPalAdapter(paypal_service)
    >>> result = adapter.process_payment(100.50, "USD")
    >>> result["status"]
    'success'
    >>> len(result["transaction_id"]) > 0
    True

    >>> # Test Stripe adapter
    >>> stripe_service = StripeService()
    >>> adapter = StripeAdapter(stripe_service)
    >>> result = adapter.process_payment(50.00, "EUR")
    >>> result["status"]
    'success'

    >>> # Test Przelewy24 adapter
    >>> p24_service = Przelewy24Service()
    >>> adapter = Przelewy24Adapter(p24_service)
    >>> result = adapter.process_payment(200.00, "PLN")
    >>> result["status"]
    'success'
"""
# %% About
# - Name: Adapter - Payment Systems Integration
# - Difficulty: easy
# - Lines: 15
# - Minutes: 12
# - Focus: Wzorzec Adapter

# %% Description

from abc import ABC, abstractmethod
import uuid
import random

# %% Hints
# - Każdy adapter implementuje PaymentProcessor
# - Adapter zawiera instancję zewnętrznego serwisu (kompozycja)
# - PayPal wymaga kwoty w centach (amount * 100)
# - Konwertuj odpowiedzi do formatu: {"status": "success/failed", "transaction_id": "..."}

# %% Run
# - PyCharm: right-click and `Run Doctest in ...`
# - Terminal: `python -m doctest -f -v starter.py`
# - Tests: `python -m pytest test_adapter.py -v`


# %% STEP 1: Mock External APIs - GOTOWE (nie modyfikuj)
# Te klasy symulują zewnętrzne API płatności - każde ma INNY interfejs

class PayPalService:
    """
    Mock PayPal API - GOTOWE

    Interfejs: make_payment(amount_cents: int, currency: str)
    Zwraca: {"payment_id": str, "status_code": int}
    """
    def make_payment(self, amount_cents: int, currency: str) -> dict:
        return {
            "payment_id": f"PAYPAL_{random.randint(1000, 9999)}",
            "status_code": 200 if amount_cents > 0 else 400
        }


class StripeService:
    """
    Mock Stripe API - GOTOWE

    Interfejs: charge(amount: float, currency: str, source: str)
    Zwraca: {"id": str, "paid": bool, "amount": float}
    """
    def charge(self, amount: float, currency: str, source: str = "card_token") -> dict:
        return {
            "id": f"ch_{uuid.uuid4().hex[:8]}",
            "paid": amount > 0,
            "amount": amount
        }


class Przelewy24Service:
    """
    Mock Przelewy24 API - GOTOWE

    Interfejs: create_transaction(amount: float, currency: str, merchant_id: str)
    Zwraca: {"transactionId": int, "success": bool}
    """
    def create_transaction(self, amount: float, currency: str, merchant_id: str = "12345") -> dict:
        return {
            "transactionId": random.randint(100000, 999999),
            "success": amount > 0 and currency == "PLN"
        }


# %% STEP 2: Target Interface - GOTOWE (nie modyfikuj)
# WZORZEC: Target (interfejs docelowy oczekiwany przez klienta)

class PaymentProcessor(ABC):
    """
    Wspólny interfejs dla wszystkich systemów płatności - GOTOWE

    To jest Target interface - wszystkie adaptery muszą go implementować.
    """

    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> dict:
        """
        Przetwórz płatność i zwróć standardową odpowiedź

        Args:
            amount: Kwota płatności
            currency: Waluta (USD, EUR, PLN)

        Returns:
            dict: {"status": "success/failed", "transaction_id": "..."}
        """
        pass


# %% STEP 3: PayPal Adapter - DO IMPLEMENTACJI
# WZORZEC: Adapter (adaptuje PayPalService do PaymentProcessor)

# TODO: Zaimplementuj klasę PayPalAdapter
#
# Klasa adaptuje PayPalService do interfejsu PaymentProcessor
#
# Dziedziczenie: PayPalAdapter(PaymentProcessor)
#
# Konstruktor __init__(self, paypal_service: PayPalService):
#   - Zapisz paypal_service jako self.paypal_service
#
# Metoda process_payment(self, amount: float, currency: str) -> dict:
#   - Konwertuj amount do centów: amount_cents = int(amount * 100)
#   - Wywołaj self.paypal_service.make_payment(amount_cents, currency)
#   - Sprawdź status_code w odpowiedzi
#   - Jeśli status_code == 200:
#       zwróć {"status": "success", "transaction_id": payment_id}
#   - W przeciwnym razie:
#       zwróć {"status": "failed", "transaction_id": None}


class PayPalAdapter(PaymentProcessor):
    def __init__(self, paypal_service: PayPalService):
        self.paypal_service = paypal_service

    def process_payment(self, amount: float, currency: str) -> dict:
        amount = int(amount * 100)

        response = self.paypal_service.make_payment(amount, currency)

        match response['status_code']:
            case 200:
                return {
                    'status': 'success',
                    'transaction_id': response['payment_id'],
                }
            case _:
                return {
                    'status': 'failed',
                    'transaction_id': None
                }


# %% STEP 4: Stripe Adapter - DO IMPLEMENTACJI
# WZORZEC: Adapter (adaptuje StripeService do PaymentProcessor)

# TODO: Zaimplementuj klasę StripeAdapter
#
# Klasa adaptuje StripeService do interfejsu PaymentProcessor
#
# Dziedziczenie: StripeAdapter(PaymentProcessor)
#
# Konstruktor __init__(self, stripe_service: StripeService):
#   - Zapisz stripe_service jako self.stripe_service
#
# Metoda process_payment(self, amount: float, currency: str) -> dict:
#   - Wywołaj self.stripe_service.charge(amount, currency)
#   - Sprawdź pole "paid" w odpowiedzi
#   - Jeśli paid == True:
#       zwróć {"status": "success", "transaction_id": id}
#   - W przeciwnym razie:
#       zwróć {"status": "failed", "transaction_id": None}


class StripeAdapter(PaymentProcessor):
    def __init__(self, stripe_service: StripeService):
        self.stripe_service = stripe_service

    def process_payment(self, amount: float, currency: str) -> dict:
        response = self.stripe_service.charge(amount, currency)

        match response['paid']:
            case True:
                return {
                    'status': 'success',
                    'transaction_id': response['id'],
                }
            case _:
                return {
                    'status': False,
                    'transaction_id': None
                }


# %% STEP 5: Przelewy24 Adapter - DO IMPLEMENTACJI
# WZORZEC: Adapter (adaptuje Przelewy24Service do PaymentProcessor)

# TODO: Zaimplementuj klasę Przelewy24Adapter
#
# Klasa adaptuje Przelewy24Service do interfejsu PaymentProcessor
#
# Dziedziczenie: Przelewy24Adapter(PaymentProcessor)
#
# Konstruktor __init__(self, p24_service: Przelewy24Service):
#   - Zapisz p24_service jako self.p24_service
#
# Metoda process_payment(self, amount: float, currency: str) -> dict:
#   - Wywołaj self.p24_service.create_transaction(amount, currency)
#   - Sprawdź pole "success" w odpowiedzi
#   - Jeśli success == True:
#       zwróć {"status": "success", "transaction_id": str(transactionId)}
#   - W przeciwnym razie:
#       zwróć {"status": "failed", "transaction_id": None}


class Przelewy24Adapter(PaymentProcessor):
    def __init__(self, p24_service: Przelewy24Service):
        self.p24_service = p24_service

    def process_payment(self, amount: float, currency: str) -> dict:
        response = self.p24_service.create_transaction(amount, currency)

        match response['success']:
            case True:
                return {
                    'status': 'success',
                    'transaction_id': str(response['transactionId']),
                }
            case _:
                return {
                    'status': 'failed',
                    'transaction_id': None
                }


# %% Example Usage
# Odkomentuj gdy zaimplementujesz
# if __name__ == "__main__":
#     # Klient używa tylko interfejsu PaymentProcessor
#     paypal = PayPalAdapter(PayPalService())
#     stripe = StripeAdapter(StripeService())
#     p24 = Przelewy24Adapter(Przelewy24Service())
#
#     # Ten sam interfejs dla wszystkich!
#     print(paypal.process_payment(100.50, "USD"))
#     print(stripe.process_payment(50.00, "EUR"))
#     print(p24.process_payment(200.00, "PLN"))
