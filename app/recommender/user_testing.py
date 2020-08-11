import sqlite3


def get_db():
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    return conn, c


def start_user_test(user_id):
    reset_testing(user_id)
    conn, c = get_db()
    query = "INSERT INTO user_testing (user_id, round) VALUES (?,1);"
    conn.execute(query, (user_id,))
    conn.commit()

    return


def get_user_round(user_id):
    conn, c = get_db()
    query = "SELECT round FROM user_testing where user_id == ? ;"
    c.execute(query, (user_id,))
    # c.execute(query)
    result = c.fetchall()
    if len(result) == 0:
        return False
    # this returns list of tuples
    # print(result[0][0]
    else:
        return result[0][0]


def next_user_testing_round(user_id):
    if check_if_testing_over(user_id):
        return
    else:
        current_round = get_user_round(user_id)
        current_round += 1
        conn, c = get_db()
        query = "UPDATE user_testing SET round = ? where user_id = ?;"
        conn.execute(query, (current_round, user_id,))
        conn.commit()
    return current_round


def reset_testing(user_id):
    conn, c = get_db()
    query = "DELETE FROM user_testing where user_id == ?"
    c.execute(query, (user_id,))
    conn.commit()
    return


def return_settings(user_id):
    # returns a triple of pearson,title_and_poster,random_explanations
    # pearson = 1 means pearsons recommendations
    # title_and_poster = 1 means show title and posters
    # random_explanations = 1 means random explatnation scores
    current_round = get_user_round(user_id)
    triple_dict = {1: (0, 0, 0),
                   2: (0, 1, 0),
                   3: (0, 1, 1),
                   4: (1, 0, 0),
                   5: (1, 1, 0),
                   6: (1, 1, 1)}
    if current_round == 0:
        return (1, 1, 0)

    # print(triple_dict[current_round])
    return triple_dict[current_round]


def check_if_testing_over(user_id):
    current_round = get_user_round(user_id)
    if current_round == 6:
        reset_testing(user_id)
        return True
    else:
        return False


def check_if_trial_exists(user_id):
    if get_user_round(user_id):
        return get_user_round(user_id)

    


if __name__ == "__main__":
    start_user_test(1)
    get_user_round(1)
    next_user_testing_round(1)
    get_user_round(1)
    return_settings(1)
