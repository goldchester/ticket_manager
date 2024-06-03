import psycopg2
import psycopg2.extras
from flask import Flask, request, render_template, g, current_app, make_response, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    conn = get_db()
    cursor = conn.cursor()
    with current_app.open_resource("queries/loginfetch.sql") as file:
        alltext = file.read()
        cursor.execute(alltext)
    data = cursor.fetchall()
    department = request.cookies.get('department')
    name = request.cookies.get('name')
    departments = set(row[0] for row in data)
    if department and name:
        return render_template("homepage.html", department=department, name=name)
    if "step" not in request.form:
        return render_template("login.html", departments=departments, step="compose_entry", action="get_dep")
    elif request.form["action"] == "get_dep":
        selected_department = request.form.get('department')
        names = [row[1] for row in data if row[0] == selected_department]
        return render_template("login.html", departments=departments, names=names, step="compose_entry", action="get_name", selected_department=selected_department)
    elif request.form["step"] == "success" and request.form['department'] and request.form['name']:
        inputdp = request.form['department']
        inputname = request.form['name']
        inputid = [row[2] for row in data if row[1] == inputname]
        inputid = str(inputid[0])
        resp = make_response(render_template("homepage.html", department=inputdp, name=inputname))
        resp.set_cookie('department', inputdp)
        resp.set_cookie('name', inputname)
        resp.set_cookie('id', inputid)
        return resp
    else:
        selected_department = request.form.get('department')
        names = [row[1] for row in data if row[0] == selected_department]
        return render_template("login.html", departments=departments, names=names, step="compose_entry", action="get_name", selected_department=selected_department)

@app.route("/create", methods=['GET', 'POST'])
def create():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM priority')
            priority = cursor.fetchall()
            cursor.execute('SELECT * FROM departments')
            departments = cursor.fetchall()
    if "step" not in request.form:     
        return render_template("create.html", step="compose_entry", priority=priority, departments=departments)
    elif request.form["step"] == "add_entry":
        title = request.form.get('title')
        problem = request.form.get('problem')
        if not title or not problem:
            return render_template("create.html", step="empty", priority=priority, departments=departments)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("insert into tickets (title, created_by_id, assigned_to_dep, problem, priority_id, status_id) values (%s, %s, %s, %s, %s, 1)",
                   [request.form['title'], request.cookies.get('id'), request.form['department'], request.form['problem'], request.form['priority']])
        conn.commit()
        return render_template("create.html", step="add_entry")

@app.route("/assign", methods=['GET', 'POST'])
def assign():
    if "step" not in request.form:
        conn = get_db()
        cursor = conn.cursor()
        with current_app.open_resource("queries/getdep.sql") as file:
            alltext = file.read()
            cursor.execute(alltext, [request.cookies.get('id')])
        depid = str(cursor.fetchone()[0])
        with current_app.open_resource("queries/assignfetch.sql") as file:
            alltext = file.read()
            cursor.execute(alltext, [depid])
        tickets = cursor.fetchall()
        return render_template('assign.html', step="display_entries", action="assign_tickets", tickets=tickets)
    elif request.form["step"] == "assign_tickets":
        selected_tickets = request.form.getlist('postid')
        conn = get_db()
        cursor = conn.cursor()
        for ticket_id in selected_tickets :
            cursor.execute('UPDATE tickets SET assigned_to = %s, status_id = 2 WHERE id = %s', 
                           [request.cookies.get('id'), ticket_id])
        conn.commit()
        return render_template('assign.html', step="success")

@app.route("/edit", methods=['GET', 'POST'])
def edit():
    conn = get_db()
    cursor = conn.cursor()
    with current_app.open_resource("queries/editfetch.sql") as file:
        alltext = file.read()
        cursor.execute(alltext, [request.cookies.get('id')])
    tickets = cursor.fetchall()
    if "step" not in request.form:
        return render_template('edit.html', step="display_entries", action="edit_ticket", tickets=tickets)
    elif request.form["step"] == "edit_ticket":
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM priority')
                priority = cursor.fetchall()
                cursor.execute('SELECT * FROM departments')
                departments = cursor.fetchall()
        selected_ticket = request.form.getlist('postid')
        selected_ticket_data = next((row for row in tickets if row[0] == int(selected_ticket[0])), None)
        return render_template('edit.html', step="edit_ticket", priority=priority, departments=departments, ticket=selected_ticket_data)
    elif request.form["step"] == "update_database":
        cursor.execute('UPDATE tickets SET problem = %s, title = %s, assigned_to_dep = %s, priority_id = %s WHERE id = %s', 
                       [request.form['problem'], request.form['title'], request.form['department'], request.form['priority'], request.form['postid']])
        conn.commit()
        return render_template('edit.html', step="success")

