import tkinter as tk
from tkinter import ttk, messagebox
from api_client import get_rate
from history_manager import load, save

CURRENCIES = ['USD', 'EUR', 'RUB', 'GBP', 'JPY']

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Currency Converter')

        ttk.Label(root, text='Из:').grid(row=0, column=0)
        self.from_var = tk.StringVar(value='USD')
        ttk.Combobox(root, textvariable=self.from_var, values=CURRENCIES, state='readonly').grid(row=0, column=1)

        ttk.Label(root, text='В:').grid(row=0, column=2)
        self.to_var = tk.StringVar(value='EUR')
        ttk.Combobox(root, textvariable=self.to_var, values=CURRENCIES, state='readonly').grid(row=0, column=3)

        ttk.Label(root, text='Сумма:').grid(row=1, column=0)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=1, column=1)

        ttk.Button(root, text='Конвертировать', command=self.convert).grid(row=1, column=2, columnspan=2)

        self.tree = ttk.Treeview(root, columns=('from', 'to', 'amount', 'result'), show='headings')
        self.tree.heading('from', text='Из')
        self.tree.heading('to', text='В')
        self.tree.heading('amount', text='Сумма')
        self.tree.heading('result', text='Результат')
        self.tree.grid(row=2, column=0, columnspan=4, sticky='nsew')

        for e in load():
            self.tree.insert('', 'end', values=(e['from'], e['to'], e['amount'], f"{e['result']:.2f}"))

    def convert(self):
        from_cur = self.from_var.get()
        to_cur = self.to_var.get()
        amt_str = self.amount_entry.get()

        if not amt_str:
            messagebox.showerror('Ошибка', 'Введите сумму')
            return
        try:
            amt = float(amt_str)
        except ValueError:
            messagebox.showerror('Ошибка', 'Сумма должна быть числом')
            return
        if amt <= 0:
            messagebox.showerror('Ошибка', 'Сумма должна быть положительной')
            return

        try:
            rate = get_rate(from_cur, to_cur)
            result = amt * rate
        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось получить курс: {e}')
            return

        entry = {'from': from_cur, 'to': to_cur, 'amount': amt, 'result': result}
        save(entry)
        self.tree.insert('', 'end', values=(from_cur, to_cur, amt, f'{result:.2f}'))
        messagebox.showinfo('Результат', f'{amt} {from_cur} = {result:.2f} {to_cur}')

if __name__ == '__main__':
    root = tk.Tk()
    App(root)
    root.mainloop()
