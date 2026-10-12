
import sys
from datetime import datetime
from abc import ABC, abstractmethod

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QInputDialog,
    QMessageBox,
)


# ==========================================================
# 1. АБСТРАКТНЫЙ БАЗОВЫЙ КЛАСС
# ==========================================================

class AbstractEntity(ABC):

    @abstractmethod
    def get_information(self):
        pass


# ==========================================================
# 2. КЛАСС ИНГРЕДИЕНТА
# ==========================================================

class Ingredient(AbstractEntity):

    def __init__(self, name, amount):
        self._name = name
        self._amount = amount

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    def get_information(self):
        return f"{self.name} - {self.amount}"

    def __str__(self):
        return self.get_information()

    def __repr__(self):
        return f"Ingredient({self.name!r}, {self.amount!r})"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.amount == other.amount


# ==========================================================
# 3. КЛАСС КАТЕГОРИИ
# ==========================================================

class Category(AbstractEntity):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def get_information(self):
        return f"Категория: {self.name}"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Category({self.name!r})"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.name == other.name


# ==========================================================
# 4. КЛАСС РЕЦЕПТА
# ==========================================================

class Recipe(AbstractEntity):

    def __init__(
        self,
        name,
        category,
        cooking_time,
        ingredients,
        description
    ):
        self._name = name
        self._category = category
        self._cooking_time = cooking_time
        self._ingredients = ingredients
        self._description = description

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def cooking_time(self):
        return self._cooking_time

    @cooking_time.setter
    def cooking_time(self, value):
        self._cooking_time = value

    @property
    def ingredients(self):
        return self._ingredients

    @ingredients.setter
    def ingredients(self, value):
        self._ingredients = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    def get_information(self):
        return (
            f"Название: {self.name}\n"
            f"Категория: {self.category.name}\n"
            f"Время приготовления: {self.cooking_time} минут\n"
            f"Ингредиенты: {self.ingredients}\n"
            f"Описание: {self.description}"
        )

    def __str__(self):
        return f"{self.name}, {self.cooking_time} минут"

    def __repr__(self):
        return f"Recipe({self.name!r})"

    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return False
        return self.name == other.name

    def __lt__(self, other):
        if not isinstance(other, Recipe):
            return NotImplemented
        return self.name < other.name


# ==========================================================
# 5. ЭЛЕМЕНТ СОБСТВЕННОЙ КОЛЛЕКЦИИ
# ==========================================================

class MapItem(AbstractEntity):

    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def get_information(self):
        return f"{self.key}: {self.value}"

    def __str__(self):
        return self.get_information()

    def __repr__(self):
        return f"MapItem({self.key!r}, {self.value!r})"

    def __eq__(self, other):
        if not isinstance(other, MapItem):
            return False
        return self.key == other.key and self.value == other.value


# ==========================================================
# 6. СОБСТВЕННАЯ КОЛЛЕКЦИЯ "MyMap"
# ==========================================================

class MyMap(AbstractEntity):

    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    def add(self, key, value):
        for item in self.items:
            if item.key == key:
                item.value = value
                return

        self.items.append(MapItem(key, value))

    def get(self, key):
        for item in self.items:
            if item.key == key:
                return item.value
        return None

    def remove(self, key):
        for item in self.items:
            if item.key == key:
                self.items.remove(item)
                return True
        return False

    def contains(self, key):
        return any(item.key == key for item in self.items)

    def get_all(self):
        return [item.value for item in self.items]

    def get_count(self):
        return len(self.items)

    def get_information(self):
        return f"Количество элементов: {self.get_count()}"

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __contains__(self, key):
        return self.contains(key)

    def __getitem__(self, key):
        result = self.get(key)
        if result is None:
            raise KeyError(key)
        return result

    def __str__(self):
        return self.get_information()

    def __repr__(self):
        return f"MyMap({self.items!r})"


# ==========================================================
# 7. КНИГА РЕЦЕПТОВ
# ==========================================================

