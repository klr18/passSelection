import tkinter as tk
from tkinter import messagebox
import random
import string


# Генерация случайного пароля
def generate_password(length, char_set):
    if not char_set:
        raise ValueError("Набор символов не может быть пустым.")
    return ''.join(random.choice(char_set) for _ in range(length))


# Фитнес-функция (сравнивает пароли)
def fitness(password, target_password):
    return sum(1 for i in range(len(password)) if password[i] == target_password[i])


# Турнирный отбор
def tournament_selection(population, target_password, k=5):
    tournament = random.sample(population, k)
    tournament = sorted(tournament, key=lambda p: fitness(p, target_password), reverse=True)
    return tournament[0]


# Кроссовер (смешивание двух родителей)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child


# Мутация (случайное изменение символа)
def mutate(password, char_set, mutation_rate=0.01):
    password = list(password)
    for i in range(len(password)):
        if random.random() < mutation_rate:
            password[i] = random.choice(char_set)
    return ''.join(password)


# Генетический алгоритм для подбора пароля
def genetic_algorithm(target_password, char_set, population_size=100, generations=1000):
    population = [generate_password(len(target_password), char_set) for _ in range(population_size)]

    for generation in range(generations):
        population = sorted(population, key=lambda p: fitness(p, target_password), reverse=True)
        if fitness(population[0], target_password) == len(target_password):
            return population[0], generation

        new_population = population[:10]  # Отбираем 10 лучших
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, target_password)
            parent2 = tournament_selection(population, target_password)
            child = crossover(parent1, parent2)
            child = mutate(child, char_set)
            new_population.append(child)

        population = new_population

    return population[0], generations


# Интерфейс с использованием Tkinter
class PasswordGeneticGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Генетический алгоритм подбора пароля")

        # Все возможные символы для пароля (по умолчанию)
        self.default_char_set = string.ascii_letters + string.digits + string.punctuation

        # Настройки интерфейса
        self.target_password_label = tk.Label(root, text="Введите целевой пароль:")
        self.target_password_label.grid(row=0, column=0)
        self.target_password_entry = tk.Entry(root, show="*")
        self.target_password_entry.grid(row=0, column=1)

        self.char_set_label = tk.Label(root, text="Выберите набор символов:")
        self.char_set_label.grid(row=1, column=0)
        self.char_set_entry = tk.Entry(root)
        self.char_set_entry.grid(row=1, column=1)
        # Устанавливаем набор символов по умолчанию
        self.char_set_entry.insert(0, self.default_char_set)

        self.population_size_label = tk.Label(root, text="Размер популяции:")
        self.population_size_label.grid(row=2, column=0)
        self.population_size_entry = tk.Entry(root)
        self.population_size_entry.grid(row=2, column=1)
        self.population_size_entry.insert(0, "100")

        self.generations_label = tk.Label(root, text="Количество поколений:")
        self.generations_label.grid(row=3, column=0)
        self.generations_entry = tk.Entry(root)
        self.generations_entry.grid(row=3, column=1)
        self.generations_entry.insert(0, "1000")

        self.mutation_rate_label = tk.Label(root, text="Скорость мутации:")
        self.mutation_rate_label.grid(row=4, column=0)
        self.mutation_rate_entry = tk.Entry(root)
        self.mutation_rate_entry.grid(row=4, column=1)
        self.mutation_rate_entry.insert(0, "0.01")

        self.start_button = tk.Button(root, text="Начать подбор", command=self.start_genetic_algorithm)
        self.start_button.grid(row=5, column=0, columnspan=2)

        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=6, column=0, columnspan=2)

    def start_genetic_algorithm(self):
        target_password = self.target_password_entry.get()
        char_set = self.char_set_entry.get()

        # Проверка, что набор символов не пустой
        if not char_set:
            messagebox.showerror("Ошибка", "Набор символов не может быть пустым!")
            return

        # Установка дефолтных значений, если пользователь не указал параметры
        population_size = int(self.population_size_entry.get()) if self.population_size_entry.get() else 100
        generations = int(self.generations_entry.get()) if self.generations_entry.get() else 1000
        mutation_rate = float(self.mutation_rate_entry.get()) if self.mutation_rate_entry.get() else 0.01

        try:
            # Запуск алгоритма
            found_password, generations_taken = genetic_algorithm(target_password, char_set, population_size,
                                                                  generations)

            if fitness(found_password, target_password) == len(target_password):
                messagebox.showinfo("Успех", f"Пароль найден: {found_password}\nПоколений: {generations_taken}")
            else:
                messagebox.showinfo("Завершено",
                                    f"Процесс завершен, но пароль не найден за {generations_taken} поколений.")

            # Обновление результата на экране
            self.result_label.config(text=f"Найденный пароль: {found_password}\nПоколений: {generations_taken}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")


# Создание окна
root = tk.Tk()
gui = PasswordGeneticGUI(root)
root.mainloop()
