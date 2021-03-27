from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# conexion con la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'materiadb'

mysql = MySQL(app)
# manejo de sesiones
app.secret_key = 'misecreto'

#Ruta principal
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materias')
    data=cur.fetchall()
    return render_template('index.html', materias = data)


#Crear Materia
@app.route('/crear_materia', methods=['POST'])
def crearMateria():
    if request.method == 'POST':
        materia = request.form['materia']
        sigla = request.form['sigla']
        descripcion = request.form['descripcion']

        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO materias (materia, sigla, descripcion) VALUES(%s,%s,%s)', (materia, sigla, descripcion))
        mysql.connection.commit()
        flash('Materia creado exitosamente')
        return redirect(url_for('index'))
        
    

#Editar Materia
@app.route('/editar/<id>')
def obtenerMateria(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM materias WHERE id = %s',[id])
    data = cur.fetchall()
    return render_template('edit_materia.html', materia = data[0])

#Modificar
@app.route('/actualizar/<id>',methods = ['POST'])
def actualizaMateria(id):
    if request.method == 'POST':
        materia = request.form['materia']
        sigla = request.form['sigla']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE materias
            SET materia = %s,
            sigla = %s,
            descripcion = %s
            WHERE id = %s
        """,(materia, sigla, descripcion, id))
        mysql.connection.commit()
    flash('Actualizado con exito')

    return redirect(url_for('index'))

#Editar Materia
@app.route('/eliminar/<string:id>')
def eliminarMateria(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM materias WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact removed successfully')
    return redirect(url_for('index'))

# Corriendo en el puerto 3001
if __name__ == '__main__':
    app.run(port=3001, debug=True)
                                    