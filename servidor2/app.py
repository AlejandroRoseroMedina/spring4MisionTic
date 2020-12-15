# importamos la libreria de flask para python
# Flask: tiene todas las funciones del microframework
# render_template :  permite renderizar los HTML en el servidor
from  flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy 
import sqlite3
import os
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/cafeteria.db"
# crear e instanciar una variable que me representa la app web en python
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")  
def index():  
    return render_template("login.html");

@app.route('/registroproducto')
def registroProducto():
    return render_template('registroproducto.html')    

@app.route('/principal')
def principal():
    return render_template('principal.html')   

@app.route('/reporteventasdia')
def reporteVentas():
    return render_template('reporteventasdia.html') 

@app.route('/registrocajero')
def registrocajero():
     return render_template('registrocajero.html')

@app.route("/savedetailslogin",methods = ["POST","GET"])  
def saveDetails():  
        msg = "msg"  
        if request.method == "POST":  
            try:  
                name = request.form["nombre"]  
                email = request.form["correo"]  
                clave = request.form["clave"]  
                with sqlite3.connect("cafeteria.db") as con:  
                    cur = con.cursor()  
                    cur.execute("INSERT into usuario (nom_usu, email_usu, clave_usu, tipo_usu) values (?,?,?,?)",(name,email,clave,2))  
                    con.commit()  
                    msg = "Cajero creado exitosamente"  
            except:  
                con.rollback() 
                msg = "No se pudo adicionar el cajero a la lista"  
                
            finally:  
                return render_template("registrocajero.html",msg = msg)  
                con.close()  
                
   
@app.route('/listacajeros')
def listacajeros():
    con = sqlite3.connect("cafeteria.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from usuario")  
    rows = cur.fetchall()
    return render_template('listacajeros.html',rows = rows)

@app.route('/eliminarcajero', methods = ["POST"]) 
def eliminarcajero():
    id = request.form["id"]  
    with sqlite3.connect("cafeteria.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from usuario where cod_usu = ?",(id,)) 
            msg = "record successfully deleted" 
      
        except:  
            msg = "can't be deleted"  
        finally:   
           #return render_template("eliminarcajero.html", msg = msg)  
           
           con = sqlite3.connect("cafeteria.db")  
           con.row_factory = sqlite3.Row  
           cur = con.cursor()  
           cur.execute("select * from usuario")  
           rows = cur.fetchall()
           return redirect(url_for('rutaeliminar'))  
           #return render_template("eliminarcajero.html", rows = rows, msg = msg)    
           
@app.route('/rutaeliminar')
def rutaeliminar():  
    con = sqlite3.connect("cafeteria.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from usuario")  
    rows = cur.fetchall()
    return render_template("eliminarcajero.html",rows = rows)  

@app.route('/visualizacionproductos')
def visualizacionproductos():
    return render_template('visualizacionproductos.html')





#declarar y crear las rutas de acceso al servidor
#@app.route("/")
#def home():
 #   return "<h1>Mi primera app en Flask!! de misionTics solo // </h1>"-->


#Logica algoritmica
@app.route('/usuariocajero',methods=['POST'])
def usuariocajero():
    nombre=request.form.get("nombre")
    return render_template("visualizacionproductos.html",nombre=nombre)


# main o disparador de la aplicacion en el servidor de python
if __name__=="__main__":
    #lanzar el servidor
    db.create_all()
    app.run(port=5000,debug=True)