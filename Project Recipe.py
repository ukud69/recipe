import sys, time, json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, \
 QVBoxLayout, QGridLayout, QListWidget, QTableWidget, QLineEdit, QInputDialog, QTableWidgetItem

try:
    with open("ingredient.json", 'r', encoding='utf-8') as file:
        myIng = json.load(file)
except:
    myIng ={}
    with open("ingredient.json", 'w', encoding='utf-8') as file:
        json.dump(myIng, file, ensure_ascii = False)

def writeListRecipe(self):                  # Заполнение списка рецептов
    self.vbox.clear()
    try:
        with open("recipe.json", 'r', encoding='utf-8') as file:
            recipe = json.load(file)
            self.vbox.addItem('Известные рецепты:')
            list_recipe = list(recipe.keys())
    except:
        list_recipe = []
    self.vbox.addItems(list_recipe)

def writeListIngredients(self):
    #self.vbox1.clear()
    try:
        with open("ingredient.json", 'r', encoding='utf-8') as file:
            ingredient = json.load(file)
            self.vbox1.addItem('Ингредиенты в наличии:')
            list_ingredients = list()
            for key, value in list(ingredient.items()):
                list_ingredients.append(str(key) + ', ' + str(value) )

            self.vbox1.addItems(list_ingredients)
    except:
        list_recipe = []

# Creating the main window
class App(QMainWindow): # Приложение
    def __init__(self):
        super().__init__()
        self.title = 'Программа расчета плана'
        self.left = 800
        self.top = 200
        self.width = 600
        self.height = 350
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.show()

# Creating new recipe widgets
class MyRecipeWitget(QWidget): # Всплывающее окно добавления рецепта
    def addRecipe(self):
        recipe = {}
        try:
            with open("recipe.json", 'r', encoding='utf-8') as file:
                recipe = json.load(file)
                myRecipeName = self.line_edit.text()
                myIngredients = {}
                i = 0
                while self.mw_table.cellWidget(i, 0).currentText() > "":
                    myIngredients[self.mw_table.cellWidget(i, 0).currentText()] = self.mw_table.item(i, 1).text()
                    print(i, myIngredients)
                    i += 1
            recipe[myRecipeName] = myIngredients
            with open("recipe.json", 'w', encoding='utf-8') as file:
                json.dump(recipe, file, ensure_ascii = False)

        except:
            with open("recipe.json", 'w', encoding='utf-8') as file:
                json.dump(recipe, file, ensure_ascii = False)
        writeListRecipe(self.parentWindow)
        self.close()

    def __init__(self, parentWindow):
        super().__init__()
        self.parentWindow = parentWindow
        self.mw = QVBoxLayout(self)
        self.grid5 = QGridLayout()
        self.mw_table = QTableWidget()
        self.mw_table.setRowCount(8)
        self.mw_table.setColumnCount(2)
        self.mw_table.setHorizontalHeaderLabels(['Ингредиент', 'Количество'])
        i = 0
        for j in range(8):
            self.comboBox = QtWidgets.QComboBox()
            self.mw_table.setCellWidget(i, 0, self.comboBox)
            self.comboBox.addItem("")
            ingredient_list = myIng
            self.comboBox.addItems(ingredient_list)
            i += 1
        self.grid5.addWidget(self.mw_table, 2, 0)
        self.mw.addLayout(self.grid5)
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Введите наименование рецепта")
        self.grid5.addWidget(self.line_edit, 1, 0)
        self.btn = QPushButton('Записать рецепт', self)
        self.btn.clicked.connect(self.addRecipe)
        self.grid5.addWidget(self.btn, 0, 0)
        self.show()

