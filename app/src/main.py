from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_dance.contrib.github import github
import markdown
import bleach
import utils
from functools import wraps

app = Flask(__name__)

github_blueprint = utils.get_oauth_data()
app.register_blueprint(github_blueprint, url_prefix = "/oauth")

def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "username" not in session:
            return redirect(url_for("login_index"))
        return f(*args,**kwargs)
    return decorated_function

@app.route("/login",methods=["GET","POST"])
def login_index():
    """
    Handles native login funcionality for the app

    - GET: Renders login.html template
    - POST: Provides authentication and session for the user, redirects to / if successful, shows a flash message if failed
    """
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

@app.route("/oauth")
def gh_login():
    """
    Handles Github OAUTH login funcionality for the app

    - GET: Renders Github login page
    - POST: Provides authentication and session for the user, redirects to / if successful, shows a flash message if failed
    """
    if not github.authorized:
        return redirect(url_for("github.login"))
    else:
        account_info = github.get("/user")
        if account_info.ok:
            account_data = account_info.json()
            username = account_data["login"]
            github_id = account_data["id"]

            user_id = utils.get_current_user_id_by_github_id(github_id)
            if not user_id:
                user_id = utils.add_github_user(username, github_id)

            session["username"] = username
            session["user_id"] = user_id
        return redirect(url_for("index"))

@app.route("/",methods=["GET"])
@login_required
def index():
    """
    Renders app home page after successful login

    - GET: Renders home page
    """
    return render_template("index.html")

@app.route("/taskList",methods=["GET","POST"])
@login_required
def list_index():
    """
    Handles requests made to /taskList endpoint

    - GET: Renders taskList.html template, displaying the user's created tasks
    - POST: Tries to create a Lorem task through the external WS, new task is displayed in list if successful, displays error flash message if failed  
    """
    if request.method == "GET":
        tasks = utils.get_tasks(session["user_id"])
        tasks_rows = "<tr>"
        for id,task in tasks.items():
            tasks_rows += ("<td><form action='" + url_for('edit_index') + "' method='GET'><input type='number' name='taskToEdit' value='" + str(id) + "' hidden><button>Editar</button></form></td>" \
                           + "<td><form action='" + url_for('complete_task_index') + "' method='GET'><input type='number' name='taskToComplete' value='" + str(id) + "' hidden><button>Completada</button></form></td>" \
                           + "<td><form action='" + url_for('cancel_task_index') + "' method='GET'><input type='number' name='taskToCancel' value='" + str(id) + "' hidden><button>Cancelar</button></form></td>" \
                           + "<td><form action='" + url_for('delete_task_index') + "' method='GET'><input type='number' name='taskToDelete' value='" + str(id) + "' hidden><button>Eliminar</button></form></td>"
                           + "<td>" +  bleach.clean(markdown.markdown(task["title"]), tags=utils.allowed_tags, attributes=utils.allowed_attrs) + "</td>" \
                           + "<td>" +  bleach.clean(markdown.markdown(task["description"]), tags=utils.allowed_tags, attributes=utils.allowed_attrs) + "</td>" \
                           + "<td>" + task["status"] + "</td>" \
                            + "<td>" +  str(task["timestamp"]) + "</td>" \
                            + "<td>" +  str(task["priority"]) + "</td>" \
                            + "</tr>"
                                )
        return render_template("taskList.html", rows = tasks_rows)
    
    if request.method == "POST":
        if not session["user_id"]:
            flash("Must be logged in to create lorem task","error")
            return redirect(url_for("list_index"))
        try:
            utils.lorem_task(session["user_id"])
            flash("Tarea creada exitosamente","success")
            return redirect(url_for("list_index"))
        except Exception as e:
            flash(str(e),"error")
            return redirect(url_for("list_index"))
    
@app.route("/newTask",methods=["GET","POST"])
@login_required
def new_index():
    """
    Handles requests made to /newTask endpoint

    - GET: Renders newTask.html template
    - POST: Tries to create a new task with the user's input, new task is created if successful, displays error flash message if failed  
    """
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
    """
    Handles requests made to /editTask endpoint

    - GET: Renders editTask.html template with the current data for the task with the ID specified in taskToEdit argument
    - POST: Tries to update task data with the user's input, task is updated if successful, displays error flash message if failed  
    """
    if request.method == "GET":
        try:
            task_info = utils.get_task_edit(request.args["taskToEdit"], session["username"])
            return render_template("editTask.html",task_info = task_info)
        except Exception as e:
            flash(str(e),"error")
            return redirect(url_for("list_index"))
    
    if request.method == "POST":
        if not utils.check_required_params(request.form):
            flash("No se proporciono al menos un dato requerido (titulo y fecha limite de tarea)","error")
            return redirect(url_for("edit_index",taskToEdit=request.form['taskID']))
            
        task_data = utils.get_form_inputs(request)

        try:
            utils.edit_task(task_data, session["username"])
            flash("Tarea editada correctamente","success")
            return redirect(url_for("edit_index",taskToEdit=request.form['taskID']))
        
        except Exception as e:
            flash(str(e),"error")
            return redirect(url_for("edit_index",taskToEdit=request.form['taskID']))
        
@app.route("/completeTask",methods=["GET"])
@login_required
def complete_task_index():
    """
    Handles requests made to /completeTask endpoint

    - GET: Tries to update task with ID specified in taskToComplete argument status column to 'Complete', displays error flash message if failed
    """
    try:
        utils.update_task_status(request.args["taskToComplete"],"Terminada", session["username"])
        flash("Tarea completada correctamente","success")
        return redirect(url_for("list_index"))
    except Exception as e:
        flash(str(e),"error")
        return redirect(url_for("list_index"))
    
@app.route("/cancelTask",methods=["GET"])
@login_required
def cancel_task_index():
    """
    Handles requests made to /cancelTask endpoint

    - GET: Tries to update task with ID specified in taskToCancel argument status column to 'Cancelled', displays error flash message if failed
    """
    try:
        utils.update_task_status(request.args["taskToCancel"],"Cancelada", session["username"])
        flash("Tarea cancelada correctamente","success")
        return redirect(url_for("list_index"))
    except Exception as e:
        flash(str(e),"error")
        return redirect(url_for("list_index"))
    
@app.route("/deleteTask",methods=["GET"])
@login_required
def delete_task_index():
    """
    Handles requests made to /deleteTask endpoint

    - GET: Tries to delete task with ID specified in taskToDelete argument, displays error flash message if failed
    """
    try:
        utils.delete_task(request.args["taskToDelete"], session["username"])
        flash("Tarea eliminada correctamente","success")
        return redirect(url_for("list_index"))
    except BaseException as e:
        flash(str(e),"error")
        return redirect(url_for("list_index"))
    

@app.route("/createUser",methods=["GET","POST"])
def create_user_index():
    """
    Handles requests made to /createUser endpoint

    - GET: Renders createUser.html template
    - POST: Tries to create new user with user's input, displays error flash message if failed
    """
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
        
@app.route("/logout", methods=["GET"])
def logout():
    """
    Handles requests made to /logout endpoint

    - GET: Clears user's session and renders login.html template
    """
    session.clear()
    return redirect(url_for("login_index"))
    
if __name__ == "__main__":
    app.secret_key = "tests"
    app.run()