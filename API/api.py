import json
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
        
        
@app.route("/movies", methods=["GET", "POST"])
def movies():
    conn = sqlite3.connect("Movies.db")
    cursor = conn.cursor()
    
    if request.method == "GET":
        cursor.execute("SELECT * FROM Movies")
        movie_list = [
            dict(id=row[0], title=row[1], year=row[2], score=row[3])
            for row in cursor.fetchall()
            ]
        if movie_list is not None:
            return jsonify(movie_list)
    
    if request.method == "POST":
        new_title = request.form["title"]
        new_year = request.form["year"]
        new_score = request.form["score"]
        sql = """INSERT INTO Movies (title, year, score) VALUES (?, ?, ?)"""
        
        cursor = cursor.execute(sql, (new_title, new_year, new_score))
        conn.commit()
        conn.close()
        return f"The movie with id:{cursor.lastrowid} has been added successfully"
    
    
@app.route("/movie/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_movie(id):
    conn = sqlite3.connect("Movies.db")
    cursor = conn.cursor()
    movie = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM Movies WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            movie = r
        if movie is not None:
            return jsonify(movie), 200
        else:
            return "Something wrong", 404
            
    if request.method == "PUT":
        sql = """UPDATE Movies
            SET title=?, 
                year=?,
                score=?
            WHERE id=?"""
        title = request.form['title']
        year = request.form['year']
        score = request.form['score']
        updated_movie = {
            "id": id,
            "title": title,
            "year": year,
            "score": score,}
        cursor.execute(sql, (title, year, score, id))
        conn.commit()
        conn.close()
        return jsonify(updated_movie)
        
    if request.method == "DELETE":
        sql = """DELETE FROM Movies WHERE id=?"""
        cursor.execute(sql, (id,))
        conn.commit()
        conn.close()
        return f"The movie with id{id} has been deleted.", 200
        
if __name__ == "__main__":
    app.run()