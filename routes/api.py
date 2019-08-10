from flask import Flask, request, session, jsonify
import mysql.connector
import json

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'asd123asd123'


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/users/add/', methods=['POST'])
def add_user():
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',
                                             database='work_it_db',
                                             user='root',
                                             password='ferfer19')
        cursor = connection.cursor()
        req_data = request.get_json()
        username = req_data['user']['username']
        password = req_data['user']['password']
        name = req_data['user']['additional_info']['name']
        if not name:
            name = None

        try:
            sql_insert_query = """ INSERT INTO `user`
                                         (`username`, `password`) VALUES (%s,%s)"""

            insert_tuple = (username, password)
            result = cursor.execute(sql_insert_query, insert_tuple)
            id_user = cursor.lastrowid
            sql_insert_query = """ INSERT INTO `user_info`
                                                     (`id_user`, `name`) VALUES (%s,%s)"""

            insert_tuple = (id_user, name)
            result = cursor.execute(sql_insert_query, insert_tuple)
            connection.commit()
            return "Record inserted successfully into python_users table"
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed inserting record into python_users table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/users/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            msg = ''
            # Getting data
            req_data = request.get_json()
            username = req_data['user']['username']
            password = req_data['user']['password']
            print(username + "," + password)

            # Check if account exists using MySQL
            connection = mysql.connector.connect(host='localhost',
                                                 database='work_it_db',
                                                 user='root',
                                                 password='ferfer19')
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
            # Fetch one record and return result
            account = cursor.fetchone()

            # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = int(account[0])
                session['username'] = account[1]
                # Redirect to home page
                return 'Logged in successfully!'
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
                return msg
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed inserting record into python_users table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/users/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return "logout"


