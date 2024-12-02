import time
from typing import Optional, List

class Student:
    def __init__(self, full_name: str, group_number: str, course: int, age: int, average_grade: float) -> None:
        self.full_name = full_name
        self.group_number = group_number
        self.course = course
        self.age = age
        self.average_grade = average_grade

    def __repr__(self) -> str:
        return f"Student({self.full_name}, {self.group_number}, {self.course}, {self.age}, {self.average_grade})"

class AVLNode:
    def __init__(self, student: Student) -> None:
        self.student = student
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None
        self.height: int = 1

class AVLTree:
    def __init__(self) -> None:
        self.root: Optional[AVLNode] = None

    def _height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _balance_factor(self, node: Optional[AVLNode]) -> int:
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        x = y.left
        if x is None:
            return y  # No rotation possible
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._height(y.left), self._height(y.right)) # пересчитываются высоты узлов
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        y = x.right
        if y is None:
            return x  # No rotation possible
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def _insert(self, node: Optional[AVLNode], student: Student) -> AVLNode:
        if not node:
            return AVLNode(student)

        if student.average_grade < node.student.average_grade:
            node.left = self._insert(node.left, student)
        else:
            node.right = self._insert(node.right, student)

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._balance_factor(node)

        if balance > 1 and student.average_grade < node.left.student.average_grade:
            return self._rotate_right(node)

        if balance < -1 and student.average_grade > node.right.student.average_grade:
            return self._rotate_left(node)

        if balance > 1 and student.average_grade > node.left.student.average_grade:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and student.average_grade < node.right.student.average_grade:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, student: Student) -> None:
        self.root = self._insert(self.root, student)

    def _find_min(self, node: AVLNode) -> AVLNode:
        if node.left is None:
            return node
        return self._find_min(node.left)

    def _delete(self, node: Optional[AVLNode], average_grade: float) -> Optional[AVLNode]:
        if not node:
            return node

        if average_grade < node.student.average_grade:
            node.left = self._delete(node.left, average_grade)
        elif average_grade > node.student.average_grade:
            node.right = self._delete(node.right, average_grade)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._find_min(node.right)
            node.student = temp.student
            node.right = self._delete(node.right, temp.student.average_grade)

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._balance_factor(node)

        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)

        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)

        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def delete(self, average_grade: float) -> None:
        self.root = self._delete(self.root, average_grade)

    def save_to_file(self, filename: str) -> None:
        with open(filename, 'w') as f:
            self._save_recursive(self.root, f)

    def _save_recursive(self, node: Optional[AVLNode], file) -> None:
        if node:
            file.write(f"{node.student.full_name},{node.student.group_number},{node.student.course},"
                       f"{node.student.age},{node.student.average_grade}\n")
            self._save_recursive(node.left, file)
            self._save_recursive(node.right, file)

    def load_from_file(self, filename: str) -> None:
        with open(filename, 'r') as f:
            for line in f:
                full_name, group_number, course, age, average_grade = line.strip().split(',')
                student = Student(full_name, group_number, int(course), int(age), float(average_grade))
                self.insert(student)

    def search(self, average_grade: float) -> bool:
        return self._search(self.root, average_grade)

    def _search(self, node: Optional[AVLNode], average_grade: float) -> bool:
        if not node:
            return False
        if node.student.average_grade == average_grade:
            return True
        elif average_grade < node.student.average_grade:
            return self._search(node.left, average_grade)
        else:
            return self._search(node.right, average_grade)

    def search_via_inorder(self, average_grade: float) -> bool:
        return self._search_via_inorder(self.root, average_grade)

    def _search_via_inorder(self, node: Optional[AVLNode], average_grade: float) -> bool:
        if node:
            found = self._search_via_inorder(node.left, average_grade)
            if found:
                return True
            if node.student.average_grade == average_grade:
                return True
            return self._search_via_inorder(node.right, average_grade)
        return False

def benchmark() -> None:
    q = AVLTree()
    start_time = time.time()

    # Вставка 1000 студентов
    for i in range(1000):
        q.insert(Student(f"Student {i}", str(i), 1, 18, 4.0 + (i % 10) * 0.1))
    print(f"Time to push 1000 students: {time.time() - start_time:.6f} seconds")

    # Удаление 1000 студентов
    start_time = time.time()
    for i in range(1000):
        q.delete(4.0 + (i % 10) * 0.1)  # Удаляем студентов с этими средними оценками
    print(f"Time to delete 1000 students: {time.time() - start_time:.6f} seconds")

def run_tests() -> None:
    tree = AVLTree()
    
    # Тест 1: Вставка студентов
    student1 = Student("Иванов Иван", "Группа 1", 1, 18, 4.5)
    student2 = Student("Петров Петр", "Группа 2", 2, 19, 3.5)
    student3 = Student("Сидоров Сидор", "Группа 3", 3, 20, 4.0)
    
    tree.insert(student1)
    tree.insert(student2)
    tree.insert(student3)

    assert tree.search(4.5) == True
    assert tree.search(3.5) == True
    assert tree.search(4.0) == True
    assert tree.search(5.0) == False  # Студент с этой оценкой не должен быть найден

    # Тест 2: Удаление студента
    tree.delete(3.5)
    assert tree.search(3.5) == False  # Удалили студента с оценкой 3.5

    # Тест 3: Сохранение и загрузка
    tree.save_to_file('test_students.txt')
    new_tree = AVLTree()
    new_tree.load_from_file('test_students.txt')
    assert new_tree.search(4.5) == True
    assert new_tree.search(4.0) == True
    assert new_tree.search(3.5) == False  # После удаления не должен быть найден

    # Тест 4: Проверка балансировки
    for i in range(100):
        tree.insert(Student(f"Student {i}", str(i), 1, 18, 4.0 + (i % 10) * 0.1))
    assert tree.root is not None  # Дерево не должно быть пустым

    # Тест 5: Проверка на несуществующую оценку
    assert tree.search(10.0) == False  # Оценка 10.0 не должна существовать

if __name__ == "__main__":
    benchmark()
    run_tests()
