from flask import render_template, request, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from sweater import app, db, login_manager
from sweater.models import Subject, User, Direction, Log, University, Comment


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', Subject=Subject)


@app.route('/directions')   # all available directions
def directions():
    if len(request.args) == 0:  # GET without args
        directions = Direction.query.order_by(Direction.name).all()
        return render_template('directions.html', directions=directions)
    else:   # GET with filtering by points
        rus = request.args.get('rus')
        math = request.args.get('math')
        phys = request.args.get('phys')
        chem = request.args.get('chem')
        hist = request.args.get('hist')
        soc = request.args.get('soc')
        inf = request.args.get('inf')
        bio = request.args.get('bio')
        geo = request.args.get('geo')
        lang = request.args.get('lang')
        litr = request.args.get('litr')
        extra = request.args.get('extra')
        subjects_points = [rus, math, phys, chem, hist, soc, inf, bio, geo, lang, litr, extra]

        for i in range(len(subjects_points)):  # converting subjects to int
            if subjects_points[i] == "":
                subjects_points[i] = 0
            else:
                subjects_points[i] = int(subjects_points[i])

        points_sum = sum(subjects_points)

        subjects_names = ['русский', 'математика', 'физика', 'химия',
                          'история', 'обществознание', 'информатика', 'биология',
                          'география', 'иностранный язык', 'литература']  # dont calc 'вступительные' because this points always will be added to final result
        name_to_ind = {}    # translate subject name to index in subjects_points
        for i in range(len(subjects_names)):
            name_to_ind[subjects_names[i]] = i

        passed_subjects = []
        for i in range(len(subjects_names)):
            if subjects_points[i] > 0:
                passed_subjects.append(subjects_names[i])
        print(passed_subjects)

        filtered_directions = []    # directions where user can enroll on budget
        scored_direction_points = []   # scored points for that direction (on that subjects)

        if request.args.get('flexRadioDefault') == 'budget':  # user choose budget places
            directions = Direction.query.order_by(Direction.budget).all()
        else:  # user choose paid places
            directions = Direction.query.order_by(Direction.paid).all()

        for direction in directions:
            necessary_subj = direction.subjects.strip().split(', ')
            # Change математика, русский, физика/информатика to:
            # [['математика'], ['русский'], ['физика', 'информатика']]
            for i in range(len(necessary_subj)):
                necessary_subj[i] = necessary_subj[i].split('/')

            # remove 'вступительные' because this points always will be added to final result
            if ['вступительные'] in necessary_subj:
                necessary_subj.remove(['вступительные'])
            print(necessary_subj)

            have_necessary_subj = False  # check that we necessary subjects for that direction
            for subjects in necessary_subj:
                have_necessary_subj = False
                for subject in subjects:   # can be few subjects on choice (физика/информатика)
                    if subject in passed_subjects:
                        have_necessary_subj = True
                if not have_necessary_subj:
                    break

            if have_necessary_subj:
                print('OK')
                points_combinations = [0]  # scored points combinations for each combination of necessary subjects
                for subjects in necessary_subj:
                    if len(subjects) == 1:
                        for i in range(len(points_combinations)):    # add passed points to this subj to all points combination
                            points_combinations[i] += subjects_points[name_to_ind[subjects[0]]]
                    else:
                        subjects_scored_points = []
                        for subject in subjects:  # can be few subjects on choice (физика/информатика)
                            if subject in passed_subjects:  # subj can be not passed
                                subjects_scored_points.append(subjects_points[name_to_ind[subject]])
                        # making all combinations from sum of points_combinations and subjects_scored_points
                        #   FOR EXAMPLE   subjects_scored_points      5 7 12
                        #                 prev_points_combinations    4 9
                        #                                             9 14 11 16 16 21
                        prev_points_combinations = points_combinations.copy()
                        points_combinations.clear()
                        for i in range(len(prev_points_combinations)):
                            for j in range(len(subjects_scored_points)):
                                points_combinations.append(prev_points_combinations[i] + subjects_scored_points[j])
                print(points_combinations)

                if request.args.get('flexRadioDefault') == 'budget':  # user choose budget places
                    if direction.budget is None:
                        continue

                    total_score = max(points_combinations) + subjects_points[11]
                    # check that max combination + additional points > budget
                    if max(points_combinations) + subjects_points[11] >= direction.budget:
                        scored_direction_points.append(total_score)
                        filtered_directions.append(direction)
                else:   # user choose paid places
                    if direction.paid is None:
                        continue

                    total_score = max(points_combinations) + subjects_points[11]
                    # check that max combination + additional points > paid
                    if max(points_combinations) + subjects_points[11] >= direction.paid:
                        scored_direction_points.append(total_score)
                        filtered_directions.append(direction)

            else:
                print('NOT')
                continue

        # математика, русский, физика
        # математика, русский, физика / информатика
        # русский, обществознание, математика / биология / иностранный язык
        # русский, литература, вступительные
        # русский, обществознание / история / иностранный язык, вступительные

        return render_template('directions.html', directions=filtered_directions, points_sum=points_sum,
                               scored_direction_points=scored_direction_points)


