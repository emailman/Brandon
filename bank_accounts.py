"""
OOP Basics: Bank Account Hierarchy
Demonstrates: abstraction, encapsulation, inheritance, polymorphism
"""

from abc import ABC, abstractmethod
from datetime import date, timedelta


# ── Abstract Base Class ─────────────────────────────────────────────────

class BankAccount(ABC):
    """All account types share this interface."""

    _next_account_number = 1001

    def __init__(self, owner: str, initial_deposit: float = 0.0):
        self._account_number = BankAccount._next_account_number
        BankAccount._next_account_number += 1
        self._owner = owner
        self._balance = 0.0
        self._transactions: list[str] = []
        if initial_deposit > 0:
            self.deposit(initial_deposit)

    # ── Properties (encapsulation) ──────────────────────────────────────

    @property
    def account_number(self) -> int:
        return self._account_number

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def balance(self) -> float:
        return self._balance

    # ── Concrete shared methods ─────────────────────────────────────────

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        self._log(f"Deposit      +${amount:>12,.2f}  "
                  f"balance: ${self._balance:,.2f}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError(f"Insufficient funds "
                             f"(balance: ${self._balance:.2f}).")
        self._balance -= amount
        self._log(f"Withdrawal   -${amount:>12,.2f}  "
                  f"balance: ${self._balance:,.2f}")

    def print_statement(self) -> None:
        line = "-" * 52
        print(f"\n{line}")
        print(f"  {self.__class__.__name__}  #{self._account_number}  "
              f"--  {self._owner}")
        print(line)
        for entry in self._transactions:
            print(f"  {entry}")
        print(line)
        print(f"  Current balance: ${self._balance:>12,.2f}")
        print(line)

    def _log(self, message: str) -> None:
        self._transactions.append(message)

    # ── Abstract method (subclasses must implement) ─────────────────────

    @abstractmethod
    def account_summary(self) -> str:
        """Return a one-line description of the account's key terms."""


# ── Checking Account ────────────────────────────────────────────────────

class CheckingAccount(BankAccount):
    """No interest. Optional overdraft limit backed by a fee."""

    def __init__(self, owner: str, initial_deposit: float = 0.0,
                 overdraft_limit: float = 0.0):
        self._overdraft_limit = overdraft_limit
        super().__init__(owner, initial_deposit)

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        available = self._balance + self._overdraft_limit
        if amount > available:
            raise ValueError(
                f"Exceeds overdraft limit (available: ${available:,.2f})."
            )
        if amount > self._balance:
            fee = 35.00
            self._balance -= amount + fee
            self._log(
                f"Withdrawal   -${amount:>12,.2f}  "
                f"balance: ${self._balance:,.2f}"
                f"  [overdraft fee -${fee:,.2f}]"
            )
        else:
            super().withdraw(amount)

    def account_summary(self) -> str:
        od = f"overdraft limit: ${self._overdraft_limit:,.2f}" \
            if self._overdraft_limit else "no overdraft"
        return (f"Checking #{self._account_number} | {od} | "
                f"balance: ${self._balance:,.2f}")


# ── Savings Account ─────────────────────────────────────────────────────

class SavingsAccount(BankAccount):
    """Variable interest rate; call apply_monthly_interest() each month."""

    def __init__(self, owner: str, initial_deposit: float = 0.0,
                 annual_rate: float = 0.04):
        self._annual_rate = annual_rate
        super().__init__(owner, initial_deposit)

    @property
    def annual_rate(self) -> float:
        return self._annual_rate

    @annual_rate.setter
    def annual_rate(self, new_rate: float) -> None:
        if new_rate < 0:
            raise ValueError("Interest rate cannot be negative.")
        old = self._annual_rate
        self._annual_rate = new_rate
        self._log(f"Rate change  APY {old:.2%} -> {new_rate:.2%}")

    def apply_monthly_interest(self) -> None:
        interest = self._balance * (self._annual_rate / 12)
        self._balance += interest
        self._log(
            f"Interest     +${interest:>10.4f}  "
            f"balance: ${self._balance:,.2f}"
            f"  (APY {self._annual_rate:.2%})"
        )

    def account_summary(self) -> str:
        return (f"Savings #{self._account_number} | "
                f"APY {self._annual_rate:.2%} "
                f"| balance: ${self._balance:.2f}")