class RecipeBook(AbstractEntity):

    def __init__(self):
        self._recipes = MyMap()

    @property
    def recipes(self):
        return self._recipes

    @recipes.setter
    def recipes(self, value):
        self._recipes = value

    def add_recipe(self, recipe):
        self.recipes.add(recipe.name, recipe)

    def get_recipe(self, name):
        return self.recipes.get(name)

    def remove_recipe(self, name):
        return self.recipes.remove(name)

    def find_recipe(self, name):
        return self.recipes.contains(name)

    def get_all_recipes(self):
        return self.recipes.get_all()

    def get_count(self):
        return self.recipes.get_count()

    def create_recipes(self):
        recipes = [
            Recipe(
                "Сырники", Category("Завтраки"), 30,
                "Творог, яйца, мука, сахар",
                "Смешать ингредиенты, сформировать сырники "
                "и обжарить на сковороде."
            ),
            Recipe(
                "Борщ", Category("Первые блюда"), 90,
                "Свёкла, капуста, картофель, морковь, мясо",
                "Сварить бульон, добавить овощи и варить "
                "до готовности."
            ),
            Recipe(
                "Паста Карбонара", Category("Основные блюда"), 25,
                "Паста, бекон, яйца, сыр",
                "Отварить пасту, обжарить бекон и смешать "
                "с соусом."
            ),
            Recipe(
                "Цезарь", Category("Салаты"), 20,
                "Курица, салат, сухарики, сыр, соус",
                "Приготовить курицу, нарезать ингредиенты "
                "и заправить салат."
            ),
            Recipe(
                "Шарлотка", Category("Выпечка"), 50,
                "Яблоки, яйца, мука, сахар",
                "Нарезать яблоки, приготовить тесто "
                "и выпекать до готовности."
            ),
            Recipe(
                "Плов", Category("Основные блюда"), 90,
                "Рис, мясо, морковь, лук, специи",
                "Обжарить мясо с овощами, добавить рис "
                "и готовить до мягкости."
            ),
            Recipe(
                "Блины", Category("Завтраки"), 30,
                "Молоко, яйца, мука, сахар",
                "Смешать ингредиенты и выпекать блины "
                "на сковороде."
            ),
            Recipe(
                "Оливье", Category("Салаты"), 45,
                "Картофель, морковь, яйца, горошек, колбаса",
                "Отварить овощи и яйца, нарезать ингредиенты "
                "и заправить майонезом."
            ),
            Recipe(
                "Гуляш", Category("Основные блюда"), 70,
                "Мясо, лук, морковь, томатная паста",
                "Обжарить мясо с овощами и тушить "
                "до мягкости."
            ),
            Recipe(
                "Тирамису", Category("Десерты"), 40,
                "Печенье, кофе, маскарпоне, яйца, сахар",
                "Подготовить крем, пропитать печенье кофе "
                "и собрать десерт."
            ),
            Recipe(
                "Рататуй", Category("Овощные блюда"), 65,
                "Кабачки, баклажаны, помидоры, перец",
                "Нарезать овощи, выложить в форму "
                "и запечь до готовности."
            )
        ]

        for recipe in recipes:
            self.add_recipe(recipe)

    def get_information(self):
        return f"Книга рецептов. Всего рецептов: {self.get_count()}"

    def __len__(self):
        return self.get_count()

    def __iter__(self):
        return iter(self.get_all_recipes())

    def __contains__(self, name):
        return self.find_recipe(name)

    def __str__(self):
        return self.get_information()

    def __repr__(self):
        return f"RecipeBook({self.get_count()} recipes)"