# Creating tab widgets
class MyTabWidget(QWidget):             # основное окно
    def addRecipe(self):
        self.exx = MyRecipeWitget(self)
        self.exx.show()

    def addIngradients(self):
        (note_name, ok) = QInputDialog.getText(self, "Добавить ингредиент", "Название ингредиента: ")
        if note_name and ok:
            with open("ingredient.json", 'w') as file:
                myIng[note_name] = 0
                json.dump(myIng, file)

    def loadReserve(self):

        with open("ingredient.json", 'r', encoding='utf-8') as file:
            ingredient = json.load(file)
            i = 0
            while self.u_table.cellWidget(i, 0).currentText() > "":
                if self.u_table.cellWidget(i, 0).currentText() in ingredient:
                    ingredient[self.u_table.cellWidget(i, 0).currentText()] +=  int(self.u_table.item(i, 1).text())
                else:
                    ingredient[self.u_table.cellWidget(i, 0).currentText()] = int(self.u_table.item(i, 1).text())
                i += 1
        with open("ingredient.json", 'w', encoding='utf-8') as file:
            json.dump(ingredient, file, ensure_ascii = False)

    def loadStocks (self):
        try:
            with open("ingredient.json", 'r', encoding='utf-8') as file:
                myIng = json.load(file)
        except:
            myIng = {}
        inkrement = 0
        list_ingredients = list(myIng.items())
        print(list_ingredients)
        for key, value in list(list_ingredients):
            if value > 0:
                print(key, value)
                self.cash_table.setItem(inkrement, 0, QTableWidgetItem(key))
                self.cash_table.setItem(inkrement, 1, QTableWidgetItem(str(value)))

                inkrement += 1


    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()  # Добавление основной таблицы и закладок
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Рецепты") # Добавление закадок к основной таблице
        self.tabs.addTab(self.tab2, "Запасы")
        self.tabs.addTab(self.tab3, "Возможности")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self) # Работа с первой закладкой
        self.grid = QGridLayout()
        self.vbox = QListWidget()
        self.grid.addWidget(self.vbox, 0, 0)
        self.vbox1 = QListWidget()
        self.grid.addWidget(self.vbox1, 0, 1)
        self.btn = QPushButton('Добавить рецепт', self)
        self.btn.clicked.connect(self.addRecipe)
        self.grid.addWidget(self.btn, 1, 0)
        self.tab1.setLayout(self.grid)
        writeListRecipe(self)
        writeListIngredients(self)

        # Create second tab
        self.tab2.layout = QVBoxLayout(self)    # Работа с второй закладкой
        self.grid2 = QGridLayout()
        self.u_table = QTableWidget()
        self.u_table.setRowCount(8)
        self.u_table.setColumnCount(2)
        self.u_table.setHorizontalHeaderLabels(['Ингредиент', 'Количество'])
        self.u_table.setColumnWidth(0, 400)
        self.u_table.setColumnWidth(1, 150)

        i = 0
        for j in range(8):
            self.comboBox = QtWidgets.QComboBox()
            self.u_table.setCellWidget(i, 0, self.comboBox)
            self.comboBox.addItem("")
            ingredient_list = myIng
            self.comboBox.addItems(ingredient_list)
            i += 1

        self.grid2.addWidget(self.u_table, 0, 0, 0, -1)
        self.vbox3 = QListWidget()
        self.btn2 = QPushButton('Записать поступление запаса', self)
        self.grid2.addWidget(self.btn2, 1, 0)
        self.btn2.clicked.connect(self.loadReserve)

        self.btn3 = QPushButton('Добавить ингредиент', self)
        self.grid2.addWidget(self.btn3, 1, 1)
        self.btn3.clicked.connect(self.addIngradients)
        self.tab2.setLayout(self.grid2)

        # Create third tab
        self.tab3.layout = QVBoxLayout(self)    # Работа с третьей закладкой
        self.grid3 = QGridLayout()
        self.btn4 = QPushButton('Загрузить запасы', self)
        self.grid3.addWidget(self.btn4, 0, 0)
        self.btn4.clicked.connect(self.loadStocks)
        self.btn5 = QPushButton('Расчитать', self)
        self.grid3.addWidget(self.btn5, 0, 1)
        self.btn6 = QPushButton('Перечитать', self)
        self.grid3.addWidget(self.btn6, 0, 2)
        self.tab3.setLayout(self.grid3)
        self.cash_table = QTableWidget()
        self.cash_table.setRowCount(8)
        self.cash_table.setColumnCount(2)
        self.cash_table.setHorizontalHeaderLabels(['Наличие\n ингредиентов', 'Количество'])
        self.cash_table.setColumnWidth(0, 160)
        self.grid3.addWidget(self.cash_table, 1, 0)
        self.i_table = QTableWidget()
        self.i_table.setRowCount(8)
        self.i_table.setColumnCount(3)

        self.i_table.setHorizontalHeaderLabels(['Рецепт', 'Количество\n макс', 'Количество\n выбор'])
        self.i_table.setColumnWidth(0, 70)
        self.i_table.setColumnWidth(1, 75)
        self.i_table.setColumnWidth(2, 75)
        self.grid3.addWidget(self.i_table, 1, 1, 1, -1)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())