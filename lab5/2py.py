from typing import List, Optional

class Book:
    def __init__(self, author: str, publisher: str, pages: int, price: float, isbn: str):
        self.author: str = author
        self.publisher: str = publisher
        self.pages: int = pages
        self.price: float = price
        self.isbn: str = isbn

    def __repr__(self) -> str:
        return f"{self.author}, {self.publisher}, {self.pages}, {self.price}, {self.isbn} "


class Array:
    def __init__(self):
        self.books: List[Book] = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    def cocktail_sort(self) -> None:
        left: int = 0
        right: int = len(self.books) - 1
        while left < right:
            for i in range(left, right):
                if self.books[i].isbn > self.books[i + 1].isbn:
                    self.books[i], self.books[i + 1] = self.books[i + 1], self.books[i]
            right -= 1
            for i in range(right, left, -1):
                if self.books[i - 1].isbn > self.books[i].isbn:
                    self.books[i], self.books[i - 1] = self.books[i - 1], self.books[i]
            left += 1

    def is_sorted(self) -> bool:
        return all(self.books[i].isbn <= self.books[i + 1].isbn for i in range(len(self.books) - 1))

    def binary_search(self, target_isbn: str) -> Optional[int]:
        if not self.is_sorted():
            raise Exception("Элементы массива не отсортированы по ISBN.")
        low: int = 0
        high: int = len(self.books) - 1

        while low <= high:
            mid: int = (low + high) // 2
            if self.books[mid].isbn == target_isbn:
                return mid
            elif self.books[mid].isbn < target_isbn:
                low = mid + 1
            else:
                high = mid - 1

        return None


# Тесты
import time

def test_books() -> None:
    array: Array = Array()
    books: List[Book] = [
        Book("Ivanov", "Publisher1", 300, 500, "ISBN1"),
        Book("Petrov", "Publisher2", 250, 150, "ISBN5"),
        Book("Sidorov", "Publisher3", 400, 300, "ISBN3"),
        Book("Fedorov", "Publisher4", 200, 200, "ISBN2"),
        Book("Aleksandrov", "Publisher5", 350, 100, "ISBN4"),
        Book("Veselov", "Publisher6", 500, 600, "ISBN6")
    ]
    for book in books:
        array.add_book(book)

    print("Книги до сортировки:")
    print(array.books)

    array.cocktail_sort()
    print("\nКниги после сортировки:")
    print(array.books)

    # Тест поиска
    isbn_to_find: str = "ISBN3"
    print(f"\nПоиск книги с ISBN {isbn_to_find}:")
    index: Optional[int] = array.binary_search(isbn_to_find)
    if index is not None:
        print(f"Книга найдена: {array.books[index]}")
    else:
        print("Книга не найдена.")

    isbn_to_find = "ISBN100"
    print(f"\nПоиск книги с ISBN {isbn_to_find}:")
    index = array.binary_search(isbn_to_find)
    if index is not None:
        print(f"Книга найдена: {array.books[index]}")
    else:
        print("Книга не найдена.")


def benchmark_books() -> None:
    array: Array = Array()
    books: List[Book] = [
        Book(f"Author{i}", f"Publisher{i}", 300 + i, i * 10, f"ISBN{i:05d}") for i in range(10000)
    ]
    for book in books:
        array.add_book(book)

    start: float = time.time()
    array.cocktail_sort()
    index: Optional[int] = array.binary_search("ISBN05000")
    end: float = time.time()

    if index is not None:
        print(f"Книга найдена: {array.books[index]}")
    else:
        print("Книга не найдена.")

    print(f"Время выполнения поиска: {end - start:.3f} секунд.")


if __name__ == "__main__":
    test_books()
    print("------------------------------------------")
    benchmark_books()