# ==========================================================
# 8. ГЛАВНОЕ ОКНО
# ==========================================================

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.login, accepted = QInputDialog.getText(
            self,
            "Вход в приложение",
            "Введите логин:"
        )

        if not accepted or not self.login.strip():
            self.login = "UserName"
        else:
            self.login = self.login.strip()

        self.time_in = datetime.now()
        self.report_written = False
        self.editing_recipe_name = None

        self.setWindowTitle("Книга рецептов")
        self.resize(700, 800)

        # Заголовок
        self.title_label = QLabel("Книга рецептов")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Поиск
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Введите название рецепта"
        )

        self.search_button = QPushButton("Найти")

        # Список и информация
        self.recipe_list = QListWidget()

        self.recipe_details = QTextEdit()
        self.recipe_details.setReadOnly(True)

        # Поля ввода
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название рецепта")

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Категория")

        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText(
            "Время приготовления в минутах"
        )

        self.ingredients_input = QLineEdit()
        self.ingredients_input.setPlaceholderText("Ингредиенты")

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Описание")
        self.description_input.setMaximumHeight(75)

        # Кнопки
        self.add_button = QPushButton("Добавить рецепт")
        self.delete_button = QPushButton("Удалить рецепт")
        self.edit_button = QPushButton("Редактировать рецепт")
        self.save_edit_button = QPushButton("Сохранить изменения")

        # Данные
        self.recipe_book = RecipeBook()
        self.recipe_book.create_recipes()

        # Основной layout
        layout = QVBoxLayout()

        layout.addWidget(self.title_label)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        layout.addWidget(QLabel("Список рецептов:"))
        layout.addWidget(self.recipe_list)

        layout.addWidget(QLabel("Информация о рецепте:"))
        layout.addWidget(self.recipe_details)

        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Категория:"))
        layout.addWidget(self.category_input)

        layout.addWidget(QLabel("Время приготовления:"))
        layout.addWidget(self.time_input)

        layout.addWidget(QLabel("Ингредиенты:"))
        layout.addWidget(self.ingredients_input)

        layout.addWidget(QLabel("Описание:"))
        layout.addWidget(self.description_input)

        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.save_edit_button)

        self.setLayout(layout)

        # Подключение сигналов
        self.search_button.clicked.connect(self.search_recipe)
        self.search_input.returnPressed.connect(self.search_recipe)
        self.recipe_list.itemClicked.connect(self.show_recipe_details)
        self.add_button.clicked.connect(self.add_recipe)
        self.delete_button.clicked.connect(self.delete_recipe)
        self.edit_button.clicked.connect(self.edit_recipe)
        self.save_edit_button.clicked.connect(self.save_edited_recipe)

        self.refresh_recipe_list()

    # ------------------------------------------------------
    # ПОИСК
    # ------------------------------------------------------

    def search_recipe(self):
        search_text = self.search_input.text().strip().lower()

        self.recipe_list.clear()

        for recipe in self.recipe_book:
            if search_text in recipe.name.lower():
                self.recipe_list.addItem(recipe.name)

        self.recipe_details.clear()

    # ------------------------------------------------------
    # ПОКАЗ ИНФОРМАЦИИ
    # ------------------------------------------------------

    def show_recipe_details(self, item):
        recipe = self.recipe_book.get_recipe(item.text())

        if recipe is not None:
            self.recipe_details.setText(recipe.get_information())

    # ------------------------------------------------------
    # ДОБАВЛЕНИЕ
    # ------------------------------------------------------

    def add_recipe(self):
        name = self.name_input.text().strip()
        category_name = self.category_input.text().strip()
        time_text = self.time_input.text().strip()
        ingredients = self.ingredients_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not all([
            name, category_name, time_text, ingredients, description
        ]):
            self.recipe_details.setText("Заполните все поля!")
            return

        try:
            cooking_time = int(time_text)
            if cooking_time <= 0:
                self.recipe_details.setText(
                    "Время должно быть больше нуля!"
                )
                return
        except ValueError:
            self.recipe_details.setText(
                "Время должно быть целым числом!"
            )
            return

        if self.recipe_book.find_recipe(name):
            self.recipe_details.setText(
                "Рецепт с таким названием уже существует!"
            )
            return

        recipe = Recipe(
            name,
            Category(category_name),
            cooking_time,
            ingredients,
            description
        )

        self.recipe_book.add_recipe(recipe)
        self.clear_input_fields()
        self.search_input.clear()
        self.refresh_recipe_list()

        self.recipe_details.setText(
            f"Рецепт «{name}» успешно добавлен!"
        )

    # ------------------------------------------------------
    # УДАЛЕНИЕ
    # ------------------------------------------------------

    def delete_recipe(self):
        selected_item = self.recipe_list.currentItem()

        if selected_item is None:
            self.recipe_details.setText(
                "Сначала выберите рецепт для удаления!"
            )
            return

        name = selected_item.text()
        self.recipe_book.remove_recipe(name)

        if self.editing_recipe_name == name:
            self.editing_recipe_name = None
            self.clear_input_fields()

        self.search_input.clear()
        self.refresh_recipe_list()

        self.recipe_details.setText(f"Рецепт «{name}» удалён!")

    # ------------------------------------------------------
    # РЕДАКТИРОВАНИЕ
    # ------------------------------------------------------

    def edit_recipe(self):
        selected_item = self.recipe_list.currentItem()

        if selected_item is None:
            self.recipe_details.setText(
                "Сначала выберите рецепт для редактирования!"
            )
            return

        recipe = self.recipe_book.get_recipe(selected_item.text())

        if recipe is None:
            return

        self.editing_recipe_name = recipe.name

        self.name_input.setText(recipe.name)
        self.category_input.setText(recipe.category.name)
        self.time_input.setText(str(recipe.cooking_time))
        self.ingredients_input.setText(recipe.ingredients)
        self.description_input.setPlainText(recipe.description)

        self.recipe_details.setText(
            "Измените данные и нажмите «Сохранить изменения»."
        )

    # ------------------------------------------------------
    # СОХРАНЕНИЕ ИЗМЕНЕНИЙ
    # ------------------------------------------------------

    def save_edited_recipe(self):
        if self.editing_recipe_name is None:
            self.recipe_details.setText(
                "Сначала выберите рецепт и нажмите "
                "«Редактировать рецепт»!"
            )
            return

        old_name = self.editing_recipe_name

        name = self.name_input.text().strip()
        category_name = self.category_input.text().strip()
        time_text = self.time_input.text().strip()
        ingredients = self.ingredients_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not all([
            name, category_name, time_text, ingredients, description
        ]):
            self.recipe_details.setText("Заполните все поля!")
            return

        try:
            cooking_time = int(time_text)
            if cooking_time <= 0:
                self.recipe_details.setText(
                    "Время должно быть больше нуля!"
                )
                return
        except ValueError:
            self.recipe_details.setText(
                "Время должно быть целым числом!"
            )
            return

        if name != old_name and self.recipe_book.find_recipe(name):
            self.recipe_details.setText(
                "Рецепт с таким названием уже существует!"
            )
            return

        self.recipe_book.remove_recipe(old_name)

        updated_recipe = Recipe(
            name,
            Category(category_name),
            cooking_time,
            ingredients,
            description
        )

        self.recipe_book.add_recipe(updated_recipe)
        self.editing_recipe_name = None

        self.search_input.clear()
        self.clear_input_fields()
        self.refresh_recipe_list()

        self.recipe_details.setText(
            f"Рецепт «{name}» успешно изменён!"
        )

    # ------------------------------------------------------
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    # ------------------------------------------------------

    def clear_input_fields(self):
        self.name_input.clear()
        self.category_input.clear()
        self.time_input.clear()
        self.ingredients_input.clear()
        self.description_input.clear()

    def refresh_recipe_list(self):
        self.recipe_list.clear()

        for recipe in self.recipe_book:
            self.recipe_list.addItem(recipe.name)

    def write_report(self):
        if self.report_written:
            return

        self.report_written = True
        time_out = datetime.now()

        time_format = "%d.%m.%Y %H:%M:%S"
        time_in_text = self.time_in.strftime(time_format)
        time_out_text = time_out.strftime(time_format)

        try:
            with open("report.txt", "a", encoding="utf-8") as file:
                file.write("+------------------------------------------------------+\n")
                file.write("| login    | time_in             | time_out            |\n")
                file.write("+------------------------------------------------------+\n")
                file.write(
                    f"| {self.login:<8} | "
                    f"{time_in_text:<19} | "
                    f"{time_out_text:<19} |\n"
                )
                file.write("+------------------------------------------------------+\n\n")
        except OSError as error:
            print(f"Не удалось записать отчёт: {error}")

    # ------------------------------------------------------
    # ПЕРЕОПРЕДЕЛЁННЫЕ МЕТОДЫ ОКНА
    # ------------------------------------------------------

    def closeEvent(self, event):
        self.write_report()
        super().closeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def changeEvent(self, event):
        super().changeEvent(event)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def focusInEvent(self, event):
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)

    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)


# ==========================================================
# 9. ЗАПУСК ПРИЛОЖЕНИЯ
# ==========================================================

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
