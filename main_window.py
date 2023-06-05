import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import configparser


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.app_width: int = 600
        self.app_height: int = 400
        self.app_x: int = (self.winfo_screenwidth() - self.app_width) // 2
        self.app_y: int = (self.winfo_screenheight() - self.app_height) // 2
        self.configure_window()

        self.config = configparser.ConfigParser()
        self.config_file = 'config.ini'

        self.copying_files = None
        self.format_card = None

        self.button_style = self.styles_configurate()

        self.format_button = None
        self.card_path_field = None
        self.save_path_field = None

        self.create_blocks()

    def configure_window(self) -> None:
        self.geometry(f'{self.app_width}x{self.app_height}+{self.app_x}+{self.app_y}')
        self.title('Funny Bees copy')
        self.resizable(False, False)

    def styles_configurate(self) -> tk.ttk.Style:
        style = ttk.Style(self)
        style.configure('TButton', borderwidth=0, background='#007bff', foreground='#fff', font=('Arial', 15))
        style.configure('TLabel', font=('Arial', 18))
        style.configure('Big.TButton', font=('Arial', 19), padding=8)
        style.map('TButton', background=[('active', '#0056b3')])

        return style

    def create_blocks(self) -> None:
        path_block = ttk.Frame(self, padding='20 30')
        path_block.grid_columnconfigure(0, weight=1)
        path_block.pack(fill='both')

        action_block = ttk.Frame(self, padding='20 50')
        action_block.grid_columnconfigure(0, weight=1, uniform="equal")
        action_block.grid_columnconfigure(1, weight=1, uniform="equal")
        action_block.pack(fill='both')

        self.path_block_elements(path_block)
        self.action_block_elements(action_block)

    def path_block_elements(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text='Путь к карте:').grid(row=0, column=0, sticky='w', pady='0 10')

        self.card_path_field = ttk.Entry(parent, width=20, font=('Arial', 16))
        self.set_field_from_start(self.card_path_field, 'card_path')
        self.card_path_field.grid(row=1, column=0, padx='0 20', sticky='we')

        ttk.Button(parent, text='Изменить', command=lambda: self.change_path(self.card_path_field, 'card_path'))\
            .grid(row=1, column=1)

        ttk.Label(parent, text='Путь куда сохранять:').grid(row=2, column=0, sticky='w', pady='30 10')

        self.save_path_field = ttk.Entry(parent, width=20, font=('Arial', 16))
        self.set_field_from_start(self.save_path_field, 'save_path')
        self.save_path_field.grid(row=3, column=0, padx='0 20', sticky='we')
        ttk.Button(parent, text='Изменить', command=lambda: self.change_path(self.save_path_field, 'save_path'))\
            .grid(row=3, column=1)

    def action_block_elements(self, parent: ttk.Frame) -> None:
        ttk.Button(parent, text='Копировать', command=lambda: self.on_copy(), style='Big.TButton')\
            .grid(row=0, column=0, sticky="w")

        ttk.Button(parent, text='Форматировать', command=lambda: self.on_format(), style='Big.TButton')\
            .grid(row=0, column=1, sticky="e")

    def on_format(self) -> None:
        warning = messagebox.askokcancel(message='Форматировать карту?')

        if not warning:
            return

        result = self.format_card(self.card_path_field.get())
        self.action_message(result)

    def on_copy(self) -> None:
        card_path = self.card_path_field.get()
        save_path = self.save_path_field.get()

        if len(card_path) == 0:
            messagebox.showerror(title='Ошибка!', message='Укажите путь к карте памяти!')
            return
        elif len(save_path) == 0:
            messagebox.showerror(title='Ошибка!', message='Укажите путь, куда копировать изображения!')
            return

        result = self.copying_files({'card_path': card_path, 'save_path': save_path})
        self.action_message(result)

    def change_path(self, field: ttk.Entry, field_name: str) -> None:
        selected_folder = filedialog.askdirectory()
        field.delete(0, tk.END)
        field.insert(0, selected_folder)

        self.save_path_to_config(field_name, selected_folder)

    def save_path_to_config(self, field_name: str, path: str) -> None:
        try:
            self.config.read(self.config_file)
            self.config.set('Path fields', field_name, path)

            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
        except Exception as error:
            print(error)

    def set_field_from_start(self, field: ttk.Entry, name: str) -> None:
        try:
            self.config.read(self.config_file)
            path = self.config.get('Path fields', name)

            field.delete(0, tk.END)
            field.insert(0, path)
        except Exception as error:
            print(error)

    def action_message(self, result: dict) -> None:
        if result['status'] == 'error':
            messagebox.showerror(title='Ошибка!', message=result['text'])
        else:
            messagebox.showinfo(message=result['text'])