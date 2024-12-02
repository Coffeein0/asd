import time
from typing import Optional

class Student:
    def __init__(self, full_name: str, group_number: str, course: int, age: int, average_grade: float) -> None:
        self.full_name = full_name
        self.group_number = group_number
        self.course = course
        self.age = age
        self.average_grade = average_grade

    def __repr__(self) -> str:
        return f"Student({self.full_name}, {self.group_number}, {self.course}, {self.age}, {self.average_grade})"

class Node:
    def __init__(self, student: Student) -> None:
        self.student = student
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class MaxHeap:
    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size: int = 0

    def _parent_index(self, index: int) -> int:
        return (index - 1) // 2

    def _left_index(self, index: int) -> int:
        return 2 * index + 1

    def _right_index(self, index: int) -> int:
        return 2 * index + 2

    def _swap(self, node1: Node, node2: Node) -> None:
        node1.student, node2.student = node2.student, node1.student

    def insert(self, student: Student) -> None:
        new_node = Node(student)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            self._heapify_up(self.size)

        self.size += 1

    def _heapify_up(self, index: int) -> None:
        current_index = index
        while current_index > 0:
            parent_index = self._parent_index(current_index)
            if self._get_student_at_index(current_index).average_grade > self._get_student_at_index(parent_index).average_grade:
                self._swap(self._get_node_at_index(current_index), self._get_node_at_index(parent_index))
                current_index = parent_index
            else:
                break

    def extract_max(self) -> Optional[Student]:
        if self.size == 0:
            return None

        max_student = self.head.student
        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            if self.head:
                self.head.prev = None

        self.size -= 1
        if self.size > 0:
            self._heapify_down(0)

        return max_student

    def _heapify_down(self, index: int) -> None:
        current_index = index
        while current_index < self.size:
            left_index = self._left_index(current_index)
            right_index = self._right_index(current_index)
            largest_index = current_index

            if left_index < self.size and self._get_student_at_index(left_index).average_grade > self._get_student_at_index(largest_index).average_grade:
                largest_index = left_index

            if right_index < self.size and self._get_student_at_index(right_index).average_grade > self._get_student_at_index(largest_index).average_grade:
                largest_index = right_index

            if largest_index != current_index:
                self._swap(self._get_node_at_index(current_index), self._get_node_at_index(largest_index))
                current_index = largest_index
            else:
                break

    def _get_student_at_index(self, index: int) -> Student:
        current = self.head
        for _ in range(index):
            current = current.next
        return current.student

    def _get_node_at_index(self, index: int) -> Node:
        current = self.head
        for _ in range(index):
            current = current.next
        return current

    def save_to_file(self, filename: str) -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            current = self.head
            while current:
                f.write(f"{current.student.full_name},{current.student.group_number},{current.student.course},"
                         f"{current.student.age},{current.student.average_grade}\n")
                current = current.next

    def load_from_file(self, filename: str) -> None:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                full_name, group_number, course, age, average_grade = line.strip().split(',')
                student = Student(full_name=full_name, group_number=group_number,
                                  course=int(course), age=int(age),
                                  average_grade=float(average_grade))
                self.insert(student)

    def search(self, average_grade: float) -> bool:
        current = self.head
        while current:
            if current.student.average_grade == average_grade:
                return True
            current = current.next
        return False

def run_tests() -> None:
    heap = MaxHeap()

    # Тест 1: Вставка студентов
    heap.insert(Student("Иванов Иван", "Группа 1", 1, 18, 4.5))
    heap.insert(Student("Петров Петр", "Группа 2", 2, 19, 3.5))
    heap.insert(Student("Сидоров Сидор", "Группа 3", 3, 20, 4.0))
    
    assert heap.search(4.5) == True
    assert heap.search(3.5) == True
    assert heap.search(4.0) == True
    assert heap.search(5.0) == False  # Не найден студент с оценкой 5.0

    # Тест 2: Извлечение максимального
    max_student = heap.extract_max()
    assert max_student.full_name == "Иванов Иван"  # Максимальная оценка 4.5

    # Тест 3: Извлечение после удаления
    second_max_student = heap.extract_max()
    assert second_max_student.full_name == "Сидоров Сидор"  # Следующий по максимальной оценке

    # Тест 4: Проверка состояния кучи
    assert heap.size == 1  # Оставшийся студент
    assert heap.search(3.5) == True  # Остался студент с оценкой 3.5

    # Тест 5: Сохранение и загрузка
    heap.save_to_file('test_students2.txt')
    new_heap = MaxHeap()
    new_heap.load_from_file('test_students2.txt')

    # Проверяем, что студенты загружены правильно
    assert new_heap.search(4.5) == False
    assert new_heap.search(4.0) == False
    assert new_heap.search(3.5) == True  # Проверяем, что 3.5 остался
    assert new_heap.search(5.0) == False  # Не найден студент с оценкой 5.0

def benchmark() -> None:
    heap = MaxHeap()
    start_time = time.time()

    # Вставка 1000 студентов
    for i in range(1000):
        heap.insert(Student(f"Student {i}", f"Group {i}", (i % 10) + 1, 18 + (i % 5), 4.0 + (i % 10) * 0.1))
    print(f"Time to push 1000 students: {time.time() - start_time:.6f} seconds")

    # Извлечение 1000 студентов
    start_time = time.time()
    for _ in range(1000):
        heap.extract_max()
    print(f"Time to extract 1000 students: {time.time() - start_time:.6f} seconds")

if __name__ == "__main__":
    benchmark()
    run_tests()
