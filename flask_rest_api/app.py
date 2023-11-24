from flask import Flask, render_template, jsonify, abort, request, redirect, url_for, session
from dotenv import load_dotenv
from flask_mysqldb import MySQL
import os

app = Flask(__name__)


load_dotenv()

app.secret_key = os.getenv('TOKEN')

app.config['MYSQL_DB'] = os.getenv('DB_NAME')
app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')

mysql = MySQL(app)

#api/blog rotes
@app.route('/api/blog/', methods=['GET'])
def get_all_blog_posts():
    if "user" not in session:
        return redirect(url_for("login"))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM blog_posts")
    blog_posts = cursor.fetchall()
    cursor.close()
    return jsonify(blog_posts)

@app.route('/api/blog/<int:id>', methods=['GET'])
def get_blog_post(id):
    if "user" not in session:
        return redirect(url_for("login"))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM blog_posts WHERE post_id = %s", (id,))
    blog_post = cursor.fetchone()
    if blog_post:
        return jsonify(blog_post)
    else:
        return abort(404)
    
@app.route('/api/blog/<int:id>', methods=['DELETE'])
def delete_blog_post(id):
    if "user" not in session:
        return redirect(url_for("login"))
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM blog_posts WHERE id = %s", (id,))
    blog_post = cursor.fetchone()
    if blog_post:
        return jsonify(blog_post)
    else:
        return abort(404)
    
@app.route('/api/blog/<int:id>', methods=['PATCH'])
def update_blog_post(id):
    if "user" not in session:
        return redirect(url_for("login"))

    data = request.get_json()
    new_title = data.get('title')
    new_content = data.get('content')

    if not new_title and not new_content:
        return abort(404)

    cursor = mysql.connection.cursor()
    update_query = "UPDATE blog_posts SET title = %s, content = %s WHERE id = %s"
    cursor.execute(update_query, (new_title, new_content, id))
    mysql.connection.commit()

    cursor.execute("SELECT * FROM blog_posts WHERE id = %s", (id,))
    updated_blog_post = cursor.fetchone()

    if updated_blog_post:
        return jsonify(updated_blog_post)
    else:
        return abort(404)



#html routes
@app.route("/", methods=["POST", "GET"])
def index():
    if "user" in session:
        user = session["user"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM blog_posts INNER JOIN users on blog_posts.author_id = users.user_id")
        blog_posts = cursor.fetchall()
        cursor.close()
        if request.method == "POST":
            title = request.form["title"]
            content = request.form["content"]
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO blog_posts (title, content, author_id) VALUES(%s, %s, %s)", (title, content, user[0]))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("index"))
        return render_template("index.html", blog_posts=blog_posts)
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        if user and check_password(password, user[3]) and check_username(username, user[1]):
            session["user"] = user
            if check_password("admin", user[3]) and check_username("admin", user[1]):
                return redirect(url_for("admin"))
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))

    else:
        return render_template("login.html")

def check_password(user_pass, db_pass):
    return user_pass == db_pass
def check_username(user_name, db_name):
    return user_name == db_name

@app.route("/admin", methods=["POST", "GET"])
def admin():
    if "user" in session:
        user = session["user"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM blog_posts INNER JOIN users on blog_posts.author_id = users.user_id")
        blog_posts = cursor.fetchall()
        cursor.close()
        if request.method == "POST":
            if "id_del" in request.form: 
                id_del = request.form["id_del"]

                cursor = mysql.connection.cursor()
                cursor.execute("DELETE FROM blog_posts WHERE post_id = %s", (id_del))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for("admin"))
            if "id_upt" in request.form:
                id_upt = request.form["id_upt"]
                title = request.form["title"]
                content = request.form["content"]

                cursor = mysql.connection.cursor()
                cursor.execute("UPDATE blog_posts SET title = %s, content = %s WHERE post_id = %s", (title, content, id_upt))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for("admin"))
        return  render_template("admin.html", blog_posts = blog_posts)
    else:
        return redirect(url_for("login"))

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["pass"]
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, email, pass) VALUES(%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("login"))
    else:    
        return render_template("register.html")
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



if __name__ == '__main__':
    app.run(debug=True)