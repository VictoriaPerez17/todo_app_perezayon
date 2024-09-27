from flask import Flask, render_template, request, url_for, redirect, session, flash
import utils
from functools import wraps

app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "username" not in session:
            return redirect(url_for("login_index"))
        return f(*args,**kwargs)
    return decorated_function

@app.route("/",methods=["GET"])
@login_required
def index():
    return render_template("index.html")

@app.route("/taskList",methods=["GET","POST"])
@login_required
def list_index():
    if request.method == "GET":
        tasks = utils.get_tasks(session["user_id"])
        tasks_rows = "<tr>"
        for id,task in tasks.items():
            tasks_rows += ("<td><form action='" + url_for('edit_index') + "' method='GET'><input type='number' name='taskToEdit' value='" + str(id) + "' hidden><button>Editar</button></form></td>" \
                           + "<td><form action='" + url_for('complete_task_index') + "' method='GET'><input type='number' name='taskToComplete' value='" + str(id) + "' hidden><button>Completada</button></form></td>" \
                           + "<td><form action='" + url_for('cancel_task_index') + "' method='GET'><input type='number' name='taskToCancel' value='" + str(id) + "' hidden><button>Cancelar</button></form></td>" \
                           + "<td><form action='" + url_for('delete_task_index') + "' method='GET'><input type='number' name='taskToDelete' value='" + str(id) + "' hidden><button>Eliminar</button></form></td>"
                           + "<td>" + task["title"] + "</td>" \
                           + "<td>" + task["description"] + "</td>" \
                           + "<td>" + task["status"] + "</td>" \
                            + "<td>" +  str(task["timestamp"]) + "</td>" \
                            + "<td>" +  str(task["priority"]) + "</td>" \
                            + "</tr>"
                                )
        return render_template("taskList.html", rows = tasks_rows)
    
@app.route("/newTask",methods=["GET","POST"])
@login_required
def new_index():
    if request.method == "GET":
        return render_template("newTask.html")
    
    if request.method == "POST":
        if not utils.check_required_params(request.form):
            flash("No se proporciono al menos un dato requerido (titulo y fecha limite de tarea)","error")
            return redirect(url_for("new_index"))
            
        task_data = utils.get_form_inputs(request)

        try:
            utils.create_task(task_data,session["user_id"])
            flash("Tarea creada exitosamente","success")
            return redirect(url_for("new_index"))
        except Exception as e:
            flash(str(e),"error")
            return redirect(url_for("new_index"))
        
    
@app.route("/editTask",methods=["GET","POST"])
@login_required
def edit_index():
    if request.method == "GET":
        task_info = utils.get_task_edit(request.args["taskToEdit"])
        return render_template("editTask.html",task_info = task_info)
    
    if request.method == "POST":
        if not utils.check_required_params(request.form):
            flash("No se proporciono al menos un dato requerido (titulo y fecha limite de tarea)","error")
            return redirect(url_for("edit_index",taskToEdit=request.form['taskID']))
            
        task_data = utils.get_form_inputs(request)

        try:
            utils.edit_task(task_data)
            flash("Tarea editada correctamente","success")
            return redirect(url_for("edit_index",taskToEdit=request.form['taskID']))
        
        except Exception as e:
            flash(str(e),"error")
            return redirect(url_for("edit_index",taskToEdit=request.form['taskID']))
        
@app.route("/completeTask",methods=["GET"])
@login_required
def complete_task_index():
    try:
        utils.update_task_status(request.args["taskToComplete"],"Terminada")
        flash("Tarea completada correctamente","success")
        return redirect(url_for("list_index"))
    except Exception as e:
        flash(str(e),"error")
        return redirect(url_for("list_index"))
    
@app.route("/cancelTask",methods=["GET"])
@login_required
def cancel_task_index():
    try:
        utils.update_task_status(request.args["taskToCancel"],"Cancelada")
        flash("Tarea cancelada correctamente","success")
        return redirect(url_for("list_index"))
    except Exception as e:
        flash(str(e),"error")
        return redirect(url_for("list_index"))
    
@app.route("/deleteTask",methods=["GET"])
@login_required
def delete_task_index():
    try:
        utils.delete_task(request.args["taskToDelete"])
        flash("Tarea eliminada correctamente","success")
        return redirect(url_for("list_index"))
    except Exception as e:
        flash(str(e),"error")
        return redirect(url_for("list_index"))

@app.route("/login",methods=["GET","POST"])
def login_index():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            if utils.authentication(username,password):
                session["username"] = username
                session["user_id"] = utils.get_current_user_id(session["username"])
                return redirect(url_for("index"))
            flash("Error al iniciar sesion, usuario o contraseña invalidos","error")
            return redirect(url_for("login_index"))
        except Exception as e:
            flash("Ocurrio un error al inciar sesion, intentar de nuevo","error")
            return redirect(url_for("login_index"))
    

@app.route("/createUser",methods=["GET","POST"])
def create_user_index():
    if request.method == "GET":
        return render_template("createUser.html")
    
    if request.method == "POST":
        try:
            utils.create_user(request.form)
            flash("Usuario creado exitosamente, ahora puede iniciar sesion con el usuario y contraseña proporcionados","success")
            return redirect(url_for("login_index"))
        except Exception as e:
            flash(str(e),"error")
            return redirect(url_for("login_index"))
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_index"))
    
if __name__ == "__main__":
    app.secret_key = "tests"
    app.run()