# ── Certificate of Deposit ──────────────────────────────────────────────

class CD(BankAccount):
    """Fixed rate and term. Early withdrawal incurs a penalty."""

    EARLY_WITHDRAWAL_PENALTY_MONTHS = 6

    def __init__(self, owner: str, principal: float,
                 annual_rate: float, term_months: int):
        if principal <= 0:
            raise ValueError("CD principal must be positive.")
        self._annual_rate = annual_rate
        self._term_months = term_months
        self._open_date = date.today()
        self._maturity_date = (self._open_date +
                               timedelta(days=term_months * 30))
        super().__init__(owner, principal)

    @property
    def maturity_date(self) -> date:
        return self._maturity_date

    @property
    def is_mature(self) -> bool:
        return date.today() >= self._maturity_date

    # CDs don't accept arbitrary deposits after opening
    def deposit(self, amount: float) -> None:
        if self._transactions:          # already opened
            raise PermissionError("Cannot add funds to an open CD.")
        super().deposit(amount)

    def withdraw(self, amount: float) -> None:
        if not self.is_mature:
            penalty_rate = ((self._annual_rate / 12) *
                            self.EARLY_WITHDRAWAL_PENALTY_MONTHS)
            penalty = self._balance * penalty_rate
            print(f"  [!] Early withdrawal penalty: ${penalty:.2f}")
            self._balance -= penalty
            self._log(f"Early penalty-${penalty:>12,.2f}  "
                      f"balance: ${self._balance:,.2f}")
        super().withdraw(amount)

    def apply_monthly_interest(self) -> None:
        interest = self._balance * (self._annual_rate / 12)
        self._balance += interest
        self._log(
            f"Interest     +${interest:>10.4f}  "
            f"balance: ${self._balance:,.2f}"
            f"  (APY {self._annual_rate:,.2%})"
        )

    def account_summary(self) -> str:
        status = "matured" if self.is_mature else \
            f"matures {self._maturity_date}"
        return (f"CD #{self._account_number} | "
                f"APY {self._annual_rate:.2%} "
                f"| {self._term_months}-month term | {status} "
                f"| balance: ${self._balance:,.2f}")


# ── Demo ────────────────────────────────────────────────────────────────

def main():
    print("=" * 52)
    print("  OOP Bank Account Demo")
    print("=" * 52)

    # --- Checking ---
    checking = CheckingAccount("Alice",
                               initial_deposit=1_000.00,
                               overdraft_limit=200.00)
    checking.deposit(500.00)
    checking.withdraw(200.00)
    try:
        checking.withdraw(2_000.00)  # should fail — over overdraft limit
    except ValueError as e:
        print(f"  [Checking] {e}")
    checking.print_statement()

    # --- Savings ---
    savings = SavingsAccount("Bob",
                             initial_deposit=5_000.00,
                             annual_rate=0.045)
    savings.deposit(1_000.00)
    savings.apply_monthly_interest()
    savings.annual_rate = 0.05  # rate change (variable)
    savings.apply_monthly_interest()
    savings.withdraw(500.00)
    savings.print_statement()

    # --- CD ---
    cd = CD("Carol",
            principal=10_000.00,
            annual_rate=0.052,
            term_months=12)
    # Simulate 3 months of interest
    for _ in range(3):
        cd.apply_monthly_interest()
    try:
        cd.deposit(500.00)  # should fail — CDs are closed after opening
    except PermissionError as e:
        print(f"\n  [CD] {e}")
    cd.withdraw(2_000.00)  # early — penalty applies
    cd.print_statement()

    # --- Polymorphism: treat all accounts the same way ---
    print("\n  Account Summaries (polymorphism)")
    print("  " + "-" * 48)
    accounts: list[BankAccount] = [checking, savings, cd]
    for acct in accounts:
        # each type formats its own summary
        print(f"  {acct.account_summary()}")


if __name__ == "__main__":
    main()
