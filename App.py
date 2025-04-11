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
            user="root",  # Default username
            password="",  # Empty password
            database="metrics_db"  # Database name from setup
        )
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return results, True  # Return results and success flag
    except Error as e:
        return f"Error: {str(e)}", False  # Return error message and failure flag


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
