from typing import List
import time

# Класс книги с полями: автор, издательство, количество страниц, стоимость, ISBN
class Book:
    def __init__(self, author: str, publisher: str, pages: int, price: float, isbn: str) -> None:
        self.author = author
        self.publisher = publisher
        self.pages = pages
        self.price = price
        self.isbn = isbn

    def __repr__(self) -> str:
        return f"Book(author='{self.author}', publisher='{self.publisher}', pages={self.pages}, price={self.price}, ISBN='{self.isbn}')"

# Класс массива книг с методами сортировки, добавления, удаления и итерируемостью
class BookArray:
    def __init__(self) -> None:
        self.books: List[Book] = []

    def __repr__(self) -> str:
        return f"[{', '.join(str(book) for book in self.books)}]"

    # Метод для добавления книги
    def append(self, book: Book) -> None:
        self.books.append(book)

    # Метод для удаления книги по ISBN
    def delete(self, isbn: str) -> None:
        self.books = [book for book in self.books if book.isbn != isbn]

    # Метод сортировки перемешиванием (Shaker sort) по возрастанию цены
    def cocktail_sort(self) -> None:
        left = 0
        right = len(self.books) - 1
        while left < right:
            for i in range(left, right):
                if self.books[i].price > self.books[i + 1].price:
                    self.books[i], self.books[i + 1] = self.books[i + 1], self.books[i]
            right -= 1
            for i in range(right, left, -1):
                if self.books[i - 1].price > self.books[i].price:
                    self.books[i], self.books[i - 1] = self.books[i - 1], self.books[i]
            left += 1

    # Метод сортировки выбором (Selection sort) по убыванию количества страниц
    def selection_sort(self) -> None:
        n = len(self.books)
        for i in range(n - 1):
            max_idx = i
            for j in range(i + 1, n):
                if self.books[j].pages > self.books[max_idx].pages:
                    max_idx = j
            self.books[i], self.books[max_idx] = self.books[max_idx], self.books[i]       

    # Делает класс итерируемым
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

    # Тест 2. Проверка метода сортировки перемешиванием (по возрастанию цены)
    arr.cocktail_sort()
    print(f"\nArray после сортировки перемешиванием (по возрастанию цены):\n{arr}")

    # Тест 3. Проверка метода сортировки выбором (по убыванию количества страниц)
    arr.selection_sort()
    print(f"\nArray после сортировки выбором (по убыванию количества страниц):\n{arr}")

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
    arr.cocktail_sort()
    end = time.time()
    print(f"Время сортировки перемешиванием для 10,000 элементов: {(end - start):.5f} секунд")
    
    # Бенчмарк на сортировку выбором
    start = time.time()
    arr.selection_sort()
    end = time.time()
    print(f"Время сортировки выбором для 10,000 элементов: {(end - start):.5f} секунд")

# Запуск тестов и бенчмарков
tests_array()
benchmarks()