@app.route('/users/<int:user_id>', methods=['GET'])
def get_info_user(user_id):
    if request.method == 'GET':
        try:
            msg = ''
            # Check if account exists using MySQL
            connection = mysql.connector.connect(host='localhost',
                                                 database='work_it_db',
                                                 user='root',
                                                 password='ferfer19')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user WHERE id = " + str(user_id))
            # Fetch one record and return result
            account = cursor.fetchone()

            # If account exists in accounts table in out database
            if account:
                cursor.execute("SELECT * FROM user_info WHERE id_user = " + str(user_id))
                account_info = cursor.fetchone()
                if account_info:
                    return jsonify(
                        id=account[0],
                        username=account[1],
                        name=account_info[1]
                    )
                else:
                    return jsonify(
                        username=account[1],
                        id=account[0]
                    )
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
                return msg
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed getting record from users table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/users/update/<int:user_id>', methods=['POST'])
def update_info_user(user_id):
    if request.method == 'POST':
        try:
            msg = ''
            req_data = request.get_json()

            connection = mysql.connector.connect(host='localhost',
                                                 database='work_it_db',
                                                 user='root',
                                                 password='ferfer19')

            cursor = connection.cursor()

            if req_data['user']['username']:
                print("Updating username")
                cursor.execute("UPDATE `user` SET `username` = '" + str(req_data['user']['username'])
                               + "' WHERE (`id` = " + str(user_id) + ")")
            if req_data['user']['password']:
                print("Updating password")
                cursor.execute("UPDATE `user` SET `password` = '" + str(req_data['user']['password'])
                               + "' WHERE (`id` = " + str(user_id) + ")")
            if req_data['user']['additional_info']['name']:
                print("Updating name")
                cursor.execute("UPDATE `user_info` SET `name` = '" + str(req_data['user']['additional_info']['name'])
                               + "' WHERE (`id_user` = " + str(user_id) + ")")
            connection.commit()
            return "Update successfully"
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed getting record from users table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/jobs/categories/add', methods=['POST'])
def add_category():
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',
                                             database='work_it_db',
                                             user='root',
                                             password='ferfer19')
        cursor = connection.cursor()
        req_data = request.get_json()
        name = req_data['category']['name']

        try:
            sql_insert_query = " INSERT INTO `job_category` (`name`) VALUES ('" + name + "')"

            result = cursor.execute(sql_insert_query)

            connection.commit()
            return "Record inserted successfully into job_category table"
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed inserting record into job_category table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/jobs/status/add', methods=['POST'])
def add_status():
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',
                                             database='work_it_db',
                                             user='root',
                                             password='ferfer19')
        cursor = connection.cursor()
        req_data = request.get_json()
        desc = req_data['status']['desc']

        try:
            sql_insert_query = " INSERT INTO `job_status` (`desc`) VALUES ('" + desc + "')"

            result = cursor.execute(sql_insert_query)

            connection.commit()
            return "Record inserted successfully into job_status table"
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed inserting record into job_category table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/jobs/add', methods=['POST'])
def add_job():
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',
                                             database='work_it_db',
                                             user='root',
                                             password='ferfer19')
        cursor = connection.cursor()
        req_data = request.get_json()
        print(str(req_data))
        title = req_data['job']['title']
        description = req_data['job']['description']
        creator = req_data['job']['creator']
        category = req_data['job']['category']

        try:
            sql_insert_query = " INSERT INTO `actual_jobs`" \
                               " (`title`,`description`,`creator`,`category`,`creation_time`) VALUES " \
                               "('" + title + "', '" + description + "', " + str(creator) + ", " + str(category) + ", (SELECT UNIX_TIMESTAMP()))"
            print(sql_insert_query)
            result = cursor.execute(sql_insert_query)

            connection.commit()
            return "Record inserted successfully into job_category table"
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed inserting record into job_category table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/jobs/<int:job_id>', methods=['GET'])
def get_info_job(job_id):
    if request.method == 'GET':
        try:
            msg = ''
            # Check if account exists using MySQL
            connection = mysql.connector.connect(host='localhost',
                                                 database='work_it_db',
                                                 user='root',
                                                 password='ferfer19')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM actual_jobs WHERE id = " + str(job_id))
            # Fetch one record and return result
            job = cursor.fetchone()

            # If account exists in accounts table in out database
            if job:
                return jsonify(
                    id=job[0],
                    title=job[1],
                    description=job[2],
                    creator=job[3],
                    category=job[4]
                )
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect job id!'
                return msg
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed getting record from actual_jobs table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/jobs/update/<int:job_id>', methods=['POST'])
def update_info_job(job_id):
    if request.method == 'POST':
        try:
            msg = ''
            req_data = request.get_json()

            connection = mysql.connector.connect(host='localhost',
                                                 database='work_it_db',
                                                 user='root',
                                                 password='ferfer19')

            cursor = connection.cursor()

            if req_data['job']['title']:
                print("Updating title")
                cursor.execute("UPDATE `actual_jobs` SET `title` = '" + str(req_data['job']['title'])
                               + "' WHERE (`id` = " + str(job_id) + ")")
            if req_data['job']['description']:
                print("Updating description")
                cursor.execute("UPDATE `actual_jobs` SET `description` = '" + str(req_data['job']['description'])
                               + "' WHERE (`id` = " + str(job_id) + ")")
            if req_data['job']['creator']:
                print("Updating creator")
                cursor.execute("UPDATE `actual_jobs` SET `creator` = '" + str(req_data['job']['creator'])
                               + "' WHERE (`id` = " + str(job_id) + ")")
            if req_data['job']['category']:
                print("Updating category")
                cursor.execute("UPDATE `actual_jobs` SET `category` = '" + str(req_data['job']['category'])
                               + "' WHERE (`id` = " + str(job_id) + ")")
            connection.commit()
            return "Update successfully"
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed getting record from users table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/jobs/categories/<int:category_id>', methods=['GET'])
def get_info_category(category_id):
    if request.method == 'GET':
        try:
            msg = ''
            # Check if account exists using MySQL
            connection = mysql.connector.connect(host='localhost',
                                                 database='work_it_db',
                                                 user='root',
                                                 password='ferfer19')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM job_category WHERE id = " + str(category_id))
            # Fetch one record and return result
            job = cursor.fetchone()

            # If account exists in accounts table in out database
            if job:
                return jsonify(
                    id=job[0],
                    name=job[1]
                )
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect job id!'
                return msg
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed getting record from actual_jobs table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/jobs/user/status/add', methods=['POST'])
def add_job_user_status():
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',
                                             database='work_it_db',
                                             user='root',
                                             password='ferfer19')
        cursor = connection.cursor()
        req_data = request.get_json()
        print(str(req_data))
        desc = req_data['status']['desc']

        try:
            sql_insert_query = " INSERT INTO `job_user_status`" \
                               " (`desc`) VALUES " \
                               "('" + desc + "')"
            result = cursor.execute(sql_insert_query)

            connection.commit()
            return "Record inserted successfully into job_category table"
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed inserting record into job_category table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/func/apply', methods=['POST'])
def apply_for_job():
    if request.method == 'POST':
        try:
            req_data = request.get_json()
            id_user = session['id']
            id_job = req_data['job']['id_job']
            status = req_data['job']['status']

            connection = mysql.connector.connect(host='localhost',
                                                 database='work_it_db',
                                                 user='root',
                                                 password='ferfer19')
            cursor = connection.cursor()

            sql_insert_query = "INSERT INTO `job_user` (`id_user`, `id_job`, `applying_time`, `status`) VALUES (" + str(id_user) + ", " + str(id_job) + ",  (SELECT UNIX_TIMESTAMP()), '" + str(status) + "')"
            print(sql_insert_query)
            result = cursor.execute(sql_insert_query)
            connection.commit()
            return "Apply successfully"

        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed getting record from actual_jobs table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/func/job/user/<int:job_id>/<int:user_id>', methods=['POST'])