@app.route('/create', methods=['POST', 'GET'])  # create new direction
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        university = request.form['university']
        ed_form = request.form['ed_form']
        subjects = request.form['subjects']
        budget = request.form['budget']
        paid = request.form['paid']
        print(name, university, ed_form, subjects, budget, paid)

        direction = Direction(name=name, university=university, ed_form=ed_form,
                              subjects=subjects, budget=budget, paid=paid)

        try:
            db.session.add(direction)
            db.session.commit()
            return render_template('create.html', status="OK")
        except:
            return render_template('create.html', status="ERROR")
    else:
        return render_template('create.html')


@app.route('/directions/<int:id>/delete')   # delete direction
def delete(id):
    direction = Direction.query.get_or_404(id)
    try:
        db.session.delete(direction)
        db.session.commit()
        return redirect('/directions')
    except:
        return 'При удалении произошла ошибка'


@app.route('/login', methods=['POST', 'GET'])   # login on site
def login():
    if current_user.is_authenticated:
        return render_template('profile.html')

    email = request.form.get('loginEmail')
    password = request.form.get('loginPassword')

    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            # logging
            log = Log(text='Log in', user_id=current_user.id)
            db.session.add(log)
            db.session.commit()

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('/login')
        else:
            flash('Неверный логин или пароль!')
    else:
        flash('Нужно ввести логин и пароль!')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])   # logout on site
@login_required
def logout():
    # logging
    log = Log(text='Log out', user_id=current_user.id)
    db.session.add(log)
    db.session.commit()
    logout_user()
    return redirect('/login')


@app.route('/register', methods=['POST'])   # register new user on site
def register():
    name = request.form['registerUsername']
    email = request.form['registerEmail']
    password = request.form['registerPassword']
    repeat_password = request.form['registerRepeatPassword']
    print(name, email, password, repeat_password)
    if not (name or email or password or repeat_password):
        flash('Не все поля заполнены')
        return redirect('/login')
        # return render_template('login.html')
    elif password != repeat_password:  # validation
        flash('Пароли не совпадают')
        return redirect('/login')
        # return render_template('login.html')
    else:
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Пользователь с таким адресом электронной почты уже есть')
            return redirect('/login')
            # return render_template('login.html')
        hash = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hash)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        # logging - REPLACE WITH TRIGGER
        # log = Log(text='Register', user_id=current_user.id)
        # db.session.add(log)
        # db.session.commit()

        return redirect('/login')


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect('/login' + '?next=' + request.url)
    return response


@app.route('/universities')
def universities():
    universities_lst = University.query.order_by(University.name).all()
    return render_template('universities.html', universities=universities_lst)


@app.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    if request.method == 'POST':
        text = request.form['text']
        comment = Comment(text=text, user_id=current_user.id)

        try:
            db.session.add(comment)
            db.session.commit()
        except:
            flash('Произошла ошибка')

    comments = Comment.query.order_by(Comment.date.desc()).all()
    return render_template('forum.html', comments=comments, User=User)  # User for defying authors of comments


@app.route('/events')
def events():
    logs = Log.query.order_by(Log.date.desc()).all()
    return render_template('events.html', logs=logs, User=User)  # User for defying authors of comments
