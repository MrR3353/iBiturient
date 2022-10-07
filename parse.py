import requests
from bs4 import BeautifulSoup
from sweater.models import Direction
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def get_num(line):
    num = ''
    for char in line:
        if char.isdigit():
            num += char
    if num == '':
        return None  # No such education form
    return int(num)


def parse_and_write_txt(university_id):
    f = open('data.txt', 'w')   # clear
    f.close()

    stop = False
    for i in range(1, 9):
        if stop:
            break
        page = requests.get('https://vuzopedia.ru/vuz/' + str(university_id) + '/spec?page=' + str(i))

        if page.status_code == 200:
            html = page.text
            soup = BeautifulSoup(html, 'html.parser')
            university = soup.find('div', {'class': 'choosevuz insertVpm'}).find('span').text.strip()
            items = soup.find_all('div', {'class': 'itemSpecAll'})
            for item in items:
                name = item.find('a', {'class': 'spectittle'}).text
                ed_form = item.find('i').text
                subjects = item.find('span').text
                scores = item.find_all('div', {'class': 'col-md-4 itemSpecAllParamWHide newbl'})
                try:
                    del(scores[0])
                except:
                    stop = True
                    break

                with open('data.txt', 'a') as f:
                    f.write(name + '\n')
                    f.write(university + '\n')
                    f.write(ed_form + '\n')
                    f.write(subjects + '\n')
                    for score in scores:
                        try:
                            score = score.find('a', {'class':'tooltipq'}).text
                            score = get_num(score)
                        except AttributeError:
                            score = None    # No such education form
                        f.write(str(score) + '\n')
        else:
            print('Error', page.status_code)


def read_txt_write_db():
    count = 0
    with open('data.txt', 'r') as f:
        while True:
            name = f.readline()
            if not name:
                break
            university = f.readline()
            ed_form = f.readline()
            subjects = f.readline()
            budget = f.readline()
            paid = f.readline()
            if budget == 'None\n':  # No such education form
                budget = None
            if paid == 'None\n':    # No such education form
                paid = None

            direction = Direction(name=name, university=university, ed_form=ed_form,
                                  subjects=subjects, budget=budget, paid=paid)

            app = Flask(__name__)
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1qa2ws@localhost/db'
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            db = SQLAlchemy(app)

            try:
                db.session.add(direction)
                db.session.commit()
                count += 1
                print(count)
            except:
                print('Error')


# 1751 1782 5428 1773
university_id = 1773
# parse_and_write_txt(university_id)
read_txt_write_db()