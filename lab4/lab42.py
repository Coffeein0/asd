import time
from typing import List

class Book:
    def __init__(self, author: str, publisher: str, pages: int, price: float, isbn: str) -> None:
        self.author = author
        self.publisher = publisher
        self.pages = pages
        self.price = price
        self.isbn = isbn

    def __repr__(self) -> str:
        return f"Book(author='{self.author}', publisher='{self.publisher}', pages={self.pages}, price={self.price}, ISBN='{self.isbn}')"

class BookArray:
    def __init__(self) -> None:
        self.books: List[Book] = []

    def __repr__(self) -> str:
        return f"[{', '.join(str(book) for book in self.books)}]"

    def append(self, book: Book) -> None:
        self.books.append(book)

    def delete(self, isbn: str) -> None:
        self.books = [book for book in self.books if book.isbn != isbn]

    def cocktail_sort_isbn(self) -> None:
        left = 0
        right = len(self.books) - 1
        while left < right:
            for i in range(left, right):
                if self.books[i].isbn > self.books[i + 1].isbn:
                    self.books[i], self.books[i + 1] = self.books[i + 1], self.books[i]
            right -= 1
            for i in range(right, left, -1):
                if self.books[i - 1].isbn > self.books[i].isbn:
                    self.books[i], self.books[i - 1] = self.books[i - 1], self.books[i]
            left += 1

    def quick_sort_price(self) -> None:
        # Используем стек для хранения границ
        stack = [(0, len(self.books) - 1)]

        while stack:
            left, right = stack.pop()
            if left < right:
                pivot = self.books[right].price
                partition_index = left
                for i in range(left, right):
                    if self.books[i].price > pivot:  # Сортируем по убыванию
                        self.books[i], self.books[partition_index] = self.books[partition_index], self.books[i]
                        partition_index += 1
                self.books[partition_index], self.books[right] = self.books[right], self.books[partition_index]

                # Добавляем границы для дальнейшей сортировки в стек
                stack.append((left, partition_index - 1))
                stack.append((partition_index + 1, right))


    def __iter__(self):
        return iter(self.books)
    
    def __str__(self) -> str:
        return '\n'.join(str(book) for book in self.books)

# Функция для тестирования класса BookArray
def tests_array() -> None:
    print("\nТесты:")
    arr = BookArray()

    # Тест 1. Проверка добавления элементов
    books = [
        Book("Джек Лондон", "Эксмо", 323, 699.99, "7-1343-16"),
        Book("Макс Фрай", "Эксмо", 687, 450.0, "4-4551-18"),
        Book("Владимир Торин", "Миф", 767, 899.0, "1-145-17"),
        Book("Джон Мильтон", "АСТ", 445, 399.99, "6-4166-815"),
        Book("Уильям Индик", "Миф", 380, 500.0, "5-51-1998"),
        Book("Кэролайн О`Дохонью", "LikeBook", 365, 799.0, "2-190-10"),
        Book("Лия Арден", "Эксмо", 414, 1280.0, "8-21-3145"),
        Book("Михаил Булгаков", "Азбука", 1114, 1349.0, "9-5631-156"),
        Book("Гастон Леру", "Эксмо", 317, 320.0, "3-1342-2413"),
        Book("Бернар Вербер", "Эксмо", 412, 699.99, "8-3165-3614")
    ]
    print(f"Array до добавления в него элементов:\n{arr}")
    for book in books:
        arr.append(book)
    print(f"Array после добавления в него элементов:\n{arr}")

    # Тест 2. Проверка метода сортировки перемешиванием (по возрастанию ISBN)
    arr.cocktail_sort_isbn()
    print(f"\nArray после сортировки перемешиванием (по возрастанию ISBN):\n{arr}")

    # Тест 3. Проверка метода быстрой сортировки (по убыванию стоимости)
    arr.quick_sort_price()
    print(f"\nArray после быстрой сортировки (по убыванию стоимости):\n{arr}")

    # Тест 4. Удаление элементов по полю ISBN
    arr.delete("2-190-10")
    arr.delete("7-1343-16")
    arr.delete("1-145-17")
    arr.delete("8-3165-3614")
    arr.delete("4-4551-18")
    print(f"\nArray после удаления 5 элементов:\n{arr}\n")

    # Тест 5. Проверка итерируемости
    print("Проверка итерируемости:")
    for book in arr:
        print(book)

    print("Все тесты пройдены!")

# Функция для выполнения бенчмарков
def benchmarks() -> None:
    print("\nБенчмарки")
    arr = BookArray()

    # Создание 10,000 книг с уникальными значениями
    books = [Book(f'Author{i}', f'Publisher{i}', i + 100, i * 100.0, f'ISBN{i}') for i in range(10000)]
    
    # Бенчмарк на добавление 10,000 элементов
    start = time.time()
    for book in books:
        arr.append(book)
    end = time.time()
    print(f"Время добавления 10,000 элементов: {(end - start):.5f} секунд")
    
    # Бенчмарк на сортировку перемешиванием
    start = time.time()
    arr.cocktail_sort_isbn()
    end = time.time()
    print(f"Время сортировки перемешиванием для 10,000 элементов: {(end - start):.5f} секунд")
    
    # Бенчмарк на сортировку по убыванию стоимости
    start = time.time()
    arr.quick_sort_price()
    end = time.time()
    print(f"Время быстрой сортировки для 10,000 элементов: {(end - start):.5f} секунд")

# Запуск тестов и бенчмарков
tests_array()
benchmarks()
