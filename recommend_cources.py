import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Загружаем данные о студентах и курсах
students = pd.read_csv("students.csv", sep=";", decimal=",", encoding="windows-1251")
courses = pd.read_csv("courses.csv", sep=";", decimal=",", encoding="windows-1251")

# Настраиваем отображение всех строк и колонок таблицы курсов и студентов
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

# Строим матрицу оценок студентов по каждому курсу, заполняя значения Nan нулями
ratings = pd.pivot_table(students, values='Рейтинг', index=['id'], columns=['Курс']).fillna(0)

# Строим матрицу сходства курсов
similarities = cosine_similarity(ratings.T)

# Функция рекомендации курсов
def recommend_courses(student_id, n):
    # Получаем оценки выбранного студента
    student = ratings.loc[student_id, :]
    # Вычисляем косинусное сходство между оценками выбранного студента и оценками других студентов
    sims = ratings.apply(lambda row: cosine_similarity([student], [row])[0][0], axis=1)
    # Сортируем cтудентов по убыванию сходства
    sims = sims.sort_values(ascending=False)
    print(sims)
    # Выбираем n+1 студентов с наибольшим сходством по оценкам, включая самого студента
    topn = sims.iloc[:n + 1]
    # Выбираем id студентов в количестве n
    id_topn = list(topn.index)
    # Выбираем оценки n ближайших
    id_students = [ratings.values[user_id - 1] for user_id in id_topn]
    marks = [[0, 0] for _ in range(len(courses.values))]
    # Находим среднюю оценку среди схожих по оценках студентов
    for i in range(1, len(id_students)):
        for number_mark, mark in enumerate(id_students[i]):
            if mark > 0:
                marks[number_mark][0] += 1
                marks[number_mark][1] += mark
    middle_marks = [part_mark[1] / part_mark[0] if part_mark[1] > 0 else 0 for part_mark in marks]
    # Подбираем по индексам курсы, которые пользователь ещё не проходил
    id_reccomend_cources = list()
    mark_user = list(id_students[0])
    print(mark_user)
    for index_mark, mark in enumerate(middle_marks):
        if mark >= 3 and mark_user[index_mark] == 0:
            id_reccomend_cources.append(index_mark + 1)
    # Получаем информацию о курсах из датафрейма с курсами
    course_info = courses[courses["id"].isin(id_reccomend_cources)]
    # Возвращаем список рекомендованных курсов
    recommended_courses = list(course_info["Название курса"])
    return recommended_courses

print(recommend_courses(5, 2))