@app.route("/editsolution", methods=['GET', 'POST'])
def editsolution():
    conn = get_db()
    cursor = conn.cursor()
    with current_app.open_resource("queries/editsolutionfetch.sql") as file:
        alltext = file.read()
        cursor.execute(alltext, [request.cookies.get('id')])
    tickets = cursor.fetchall()
    if "step" not in request.form:
        return render_template('edit.html', step="display_entries", action="edit_solution", tickets=tickets)
    elif request.form["substep"] == "edit_ticket_solution":
        selected_ticket = request.form.getlist('postid')
        selected_ticket_data = next((row for row in tickets if row[0] == int(selected_ticket[0])), None)
        return render_template('edit.html', substep="edit_ticket_solution", ticket=selected_ticket_data)
    elif request.form["step"] == "update_database":
        cursor.execute('UPDATE tickets SET solutions = %s WHERE id = %s', 
                       [request.form['solutions'], request.form['postid']])
        conn.commit()
        return render_template('edit.html', step="success")

@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if "step" not in request.form:
        conn = get_db()
        cursor = conn.cursor()
        with current_app.open_resource("queries/deletefetch.sql") as file:
            alltext = file.read()
            cursor.execute(alltext, [request.cookies.get('id')])
        tickets = cursor.fetchall()
        return render_template('assign.html', step="display_entries", action="delete_tickets", tickets=tickets)
    elif request.form["substep"] == "delete_tickets":
        selected_tickets = request.form.getlist('postid')
        conn = get_db()
        cursor = conn.cursor()
        for ticket_id in selected_tickets :
            cursor.execute('DELETE FROM tickets WHERE id = %s', 
                           [ticket_id])
        conn.commit()
        return render_template('assign.html', step="success", substep="delete_tickets")

@app.route("/solve", methods=['GET', 'POST'])
def solve():
    if "step" not in request.form:
        conn = get_db()
        cursor = conn.cursor()
        with current_app.open_resource("queries/solvefetch.sql") as file:
            alltext = file.read()
            cursor.execute(alltext, [request.cookies.get('id')])
        tickets = cursor.fetchall()
        return render_template('assign.html', step="display_entries", action="solve_tickets", tickets=tickets)
    elif request.form["substep"] == "solve_tickets":
        selected_tickets = request.form.getlist('postid')
        conn = get_db()
        cursor = conn.cursor()
        for ticket_id in selected_tickets :
            cursor.execute('UPDATE tickets SET status_id = 3, solved_at = now() WHERE id = %s', 
                           [ticket_id])
        conn.commit()
        return render_template('assign.html', step="success", substep="solve_tickets")

@app.route("/browse", methods=['GET', 'POST'])
def browse():
    return render_template('browse.html')

@app.route("/browse_created", methods=['GET', 'POST'])
def browse_created():
    conn = get_db()
    cursor = conn.cursor()
    with current_app.open_resource("queries/browse_created.sql") as file:
        alltext = file.read()
        cursor.execute(alltext, [request.cookies.get('id')])
    tickets = cursor.fetchall()
    return render_template('browsetickets.html', tickets=tickets)

@app.route("/browse_assigned", methods=['GET', 'POST'])
def browse_assigned():
    conn = get_db()
    cursor = conn.cursor()
    with current_app.open_resource("queries/browse_assigned.sql") as file:
        alltext = file.read()
        cursor.execute(alltext, [request.cookies.get('id')])
    tickets = cursor.fetchall()
    return render_template('browsetickets.html', tickets=tickets)

@app.route("/browse_department", methods=['GET', 'POST'])
def browse_department():
    conn = get_db()
    cursor = conn.cursor()
    with current_app.open_resource("queries/getdep.sql") as file:
        alltext = file.read()
        cursor.execute(alltext, [request.cookies.get('id')])
    depid = str(cursor.fetchone()[0]) 
    with current_app.open_resource("queries/browse_department.sql") as file:
        alltext = file.read()
        cursor.execute(alltext, [depid])
    tickets = cursor.fetchall()
    return render_template('browsetickets.html', tickets=tickets)

@app.route("/browse_solved", methods=['GET', 'POST'])
def browse_solved():
    conn = get_db()
    cursor = conn.cursor()
    with current_app.open_resource("queries/browse_solved.sql") as file:
        alltext = file.read()
        cursor.execute(alltext, [request.cookies.get('id')])
    tickets = cursor.fetchall()
    return render_template('browsetickets.html', tickets=tickets)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('department')
    resp.delete_cookie('name')
    resp.delete_cookie('id')
    return resp

def connect_db():
    conn = psycopg2.connect(host="localhost", user="redacted", password="redacted", dbname="myproject", 
    cursor_factory=psycopg2.extras.DictCursor)
    return conn
    
def get_db():
    if "db" not in g:
        g.db = connect_db()

    return g.db
    
@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()
        debug("Closing DB")

def debug(s):
    if app.config['DEBUG']:
        print(s)

@app.cli.command("init")
def init_db():
    conn = get_db()
    cur = conn.cursor()
    with current_app.open_resource("schemas/init.sql") as file:
        alltext = file.read()
        cur.execute(alltext)
    conn.commit()
    print("Initialized the database.")

@app.cli.command("populate")
def init_db():
    conn = get_db()
    cur = conn.cursor()
    with current_app.open_resource("schemas/populate.sql") as file:
        alltext = file.read()
        cur.execute(alltext)
    conn.commit()
    print("Populated the tables.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)