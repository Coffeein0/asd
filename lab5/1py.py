from typing import List, Optional

class Book:
    def __init__(self, author: str, publisher: str, pages: int, price: float, isbn: str):
        self.author: str = author
        self.publisher: str = publisher
        self.pages: int = pages
        self.price: float = price
        self.isbn: str = isbn

    def __repr__(self) -> str:
        return f"{self.author}, {self.publisher}, {self.price} руб."


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
                if self.books[i].price > self.books[i + 1].price:
                    self.books[i], self.books[i + 1] = self.books[i + 1], self.books[i]
            right -= 1
            for i in range(right, left, -1):
                if self.books[i - 1].price > self.books[i].price:
                    self.books[i], self.books[i - 1] = self.books[i - 1], self.books[i]
            left += 1

    def is_sorted(self) -> bool:
        return all(self.books[i].price <= self.books[i + 1].price for i in range(len(self.books) - 1))

    def interpolation_search(self, target_price: float) -> Optional[int]:
        if not self.is_sorted():
            raise Exception("Элементы массива не отсортированы по цене.")
        low: int = 0
        high: int = len(self.books) - 1
        while low <= high and self.books[low].price <= target_price <= self.books[high].price:
            if self.books[low].price == self.books[high].price:
                break
            pos: int = low + (target_price - self.books[low].price) * (high - low) // (self.books[high].price - self.books[low].price)
            if pos < 0 or pos >= len(self.books):
                break
            if self.books[pos].price == target_price:
                return pos
            elif self.books[pos].price < target_price:
                low = pos + 1
            else:
                high = pos - 1
        return None


# Тесты
import time

def test_books() -> None:
    array: Array = Array()
    books: List[Book] = [
        Book("Ivanov", "Publisher1", 300, 500, "ISBN1"),
        Book("Petrov", "Publisher2", 250, 150, "ISBN2"),
        Book("Sidorov", "Publisher3", 400, 300, "ISBN3"),
        Book("Fedorov", "Publisher4", 200, 200, "ISBN4"),
        Book("Aleksandrov", "Publisher5", 350, 100, "ISBN5"),
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
    price_to_find: float = 300
    print(f"\nПоиск книги с ценой {price_to_find}:")
    index: Optional[int] = array.interpolation_search(price_to_find)
    if index is not None:
        print(f"Книга найдена: {array.books[index]}")
    else:
        print("Книга не найдена.")

    price_to_find = 1000
    print(f"\nПоиск книги с ценой {price_to_find}:")
    index = array.interpolation_search(price_to_find)
    if index is not None:
        print(f"Книга найдена: {array.books[index]}")
    else:
        print("Книга не найдена.")


def benchmark_books() -> None:
    array: Array = Array()
    books: List[Book] = [
        Book(f"Author{i}", f"Publisher{i}", 300 + i, i * 10, f"ISBN{i}") for i in range(10000)
    ]
    for book in books:
        array.add_book(book)

    start: float = time.time()
    array.cocktail_sort()
    index: Optional[int] = array.interpolation_search(5000)
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
