import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Основное окно
root = tk.Tk()
root.title("Book Tracker")
root.geometry("700x600")

# Переменные для полей ввода
title_var = tk.StringVar()
author_var = tk.StringVar()
genre_var = tk.StringVar()
pages_var = tk.StringVar()

# Создаем поля для ввода данных
tk.Label(root, text="Название книги").grid(row=0, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=title_var, width=30).grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Автор").grid(row=1, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=author_var, width=30).grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Жанр").grid(row=2, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=genre_var, width=30).grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Количество страниц").grid(row=3, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=pages_var, width=10).grid(row=3, column=1, padx=5, pady=5, sticky='w')

# Список для хранения данных книг
books = []

# Создаем таблицу для отображения книг
columns = ("Название", "Автор", "Жанр", "Страницы")
tree = ttk.Treeview(root, columns=columns, show='headings', height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.grid(row=5, column=0, columnspan=4, padx=5, pady=10)

# Функция для очистки полей ввода
def clear_fields():
    title_var.set("")
    author_var.set("")
    genre_var.set("")
    pages_var.set("")

# Функция добавления книги
def add_book():
    title = title_var.get().strip()
    author = author_var.get().strip()
    genre = genre_var.get().strip()
    pages = pages_var.get().strip()

    # Проверка корректности
    if not title or not author or not genre or not pages:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
        return
    if not pages.isdigit():
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
        return

    book = {
        "Название": title,
        "Автор": author,
        "Жанр": genre,
        "Страницы": int(pages)
    }
    books.append(book)
    tree.insert('', tk.END, values=(title, author, genre, pages))
    clear_fields()

# Кнопка добавления книги
tk.Button(root, text="Добавить книгу", command=add_book).grid(row=4, column=0, columnspan=2, pady=10)

# --- Фильтрация ---
filter_genre_var = tk.StringVar()
filter_pages_greater_than_var = tk.StringVar()

tk.Label(root, text="Фильтр по жанру").grid(row=6, column=0, padx=5, pady=5, sticky='w')
genre_filter_entry = tk.Entry(root, textvariable=filter_genre_var, width=20)
genre_filter_entry.grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Страниц больше").grid(row=6, column=2, padx=5, pady=5, sticky='w')
pages_filter_entry = tk.Entry(root, textvariable=filter_pages_greater_than_var, width=10)
pages_filter_entry.grid(row=6, column=3, padx=5, pady=5)

def apply_filter():
    genre_filter = filter_genre_var.get().strip().lower()
    pages_filter = filter_pages_greater_than_var.get().strip()

    # Очистка таблицы
    for item in tree.get_children():
        tree.delete(item)

    for book in books:
        if genre_filter and genre_filter not in book["Жанр"].lower():
            continue
        if pages_filter:
            if not pages_filter.isdigit() or book["Страницы"] <= int(pages_filter):
                continue
        tree.insert('', tk.END, values=(
            book["Название"], book["Автор"], book["Жанр"], book["Страницы"]
        ))

def reset_filter():
    filter_genre_var.set("")
    filter_pages_greater_than_var.set("")
    apply_filter()

tk.Button(root, text="Применить фильтр", command=apply_filter).grid(row=7, column=0, pady=10)
tk.Button(root, text="Сбросить фильтр", command=reset_filter).grid(row=7, column=1, pady=10)

# --- Сохранение и загрузка ---
def save_to_json():
    try:
        with open("books.json", "w", encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные успешно сохранены")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

def load_from_json():
    if os.path.exists("books.json"):
        try:
            with open("books.json", "r", encoding='utf-8') as f:
                loaded_books = json.load(f)
            for book in loaded_books:
                books.append(book)
                tree.insert('', tk.END, values=(
                    book["Название"],
                    book["Автор"],
                    book["Жанр"],
                    book["Страницы"]
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

# Загружаем при старте
load_from_json()

# Кнопки сохранения
tk.Button(root, text="Сохранить в JSON", command=save_to_json).grid(row=8, column=0, pady=10)

# --- Запуск ---
root.mainloop()