def update_job_user(job_id, user_id):
    if request.method == 'POST':
        try:
            msg = ''
            req_data = request.get_json()

            connection = mysql.connector.connect(host='localhost',
                                                 database='work_it_db',
                                                 user='root',
                                                 password='ferfer19')

            cursor = connection.cursor()

            if req_data['job']['applying_time']:
                print("Updating applying_time")
                cursor.execute("UPDATE `job_user` SET `applying_time` = '" + str(req_data['job']['applying_time'])
                               + "' WHERE (`id_user` = " + str(user_id) + " and `id_job` = " + str(job_id) + ")")
            if req_data['job']['status']:
                print("Updating status")
                cursor.execute("UPDATE `job_user` SET `status` = '" + str(req_data['job']['status'])
                               + "' WHERE (`id_user` = " + str(user_id) + " and `id_job` = " + str(job_id) + ")")
            if req_data['user']['id_user']:
                print("Updating id_user")
                cursor.execute("UPDATE `job_user` SET `id_user` = '" + str(req_data['user']['id_user'])
                               + "' WHERE (`id_user` = " + str(user_id) + " and `id_job` = " + str(job_id) + ")")
                user_id = req_data['user']['id_user']
            if req_data['job']['id_job']:
                print("Updating id_job")
                cursor.execute("UPDATE `job_user` SET `id_job` = '" + str(req_data['job']['id_job'])
                               + "' WHERE (`id_user` = " + str(user_id) + " and `id_job` = " + str(job_id) + ")")
            connection.commit()
            return "Update successfully"
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed getting record from users table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/jobs/user/<int:user_id>', methods=['GET'])
def get_jobs_by_user(user_id):
    if request.method == 'GET':
        try:
            msg = ''

            connection = mysql.connector.connect(host='localhost',
                                                 database='work_it_db',
                                                 user='root',
                                                 password='ferfer19')

            cursor = connection.cursor()
            cursor.execute("SELECT * from `actual_jobs` WHERE (`creator` = " + str(user_id) + ")")

            jobs = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                jobs.append(row)
            return json.dumps(jobs)
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed getting record from users table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


@app.route('/jobs/filter', methods=['GET'])
def get_jobs_by_filter():
    if request.method == 'GET':
        try:
            msg = ''
            req_data = request.get_json()

            connection = mysql.connector.connect(host='localhost',
                                                 database='work_it_db',
                                                 user='root',
                                                 password='ferfer19')

            cursor = connection.cursor()
            tquery = "SELECT * from `actual_jobs` WHERE "
            count = 0

            if req_data['filter']['description']:
                count = count + 1
                if count > 1:
                    tquery += " and "
                tquery += "description = '" + req_data['filter']['description'] + "'"

            if req_data['filter']['title']:
                count = count + 1
                if count > 1:
                    tquery += " and "
                tquery += "title = '" + req_data['filter']['title'] + "'"

            if req_data['filter']['creator']:
                count = count + 1
                if count > 1:
                    tquery += " and "
                tquery += "creator =" + str(req_data['filter']['creator'])

            if req_data['filter']['category']:
                count = count + 1
                if count > 1:
                    tquery += " and "
                tquery += "category =" + str(req_data['filter']['category'])

            if req_data['filter']['creation_time']:
                count = count + 1
                if count > 1:
                    tquery += " and "
                tquery += "creation_time =" + str(req_data['filter']['creation_time'])

            if req_data['filter']['job_status']:
                count = count + 1
                if count > 1:
                    tquery += " and "
                tquery += "job_status =" + str(req_data['filter']['job_status'])

            print(tquery)
            cursor.execute(tquery)

            jobs = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                jobs.append(row)
            return json.dumps(jobs)
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            return "Failed getting record from users table {}".format(error)
        finally:
            # closing database connection.
            if connection.is_connected():
                cursor.close()
                connection.close()


if __name__ == '__main__':
    app.run(debug=True)
