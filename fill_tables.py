from start import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sweater.models import University, Ranks

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1qa2ws@localhost/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def add_subjects():
    subjects_names = ['Русский язык', 'Математика', 'Физика', 'Химия',
                      'История', 'Обществознание', 'Информатика и ИКТ', 'Биология',
                      'География', 'Иностранный язык', 'Литература', 'Доп. баллы*']

    for i in range(len(subjects_names)):
        min_score = 36
        max_score = 100
        if i == 11:
            min_score = 0
            max_score = 110
        subject = Subject(name=subjects_names[i], min_score=min_score, max_score=max_score)
        try:
            db.session.add(subject)
            db.session.commit()
        except:
            print('Error')


def add_universities():
    universities = [['КФУ', 'Казанский (Приволжский) федеральный университет', 'Казань', 1751],
                    ['КГЭУ', 'Казанский государственный энергетический университет', 'Казань', 1782],
                    ['КНИТУ', 'Казанский национальный исследовательский технологический университет', 'Казань', 1773],
                    ['КНИТУ-КАИ', 'Казанский национальный исследовательский технический университет им. А.Н. Туполева - КАИ', 'Казань', 5428]]

    count = 0
    for i in range(len(universities)):
        university = University(name=universities[i][0], full_name=universities[i][1], city=universities[i][2], vuzopedia_id=universities[i][3])
        try:
            db.session.add(university)
            db.session.commit()
            count += 1
            print(count)
        except:
            print('Error')


def add_ranks():
    ranks = [['Абитуриент', 0],
             ['Бакалавр', 2],
             ['Магистр', 4],
             ['Кандидат наук', 8],
             ['Доктор наук', 16],
             ['Профессор', 32]]

    count = 0
    for i in range(len(ranks)):
        rank = Ranks(name=ranks[i][0], score=ranks[i][1])
        try:
            db.session.add(rank)
            db.session.commit()
            count += 1
            print(count)
        except:
            print('Error')


# add_subjects()
# add_universities()
# add_ranks()
