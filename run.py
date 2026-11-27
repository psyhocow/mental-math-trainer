"""Launch the Mental Math Trainer desktop application."""

from mental_math.ui import MentalMathApp


def main() -> None:
    app = MentalMathApp()
    app.mainloop()


if __name__ == "__main__":
    main()
