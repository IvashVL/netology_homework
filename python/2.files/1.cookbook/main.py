class Ingredient:
    """Класс Ingredient представляет ингредиент блюда.

    Класс имеет три параметра: name - имя ингредиента, quantity - количество и measure - единица измерения.
    Метод __str__ переопределен для вывода экземпляра класса на экран функцией print().
    Метод to_dict() возвращает словарь с параметрами ингредиента в соответствии с требованем задачи №1.
    Если немного отступить от требования задачи №1 и хранить рецепт не как список словарей, а как список экземпляров
    класса Ingredient, то можно было бы сократить код.
    Метод load_from_string(string) считывает параметры ингредиента (name, quantity и measure) из строки string

    """
    def __init__(self, ingredient_name='', quantity=0, measure=''):
        self.name = ingredient_name
        self.quantity = quantity
        self.measure = measure

    def __str__(self):
        return ' | '.join((self.name, str(self.quantity), self.measure))

    def to_dict(self):
        return {'ingredient_name': self.name, 'quantity': int(self.quantity), 'measure': self.measure}

    def load_from_string(self, string):
        self.name, quantity, self.measure = (s.strip() for s in string.split('|'))
        self.quantity = int(quantity)


class Recipe:
    """Класс Recipe представляет рецепт блюда

    Класс имеет два параметра name - название блюда и ingredients - список ингредиентов.
    Ингредиенты в списке представленны словарями вида:
    {'ingredient_name': name, 'quantity': quantity, 'measure': measure}
    Мне кажется логичнее хранить рецепт списком экземпляров класса Ingredient. Это в дальнейшем бы позволило
    немного сократить код и избавить от "лишних" преобразований в словари.

    Метод __str__ переопределен для вывода экземпляра класса на экран функцией print().
    Метод __iadd__ переопределен для того чтобы можно было добавлять ингредиенты к рецептам оператором '+='
    оператором '+='
    Метод __mul__ переопределен для того чтобы можно было рецепт умножать на количество персон
    Метод to_dict() возвращает словарь с названием блюда и списком ингредиентов в соответствии с требованем задачи №1.
    """
    def __init__(self, name, *ingredients):
        self.name = name.capitalize()
        self.ingredients = [ingredient.to_dict() for ingredient in ingredients]

    def __str__(self):
        return f'{self.name}\n{len(self.ingredients)}\n' + "\n".join(str(Ingredient(**ingredient))
                                                                     for ingredient in self.ingredients) + '\n'

    def __iadd__(self, other):
        if isinstance(other, Ingredient):
            for ingredient in self.ingredients:
                if ingredient['ingredient_name'] == other.name:
                    ingredient['quantity'] += other.quantity
                    break
            else:
                self.ingredients.append(other.to_dict())
        return self

    def __mul__(self, other):
        result = Recipe(self.name, *[Ingredient(**ingredient) for ingredient in self.ingredients])
        for ingredient in result.ingredients:
            ingredient['quantity'] *= int(other)
        return result

    def to_dict(self):
        return {self.name: self.ingredients}


class ShopList(Recipe):
    """Класс ShopList представляет список покупок

    Метод __iadd__ переопределен для того чтобы можно было добавлять рецепты и ингредиенты всписок покупок
    оператором '+='.
    Метод to_dict() возвращает словарь со списком ингредиентов в соответствии с требованем задачи №2.
    """
    def __init__(self):
        super().__init__('Список покупок')

    def __iadd__(self, other):
        if isinstance(other, Recipe) or isinstance(other, type(self)):
            for new_ingredient in other.ingredients:
                super().__iadd__(Ingredient(**new_ingredient))
        elif isinstance(other, Ingredient):
            super().__iadd__(other)
        return self

    def to_shop_dict(self):
        return {ingredient['ingredient_name']: {'measure': ingredient['measure'],
                                                'quantity': ingredient['quantity']}
                for ingredient in self.ingredients}


