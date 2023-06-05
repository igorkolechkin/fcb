from copying_files import copying_files
from format_card import format_card
from main_window import App


def on_format(question) -> None:
    answer = question()
    print(f'Format: {answer}')


def main() -> None:
    app = App()
    app.copying_files = copying_files
    app.format_card = format_card

    app.mainloop()


if __name__ == '__main__':
    main()
