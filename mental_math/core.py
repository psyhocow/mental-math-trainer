"""Question generation and guided mental arithmetic examples."""

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Question:
    prompt: str
    answer: int
    hint_key: str


@dataclass(frozen=True)
class FormulaQuestion:
    prompt: str
    answer: str
    choices: tuple[str, ...]
    hint_key: str


def make_question(difficulty: str) -> Question:
    """Create a non-negative arithmetic question for the selected level."""
    if difficulty == "easy":
        left, right = random.randint(0, 20), random.randint(0, 20)
        operation = random.choice(("+", "−"))
        if operation == "−" and right > left:
            left, right = right, left
        answer = left + right if operation == "+" else left - right
        hint_key = "hint_easy"
    elif difficulty == "normal":
        operation = random.choice(("+", "−", "×", "÷"))
        if operation == "+":
            left, right = random.randint(10, 99), random.randint(10, 99)
            answer = left + right
        elif operation == "−":
            left, right = sorted((random.randint(10, 99), random.randint(10, 99)), reverse=True)
            answer = left - right
        elif operation == "×":
            left, right = random.randint(2, 12), random.randint(2, 12)
            answer = left * right
        else:
            right = random.randint(2, 12)
            answer = random.randint(2, 12)
            left = right * answer
        hint_key = "hint_normal"
    else:
        operation = random.choice(("+", "−", "×", "÷"))
        if operation == "+":
            left, right = random.randint(100, 999), random.randint(100, 999)
            answer = left + right
        elif operation == "−":
            left, right = sorted((random.randint(100, 999), random.randint(100, 999)), reverse=True)
            answer = left - right
        elif operation == "×":
            left, right = random.randint(12, 99), random.randint(2, 12)
            answer = left * right
        else:
            right = random.randint(2, 12)
            answer = random.randint(12, 99)
            left = right * answer
        hint_key = "hint_hard"

    return Question(f"{left} {operation} {right} = ?", answer, hint_key)


def tutorial_questions() -> tuple[Question, ...]:
    """A short, fixed sequence that introduces useful mental strategies."""
    return (
        Question("3 + 2 = ?", 5, "tutorial_hint_1"),
        Question("8 + 5 = ?", 13, "tutorial_hint_2"),
        Question("14 − 6 = ?", 8, "tutorial_hint_3"),
        Question("4 × 3 = ?", 12, "tutorial_hint_4"),
        Question("20 ÷ 5 = ?", 4, "tutorial_hint_5"),
        Question("19 + 6 = ?", 25, "tutorial_hint_6"),
    )


def make_formula_question() -> FormulaQuestion:
    """Choose one of the three core abbreviated multiplication identities."""
    formulas = (
        FormulaQuestion(
            "a² − b² = ?",
            "(a − b)(a + b)",
            ("(a − b)(a + b)", "(a − b)²", "a² + b²", "(a + b)²"),
            "fsu_hint_difference",
        ),
        FormulaQuestion(
            "(a + b)² = ?",
            "a² + 2ab + b²",
            ("a² + 2ab + b²", "a² + b²", "a² − 2ab + b²", "(a − b)(a + b)"),
            "fsu_hint_sum_square",
        ),
        FormulaQuestion(
            "(a − b)² = ?",
            "a² − 2ab + b²",
            ("a² − 2ab + b²", "a² + 2ab + b²", "a² − b²", "(a − b)(a + b)"),
            "fsu_hint_difference_square",
        ),
    )
    selected = random.choice(formulas)
    choices = list(selected.choices)
    random.shuffle(choices)
    return FormulaQuestion(selected.prompt, selected.answer, tuple(choices), selected.hint_key)