class CookBook:
    """Класс CookBook представляет кулинарную книгу.

    Класс имеет один параметр recipes - словарь с рецептами.
    Метод __str__ переопределен для вывода экземпляра класса на экран функцией print().
    Метод add_recipe(recipe) добавляет рецепт в кулинарную книгу.
    Метод get_recipe(recipe_name) позволяет по названию блюда получить его состав.
    Метод load_from_file(path) считывает кулинарную книгу из файла path.
    Метод save_to_file(path) записывает кулинарную книгу в файл path.
    """
    def __init__(self):
        self.recipes = dict()

    def __str__(self):
        str = ''
        for recipe in self.recipes.keys():
            str += f'{recipe}\n'
            str += f'{len(self.recipes[recipe])}\n'
            str += "\n".join(Ingredient(**ingredient).__str__() for ingredient in self.recipes[recipe])
            str += '\n\n'
        return str

    def add_recipe(self, recipe):
        self.recipes.update(recipe.to_dict())

    def get_recipe(self, recipe_name):
        if recipe_name in self.recipes:
            return Recipe(recipe_name, *[Ingredient(**ingredient) for ingredient in self.recipes[recipe_name]])

    def load_from_file(self, path):
        with open(path) as file:
            self.recipes.clear()
            line = 'run!'
            while line != '':
                recipe = Recipe(file.readline().strip())
                for i in range(int(file.readline())):
                    ingredient = Ingredient()
                    ingredient.load_from_string(file.readline())
                    recipe += ingredient
                self.recipes.update(recipe.to_dict())
                line = file.readline()

    def save_to_file(self, path):
        with open(path, 'w') as file:
            file.write(str(self))


def get_shop_list_by_dishes(cook_book, person_count, *dishes):
    """Функция по заданию №2.
    Добавлен пареметр cook_book для того чтобы не "привязываться" к конкретной кулинарной книге
    """
    shop_list = ShopList()
    for dish in dishes:
        shop_list += cook_book.get_recipe(dish) * person_count
    return shop_list.to_shop_dict()

def get_shop_list(cook_book, **dishes):
    """Функция для создания более "сложных" списков покупок

    Список покупок генерируется по словарю вида
    dishes_dict = {'Утка по-пекински': 2, 'Фахитос': 4, 'Омлет': 5},
    где ключи - наименования блюд, а значения - количество персон
    """
    shop_list = ShopList()
    for dish in dishes.keys():
        shop_list += cook_book.get_recipe(dish) * dishes[dish]
    return shop_list.to_shop_dict()


dishes = ['Утка по-пекински', 'Фахитос', 'Омлет']
dishes_dict = {'Утка по-пекински': 2, 'Фахитос': 4, 'Омлет': 5}

cook_book = CookBook()
cook_book.load_from_file('recipes.txt')
print(cook_book)
print(get_shop_list_by_dishes(cook_book, 3, *dishes))
print(get_shop_list(cook_book, **dishes_dict))

"""Создание новой кулинарной книги и сохранение в файл"""
hedgehog = [{'ingredient_name': 'Колбаса копченая', 'quantity': 100, 'measure': 'г.'},
            {'ingredient_name': 'Сыр твердый', 'quantity': 100, 'measure': 'г.'},
            {'ingredient_name': 'Кукуруза консервированная', 'quantity': 100, 'measure': 'г.'},
            {'ingredient_name': 'Яйцо', 'quantity': 3, 'measure': 'шт.'},
            {'ingredient_name': 'Чеснок', 'quantity': 1, 'measure': 'зубч.'},
            {'ingredient_name': 'Майонез', 'quantity': 80, 'measure': 'г.'}]

sea_red = [{'ingredient_name': 'Крабовые палочки', 'quantity': 250, 'measure': 'г.'},
           {'ingredient_name': 'Помидоры', 'quantity': 2, 'measure': 'шт.'},
           {'ingredient_name': 'Сыр', 'quantity': 150, 'measure': 'г.'},
           {'ingredient_name': 'Чеснок', 'quantity': 2, 'measure': 'зубч.'},
           {'ingredient_name': 'Майонез', 'quantity': 60, 'measure': 'г.'}]

salades = CookBook()
salades.add_recipe(Recipe('Ёжик', *[Ingredient(**ingredient) for ingredient in hedgehog]))
salades.add_recipe(Recipe('Красное море', *[Ingredient(**ingredient) for ingredient in sea_red]))
salades.save_to_file('salades.txt')

"""Теперь можно создавать списки покупок по нескольким кулинарным книгам"""
print('---------------')
shop_list = ShopList()
shop_list += cook_book.get_recipe('Запеченный картофель')
shop_list += salades.get_recipe('Ёжик')
print(shop_list)

"""Список покупок можно сохранить в файл"""
shop_book = CookBook()
shop_book.add_recipe(shop_list)
print(shop_book)
shop_book.save_to_file('shoplist.txt')
