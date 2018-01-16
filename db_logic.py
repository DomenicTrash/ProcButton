import datetime
import sqlite3

MY_DB = "my_db.db"
AUTO_USE_STARS = False


def create_db():
    db = sqlite3.connect(MY_DB)
    c = db.cursor()
    try:
        c.execute('''CREATE TABLE main_table
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TIMESTAMP, 
                     current_streak INT, max_streak INT, next_star INT, stars INT)''')
        add_empty_row()
    except sqlite3.OperationalError:  # table already exists
        print("Table already exists.")
    finally:
        db.commit()
        db.close()


def drop_table_db():
    db = sqlite3.connect(MY_DB)
    c = db.cursor()
    try:
        c.execute('''DROP TABLE main_table''')
    finally:
        db.commit()
        db.close()


def add_row(one_row_obj):
    db = sqlite3.connect(MY_DB)
    c = db.cursor()
    try:
        c.execute('''INSERT INTO main_table (created_at, current_streak, max_streak, next_star, stars)
                                 VALUES (?,?,?,?,?)''', (one_row_obj.created_at,
                                                         one_row_obj.current_streak, one_row_obj.max_streak,
                                                         one_row_obj.next_star, one_row_obj.stars))
    except sqlite3.Error as e:
        print("Error in add_row()")
        print(e)
        db.rollback()
    finally:
        print("added row")
        db.commit()
        db.close()


def get_last_row():
    # -> OneRow
    # added paramters to get a date object instead of a string
    db = sqlite3.connect(MY_DB, detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    # db.row_factory = sqlite3.Row
    # used custom object to have the attributes in the correct types instead of strings
    c = db.cursor()
    c.execute("SELECT * FROM main_table ORDER BY id DESC LIMIT 1")
    row = OneRow(c.fetchone())
    db.close()
    return row


def add_empty_row():
    row = OneRow([0, datetime.datetime.today(), 0, 0, 0, 0])
    add_row(row)


# Reset current_streak and next_star or automtically use one star
def add_zero_day_row():
    r = get_last_row()
    created_at = datetime.datetime.today()
    current_streak = 0
    next_star = 0
    stars = r.stars

    if AUTO_USE_STARS:
        if r.stars >= 1:
            current_streak = r.current_streak
            next_star = r.next_star
            stars = r.stars - 1

    new_row = OneRow([r.id, created_at, current_streak, r.max_streak, next_star, stars])
    add_row(new_row)


def add_incremented_row():
    # gets called after button was pressed
    r = get_last_row()
    created_at = datetime.datetime.today()
    current_streak = r.current_streak + 1
    max_streak = is_max_streak(current_streak, r.max_streak)
    next_star, stars = increment_stars(r.next_star, r.stars)
    new_row = OneRow([r.id, created_at, current_streak, max_streak, next_star, stars])
    add_row(new_row)


def use_star():
    r = get_last_row()
    created_at = datetime.datetime.today()
    stars = r.stars - 1
    new_row = OneRow([r.id, created_at, r.current_streak, r.max_streak, r.next_star, stars])
    add_row(new_row)


def check_if_row_was_added():
    # if no row for yesterdays date, add_zero_day_row()
    r = get_last_row()
    date_last_row = r.created_at.date()
    if not is_date_from_yesterdy(date_last_row):
        add_zero_day_row()
    else:
        if r.next_star == 3:
            set_next_star_to_zero_in_last_row()


def set_next_star_to_zero_in_last_row():
    r = get_last_row()
    db = sqlite3.connect(MY_DB)
    c = db.cursor()
    try:
        c.execute('''UPDATE main_table SET next_star = ? WHERE id = ?''', (0, r.id))
    except sqlite3.Error as e:
        print("Error in remove_next_star_last_row()")
        print(e)
        db.rollback()
    finally:
        db.commit()
        db.close()


def was_already_added_today():
    r = get_last_row()
    date_last_row = r.created_at.date()
    return datetime.date.today() == date_last_row


def count_total_days():
    db = sqlite3.connect(MY_DB, detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = db.cursor()
    c.execute("SELECT count(current_streak) FROM main_table WHERE current_streak != 0")
    count = c.fetchall()
    db.close()
    return count[0][0]


#######################################
# Update logic
#######################################
def increment_stars(next_star, stars):
    next_star += 1
    if next_star == 4:
        next_star = 0
        stars += 1
    return next_star, stars


def is_max_streak(current_streak, max_streak):
    if current_streak > max_streak:
        max_streak = current_streak
    else:
        max_streak = max_streak
    return max_streak


def is_date_from_yesterdy(date):
    date_yesterday = datetime.date.today() - datetime.timedelta(1)
    if date == date_yesterday:
        return True
    return False


class OneRow:
    def __init__(self, row_list):
        if row_list is not None:
            self.id = row_list[0]
            self.created_at = row_list[1]
            self.current_streak = row_list[2]
            self.max_streak = row_list[3]
            self.next_star = row_list[4]
            self.stars = row_list[5]


if __name__ == '__main__':
    create_db()
    # add_incremented_row()
    # add_zero_day_row()
    # count_total_days()
    # set_next_star_to_zero_last_row()
