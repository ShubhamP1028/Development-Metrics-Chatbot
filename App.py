from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error
from devmatric import extract_info, build_sql

bot = Flask(__name__)


def run_query(sql):
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="metrics_db"
        )
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return results, True
    except Error as e:
        return f"Error: {str(e)}", False


@bot.route("/", methods=["GET", "POST"])
def index():
    result = None
    query = ""
    sql = ""
    if request.method == "POST":
        query = request.form["query"]
        info = extract_info(query)
        sql = build_sql(info)
        result = run_query(sql)
    return render_template("index.html", result=result, query=query, sql=sql)


if __name__ == "__main__":
    bot.run(debug=True)
