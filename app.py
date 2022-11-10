from flask import Flask, request, Response
import sqlite3, json

app = Flask(__name__)

db_locale="class.db"       

@app.route("/view",methods=['GET'])
def view_rec():
    if request.method=='GET':
        con=sqlite3.connect(db_locale)
        rno=request.headers["reg_no"]
        print(rno)
        c=con.cursor()
        sql_exec_str="SELECT * FROM student WHERE reg_no = ?"
        student_info=c.execute(sql_exec_str,[rno]).fetchall()
        con.commit()
        con.close()
        resp={}
        resp["reg_no"]=student_info[0][0]
        resp["name"]=student_info[0][1]
        resp["marks"]=student_info[0][2]
        fin_resp={}
        fin_resp["result"]=resp
        return json.dumps(fin_resp)
@app.route("/view_all",methods=['GET'])
def view_all_rec():
    if request.method=="GET":
        con=sqlite3.connect(db_locale)
        c=con.cursor()
        c.execute("""
            SELECT * FROM student
        """)
        students=c.fetchall()
        con.commit()
        con.close()
        res=[]
        final_res={}
        for student in students:
            resp={}
            resp["reg_no"]=student[0]
            resp["name"]=student[1]
            resp["marks"]=student[2]
            res.append(resp)
        final_res['result']=res
        return json.dumps(final_res)

@app.route("/add",methods=['POST'])
def add_rec():
    if request.method=='POST':
        con=sqlite3.connect(db_locale)
        c=con.cursor()
        c.execute("""
            INSERT INTO student(reg_no,name,marks)
            VALUES(?,?,?)
        """,(request.headers["reg_no"],request.headers["name"],request.headers["marks"])
        )
        con.commit()
        con.close()
        resp={}
        return Response(status=200)

@app.route("/delete",methods=['DELETE'])
def delete_rec():
    if request.method=='DELETE':
        con=sqlite3.connect(db_locale)
        c=con.cursor()
        c.execute("""
            DELETE FROM student
            WHERE reg_no = ?
        """,(request.headers["reg_no"])
        )
        con.commit()
        con.close()
        return Response(status=200)
@app.route("/update",methods=['PATCH'])
def update():
    if request.method=='PATCH':
        con=sqlite3.connect(db_locale)
        c=con.cursor()
        sql_exec_str="UPDATE student SET name = ?, marks=? WHERE reg_no =?"
        c.execute(sql_exec_str,(request.headers['name'],request.headers['marks'],request.headers['reg_no']))
        con.commit()
        con.close()
        return Response(status=200)
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)