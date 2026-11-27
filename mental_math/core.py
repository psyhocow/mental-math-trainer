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


@dataclass(frozen=True)
class Topic:
    id: str
    title: str
    description: str
    stage: int


# Ordered progression from number bonds to applied mental arithmetic. Topic
# metadata drives both question generation and the mastery path in the UI.
CURRICULUM = (
    Topic("bonds_10", "Number bonds · within 10", "Addition and subtraction facts", 1),
    Topic("teens_no_bridge", "Teens · no regrouping", "Add or subtract without crossing 10", 2),
    Topic("teens_bridge", "Bridge through 10", "Regrouping with numbers up to 20", 3),
    Topic("round_tens", "Round tens · within 100", "Add and subtract multiples of ten", 4),
    Topic("hundred_no_bridge", "Within 100 · no regrouping", "Two digit operations without carrying or borrowing", 5),
    Topic("hundred_bridge", "Within 100 · regrouping", "Carry and borrow across tens", 6),
    Topic("tables", "Multiplication tables · 1–10", "Multiplication and inverse division facts", 7),
    Topic("beyond_tables", "Beyond tables · within 100", "Distributive multiplication and exact division", 8),
    Topic("thousands", "Larger numbers · within 1,000", "Place value and multi-step arithmetic", 9),
    Topic("shortcuts", "Shortcuts · applied arithmetic", "Multiplication shortcuts, squares, percentages, fractions, and decimals", 10),
)


def make_topic_question(topic_id: str, band: int = 0) -> Question:
    """Construct a fresh integer problem satisfying the selected topic rules."""
    if topic_id == "bonds_10":
        op = random.choice(("+", "−")); maximum = min(9, 4 + max(0, band) * 2); a = random.randint(2, maximum); b = random.randint(2, 10-a) if op == "+" else random.randint(2, a)
    elif topic_id == "teens_no_bridge":
        op = random.choice(("+", "−"))
        if op == "+": a = random.randint(11, min(17, 13 + band * 2)); b = random.randint(2, min(9, 19-a))
        else: a = random.randint(12, 19); b = random.randint(2, min(9, a % 10))
    elif topic_id == "teens_bridge":
        op = random.choice(("+", "−"))
        if op == "+": a = random.randint(2, 9); b = random.randint(11-a, 20-a)
        else: a = random.randint(11, 18); b = random.randint(a % 10 + 1, min(9, a-1))
    elif topic_id == "round_tens":
        op = random.choice(("+", "−")); a = random.randrange(20, min(100, 60 + band * 20), 10); b = random.randrange(10, (100-a if op == "+" else a)+1, 10)
    elif topic_id in {"hundred_no_bridge", "hundred_bridge"}:
        op = random.choice(("+", "−")); carry = topic_id == "hundred_bridge"
        if op == "+":
            a = random.randint(20, min(79, 49 + band * 15))
            candidates = [value for value in range(11, min(99-a, 89)+1) if ((a % 10 + value % 10 >= 10) == carry)]
            if not candidates: return make_topic_question(topic_id)
            b = random.choice(candidates)
        else:
            a = random.randint(21, 99)
            candidates = [value for value in range(11, a) if ((a % 10 < value % 10) == carry)]
            if not candidates: return make_topic_question(topic_id)
            b = random.choice(candidates)
    elif topic_id == "tables":
        op = random.choice(("×", "÷")); lower, upper = ((2, 5) if band == 0 else (2, 10) if band == 1 else (6, 10)); a = random.randint(lower, upper); b = random.randint(lower, upper)
        if op == "÷": a, b = a*b, b
    elif topic_id == "beyond_tables":
        op = random.choice(("×", "÷"))
        if op == "×": a = random.randint(11, 19); b = random.randint(2, 5)
        else:
            b = random.randint(3, 9); a = b * random.randint(2, 11)
    elif topic_id == "thousands":
        op = random.choice(("+", "−", "×", "÷"))
        if op == "+":
            a = random.randint(100, 899); b = random.randint(100, 999-a)
        elif op == "−": a, b = random.randint(200, 999), random.randint(100, 199)
        elif op == "×": a, b = random.randint(10, 99), random.choice((10, 100))
        else: b = random.choice((10, 100)); a = b * random.randint(10, 99)
    elif topic_id == "shortcuts":
        kind = random.choice(("shortcut", "square", "percent", "fraction", "decimal"))
        if kind == "shortcut":
            a, b = random.randint(2, 20 + band * 20), random.choice((5, 9, 11, 25))
            return Question(f"{a} × {b} = ?", a * b, "hint_normal")
        if kind == "square":
            a = random.randint(2, 9) * 10 + 5
            return Question(f"{a}² = ?", a * a, "hint_normal")
        if kind == "percent":
            percent = random.choice((10, 25, 50, 75))
            whole = random.randint(1, 20 + band * 20) * 4
            return Question(f"{percent}% of {whole} = ?", whole * percent // 100, "hint_normal")
        if kind == "fraction":
            numerator, denominator = random.choice(((1, 2), (1, 4), (3, 4)))
            whole = random.randint(2, 20 + band * 10) * denominator
            return Question(f"{numerator}/{denominator} of {whole} = ?", whole * numerator // denominator, "hint_normal")
        whole = random.randint(1, 9 + band * 5)
        return Question(f"{whole}.5 + 0.5 = ?", whole + 1, "hint_normal")
    else:
        raise ValueError(f"Unknown curriculum topic: {topic_id}")
    result = a+b if op == "+" else a-b if op == "−" else a*b if op == "×" else a//b
    return Question(f"{a} {op} {b} = ?", result, "hint_normal")


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
