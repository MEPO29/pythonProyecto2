from tkcalendar import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from types import NoneType
import psycopg2
from psycopg2 import extensions
from datetime import datetime, timedelta, date

root = Tk()
root.title('App SmartWatch')
host1 = "localhost"
database1 = "Py3"
user1 = "postgres"
password1 = "Belmar.2017"
port1 = "5432"
user2 = "usuariou1"
password2 = "adminu1"
user3 = "usuariose1"
password3 = "adminse1"
user4 = "superuser1"
password4 = "superadmin1"

def crearTablas():

    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS usuario
    (ID_usuario VARCHAR PRIMARY KEY,
    nombre VARCHAR,
    apellido VARCHAR,
    edad INT,
    altura DOUBLE PRECISION,
    calorias_diarias INT,
    peso_actual INT,
    password VARCHAR);

    CREATE TABLE IF NOT EXISTS progreso
    (fk_ID_usuario VARCHAR REFERENCES usuario(ID_usuario),
    semana INT,
    peso_semanal INT,
    diferencia_sem INT,
    fecha_semana DATE);

    CREATE TABLE IF NOT EXISTS suscripcion
    (fk_ID_usuario VARCHAR REFERENCES usuario(ID_usuario),
    tipo VARCHAR,
    num_tarjeta BIGINT,
    cv_tarjeta INT,
    vence_tarjeta VARCHAR,
    fecha_registro DATE,
    fecha_expiracion DATE);

    CREATE TABLE IF NOT EXISTS instructor
    (nombre_instructor VARCHAR PRIMARY KEY,
    apellido_instructor VARCHAR);

    CREATE TABLE IF NOT EXISTS sesion
    (id_sesion VARCHAR PRIMARY KEY,
    categoria VARCHAR,
    fk_nombre_instructor VARCHAR REFERENCES instructor(nombre_instructor),
    fecha_hora_inicio TIMESTAMP,
    fecha_hora_fin TIMESTAMP);

    CREATE TABLE IF NOT EXISTS registro_sesion
    (fk_id_sesion VARCHAR REFERENCES sesion(id_sesion),
    fk_ID_usuario VARCHAR REFERENCES usuario(ID_usuario));

    CREATE TABLE IF NOT EXISTS admin
    (user_admin VARCHAR PRIMARY KEY,
    pass_admin VARCHAR);

    CREATE TABLE IF NOT EXISTS adminu
    (user_admin VARCHAR PRIMARY KEY,
    pass_admin VARCHAR);

    CREATE TABLE IF NOT EXISTS admins
    (user_admin VARCHAR PRIMARY KEY,
    pass_admin VARCHAR);

    CREATE TABLE IF NOT EXISTS superadm
    (user_admin VARCHAR PRIMARY KEY,
    pass_admin VARCHAR);

    create table if not exists log_admin
    (usuario varchar,
    accion varchar,
    fecha date,
    tiempo time);
    ''')

    conn.commit()
    conn.close()

def insertAdm():
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''
    INSERT INTO adminu VALUES('usuarioU1', 'adminu1');
    INSERT INTO admins VALUES('usuarioSe1', 'adminse1');
    INSERT INTO superadm VALUES('superuser1', 'superadmin1');
    ''')

    conn.commit()
    conn.close()

def CreacionGrupos():
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''
    CREATE GROUP admin_usuarios;
    CREATE GROUP admin_sesiones;
    CREATE GROUP super_admin;

    ''')

    conn.commit()
    conn.close()

def crearPrivilegios():
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''

    --GRANT ALL PRIVILEGES ON table adminu, usuario, progreso, suscripcion TO admin_usuarios WITH GRANT OPTION; 
    --GRANT INSERT ON log_admin to admin_usuarios;
    --GRANT ALL PRIVILEGES ON table  admins, sesion, registro_sesion, instructor TO admin_sesiones WITH GRANT OPTION; 
    --GRANT INSERT ON log_admin to admin_sesiones;
    --GRANT ALL PRIVILEGES ON table usuario, sesion ,suscripcion , registro_sesion , adminu, admins, superadm  , instructor, log_admin , progreso  TO super_admin with GRANT OPTION;
    --GRANT create on schema public to super_admin;
    --Alter table if exists consulta1 owner to super_admin;
    --Alter table if exists consulta2 owner to super_admin;
    --Alter table if exists consulta3 owner to super_admin;
    ''')

    conn.commit()
    conn.close()

def CreacionRoles():
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''

    CREATE ROLE usuarioU1 WITH
	    LOGIN
	    NOSUPERUSER
	    NOCREATEDB
	    NOCREATEROLE
	    INHERIT
	    NOREPLICATION
	    CONNECTION LIMIT -1
	    PASSWORD 'adminu1';

    GRANT admin_usuarios TO usuarioU1;

    CREATE ROLE usuarioSe1 WITH
	    LOGIN
	    NOSUPERUSER
	    NOCREATEDB
	    NOCREATEROLE
	    INHERIT
	    NOREPLICATION
	    CONNECTION LIMIT -1
	    PASSWORD 'adminse1';

    GRANT admin_sesiones TO usuarioSe1;


    CREATE ROLE superuser1 WITH
	    LOGIN
	    SUPERUSER
	    CREATEDB
	    CREATEROLE
	    INHERIT
	    REPLICATION
	    CONNECTION LIMIT -1
	    PASSWORD 'superadmin1';

    GRANT super_admin TO superuser1;


    ''')

    conn.commit()
    conn.close()

    
def crearVista():
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''
    --Create  view consulta1 as
    --SELECT  extract (day from fecha_hora_inicio) as dia, count(id_sesion) as conteo FROM sesion 
	--WHERE extract(hour from fecha_hora_inicio) between 15 and 20 
    --GROUP BY dia 
    --ORDER BY conteo desc
    --LIMIT 5 ;

    --Create view consulta2 as
    --SELECT  fk_nombre_instructor, count(fk_nombre_instructor)as cuenta 
    --FROM sesion
    --where extract ( month from fecha_hora_inicio) = 10
    --GROUP BY fk_nombre_instructor
    --ORDER BY cuenta desc
    --LIMIT 10 ;

    Create view consulta3 as
    select usuario, count(usuario) as cantidad_usuario  
    from log_admin 
    group by usuario




    ''')

    conn.commit()
    conn.close()


def funcionReg():
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''INSERT INTO usuario
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', 
    (us_id.get(),
    us_nombre.get(), 
    us_apellido.get(), 
    int(us_edad.get()), 
    float(us_altura.get()), 
    int(us_cal.get()), 
    int(us_peso.get()), 
    us_pass.get())
    )

    c.execute('''INSERT INTO progreso
    VALUES (%s, %s, %s, %s, %s)''',
    (us_id.get(),
    1,
    int(us_peso.get()),
    0,
    datetime.today().date())
    )

    conn.commit()
    conn.close()

    notifReg.config(text="Registrado con éxito", fg='green')

def displayUsuarios():
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

def trigger_instructor():

    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''
    drop function if exists bitacora();
    create or replace function bitacora1()
    returns trigger as $$
    declare 
	    usuario varchar(20) := user;
	    fecha date := current_date;
	    tiempo time := current_time;
    begin
	    insert into log_admin values (usuario, 'modificar instructores', fecha, tiempo);
	    return new;
    end;
    $$
    language plpgsql;

    create or replace trigger mod_instructores
    before update
    on instructor
    for each row execute procedure bitacora1();

    create or replace function bitacora2()
    returns trigger as $$
    declare 
	    usuario varchar(20) := user;
	    fecha date := current_date;
	    tiempo time := current_time;
    begin
	    insert into log_admin values (usuario, 'eliminar instructores', fecha, tiempo);
	    return new;
    end;
    $$
    language plpgsql;

    create or replace trigger del_instructores
    before delete
    on instructor
    for each row execute procedure bitacora2();

    create or replace function bitacora3()
    returns trigger as $$
    declare 
	    usuario varchar(20) := user;
	    fecha date := current_date;
	    tiempo time := current_time;
    begin
	    insert into log_admin values (usuario, 'crear instructores', fecha, tiempo);
	    return new;
    end;
    $$
    language plpgsql;

    create or replace trigger ins_instructores
    after insert
    on instructor
    for each row execute procedure bitacora3();
    ''')

    conn.commit()
    conn.close()

def trigger_usuario():
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''
    create or replace function bitacora4()
    returns trigger as $$
    declare 
	    usuario varchar(20) := user;
	    fecha date := current_date;
	    tiempo time := current_time;
    begin
	    insert into log_admin values (usuario, 'modificar usuario', fecha, tiempo);
	    return new;
    end;
    $$
    language plpgsql;

    create or replace trigger mod_usuario
    before update
    on usuario
    for each row execute procedure bitacora4();

    create or replace function bitacora5()
    returns trigger as $$
    declare 
	    usuario varchar(20) := user;
	    fecha date := current_date;
	    tiempo time := current_time;
    begin
	    insert into log_admin values (usuario, 'eliminar usuario', fecha, tiempo);
	    return new;
    end;
    $$
    language plpgsql;

    create or replace trigger del_usuario
    before delete
    on usuario
    for each row execute procedure bitacora5();

    create or replace function bitacora6()
    returns trigger as $$
    declare 
	    usuario varchar(20) := user;
	    fecha date := current_date;
	    tiempo time := current_time;
    begin
	    insert into log_admin values (usuario, 'crear usuario', fecha, tiempo);
	    return new;
    end;
    $$
    language plpgsql;

    create or replace trigger ins_usuario
    after insert
    on usuario
    for each row execute procedure bitacora6();
    ''')

    conn.commit()
    conn.close()

def trigger_sesiones():
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''
    create or replace function bitacora7()
    returns trigger as $$
    declare 
	    usuario varchar(20) := user;
	    fecha date := current_date;
	    tiempo time := current_time;
    begin
	    insert into log_admin values (usuario, 'modificar sesion', fecha, tiempo);
	    return new;
    end;
    $$
    language plpgsql;

    create or replace trigger mod_sesiones
    before update
    on sesion
    for each row execute procedure bitacora7();

    create or replace function bitacora8()
    returns trigger as $$
    declare 
	    usuario varchar(20) := user;
	    fecha date := current_date;
	    tiempo time := current_time;
    begin
	    insert into log_admin values (usuario, 'eliminar sesion', fecha, tiempo);
	    return new;
    end;
    $$
    language plpgsql;

    create or replace trigger del_sesion
    before delete
    on sesion
    for each row execute procedure bitacora8();

    create or replace function bitacora9()
    returns trigger as $$
    declare 
	    usuario varchar(20) := user;
	    fecha date := current_date;
	    tiempo time := current_time;
    begin
	    insert into log_admin values (usuario, 'crear sesion', fecha, tiempo);
	    return new;
    end;
    $$
    language plpgsql;

    create or replace trigger ins_sesion
    after insert
    on sesion
    for each row execute procedure bitacora9();
    ''')

    conn.commit()
    conn.close()

def crearTriggers():
    trigger_usuario()
    trigger_instructor()
    trigger_sesiones()
## PANTALLA SIGNUP

def signup():
    frame = Toplevel(root)

    global us_id
    global us_nombre
    global us_apellido
    global us_edad
    global us_altura
    global us_cal
    global us_peso
    global us_pass
    global notifReg

    l_id = Label(frame, text= "ID de usuario:")
    l_id.grid(row= 0, column= 0, pady= 10, padx= 10)

    us_id = Entry(frame, font=("Helvetica, 18"))
    us_id.grid(row=0, column=1, pady=10, padx=10)

    l_nombre = Label(frame, text= "Nombre:")
    l_nombre.grid(row= 1, column= 0, pady= 10, padx= 10)

    us_nombre = Entry(frame, font=("Helvetica, 18"))
    us_nombre.grid(row=1, column=1, pady=10, padx=10)

    l_apellido = Label(frame, text= "Apellido:")
    l_apellido.grid(row= 2, column= 0, pady= 10, padx= 10)

    us_apellido = Entry(frame, font=("Helvetica, 18"))
    us_apellido.grid(row=2, column=1, pady=10, padx=10)

    l_edad = Label(frame, text= "Edad:")
    l_edad.grid(row= 3, column= 0, pady= 10, padx= 10)

    us_edad = Entry(frame, font=("Helvetica, 18"))
    us_edad.grid(row=3, column=1, pady=10, padx=10)

    l_altura = Label(frame, text= "Altura (metros):")
    l_altura.grid(row= 4, column= 0, pady= 10, padx= 10)

    us_altura = Entry(frame, font=("Helvetica, 18"))
    us_altura.grid(row=4, column=1, pady=10, padx=10)

    l_cal = Label(frame, text= "Calorias diarias:")
    l_cal.grid(row= 5, column= 0, pady= 10, padx= 10)

    us_cal = Entry(frame, font=("Helvetica, 18"))
    us_cal.grid(row=5, column=1, pady=10, padx=10)

    l_peso = Label(frame, text= "Peso:")
    l_peso.grid(row= 6, column= 0, pady= 10, padx= 10)

    us_peso = Entry(frame, font=("Helvetica, 18"))
    us_peso.grid(row=6, column=1, pady=10, padx=10)

    l_pass = Label(frame, text= "Contraseña:")
    l_pass.grid(row= 7, column= 0, pady= 10, padx= 10)

    us_pass = Entry(frame, font=("Helvetica, 18"))
    us_pass.grid(row=7, column=1, pady=10, padx=10)

    notifReg = Label(frame, font=("Helvetica, 18"))
    notifReg.grid(row=8, column=0, padx=10, pady=10)

    submit_log = Button(frame, text= "Registrar", font=("Helvetica", 20, "bold"), width=20, command=funcionReg)
    submit_log.grid(row=8, column=1, padx=10, pady=10)

def login():
    global userLogin
    global passLogin
    global loginNotif
    global plog

    plog = Toplevel(root)
    plog.title('Inicio de sesión')

    l_userLogin = Label(plog, text= "ID de usuario:")
    l_userLogin.grid(row= 0, column= 0, pady= 10, padx= 10)

    userLogin = Entry(plog, font=("Helvetica", 18))
    userLogin.grid(row=0, column=1, pady=10, padx=10)

    l_passLogin = Label(plog, text= "Contraseña:")
    l_passLogin.grid(row= 1, column= 0, pady= 10, padx= 10)

    passLogin = Entry(plog, show= "*")
    passLogin.grid(row=1, column=1, pady=10, padx=10)

    loginNotif = Label(plog, font=("Helvetica", 18))
    loginNotif.grid(row= 2, column= 0, pady= 10, padx= 10)

    submitLogin = Button(plog, text= "Ingresar", font=("Helvetica", 18, "bold"), command = validarLogin, width= 20)
    submitLogin.grid(row=2,column=1,pady=10,padx=10)

def validarLogin():
    try:
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

        c = conn.cursor()

        query = '''SELECT ID_usuario, password, nombre FROM usuario WHERE ID_usuario = %s AND password = %s'''
        c.execute(query, (userLogin.get(), passLogin.get()))
        global credenciales
        credenciales = c.fetchone()

        c.execute('''SELECT fecha_expiracion - fecha_registro AS DateDifference FROM suscripcion WHERE fk_id_usuario = %s''', (credenciales[0],))
        datediff = c.fetchone()

        if credenciales[0] == userLogin.get() and credenciales[1] == passLogin.get() and type(datediff) is NoneType:
            plog.destroy()
            mainSc = Toplevel(root)

            Label(mainSc, fg='red', text="No estás suscrito, suscribete y vuelve a iniciar sesión", font=("Helvetica", 18)).grid(row=0)
            botonSuscripcion = Button(mainSc, text='Suscripción', bg='sky blue', font=("Helvetica", 18), command=suscripcion)
            botonSuscripcion.grid(row=1)

        elif credenciales[0] == userLogin.get() and credenciales[1] == passLogin.get() and datediff[0] > 0:
            plog.destroy()
            mainSc = Toplevel(root)
            mainSc.title("Inicio")

            Label(mainSc, text="Bienvenid@ " + credenciales[2], font=("Helvetica", 24)).grid(row=0,pady=10)
            botonSuscripcion = Button(mainSc, text='Suscripción', bg='sky blue', font=("Helvetica", 18), command=suscripcion).grid(row=1,pady=10,padx=10)
            botonSesiones = Button(mainSc, text='Sesiones', bg='sky blue', font=("Helvetica", 18), command=sesiones).grid(row=2,pady=10,padx=10)
            botonConsulta = Button(mainSc, text='Registro de peso', bg='sky blue', font=("Helvetica", 18), command=consulta).grid(row=3,pady=10,padx=10)
            botonCalendario = Button(mainSc, text='Calendario', bg='sky blue', font=("Helvetica", 18), command=calendario).grid(row=5,pady=10,padx=10)
            notifNuevoPeso = Label(mainSc, font=("Helvetica", 16))
            notifNuevoPeso.grid(row=6,pady=10)
            queryNuevoPeso = '''
            SELECT CURRENT_DATE - MAX(fecha_semana) as DateDiffProgreso, MAX(semana) as UltimaSemana, peso_semanal
            FROM progreso 
            WHERE fk_id_usuario = %s
            GROUP BY peso_semanal, semana
            HAVING semana = MAX(semana)'''
            c.execute(queryNuevoPeso,(credenciales[0],))

            datediffPeso = c.fetchone()

            if datediffPeso[0] >= 7:
                def nuevoPeso(host1, database1, user1, password1, port1):
                    conn = psycopg2.connect(
                    host = host1,
                    database = database1,
                    user = user1,
                    password = password1,
                    port = port1

                    )

                    c = conn.cursor()

                    queryInsertNuevoPeso = '''INSERT INTO progreso VALUES(%s,%s,%s,%s,%s)'''
                    c.execute(queryInsertNuevoPeso, (credenciales[0], datediffPeso[1]+1 , entryNuevoPeso.get(), int(entryNuevoPeso.get()) - datediffPeso[2], datetime.today().date()))
                    conn.commit()
                    conn.close()
                    notifNuevoPeso.config(text="El peso se ha registrado con éxito", fg='green')
                    entryNuevoPeso.destroy()
                    botonNuevoPeso.destroy()
                
                notifNuevoPeso.config(text="Ingrese un nuevo peso para esta semana", fg='red')
                entryNuevoPeso = Entry(mainSc, font=("Helvetica", 16))
                entryNuevoPeso.grid(row=7,pady=10)
                botonNuevoPeso = Button(mainSc, text="Insertar peso", font=("Helvetica", 16), command= nuevoPeso)
                botonNuevoPeso.grid(row=8,pady=5)

        elif credenciales[0] == userLogin.get() and credenciales[1] == passLogin.get() and datediff[0] <= 0:
            plog.destroy()
            mainSc = Toplevel(root)
            queryUpdate = '''
            UPDATE suscripcion SET 
            num_tarjeta = NULL,
            cv_tarjeta = NULL,
            vence_tarjeta = NULL
            WHERE fk_ID_usuario is %s
            '''

            c.execute(queryUpdate, (credenciales[0],))
            conn.commit()

            Label(fg='red', text="No estás suscrito, suscribete y vuelve a iniciar sesión", font=("Helvetica", 18)).grid(row=0)
            botonSuscripcion = Button(mainSc, text='Suscripción', bg='sky blue', font=("Helvetica", 18), command=suscripcion)
            botonSuscripcion.grid(row=1)

    except (Exception, psycopg2.Error) as error:
        loginNotif.config(fg="red", text= "Credenciales incorrectos")
        print(error)

    conn.commit()
    conn.close()

def tiposAdmin():
    padmin = Toplevel(root)
    padmin.title("Funciones de administrador")
    botoneditaradmin = Button(padmin, text='Administrador de usuarios', bg='sky blue', font=("Helvetica", 18), command=adminUsuariosLogin).grid(row=1,pady=10,padx=10)
    botonInstructores = Button(padmin, text='Administrador de sesiones', bg='sky blue', font=("Helvetica", 18), command=adminSesionesLogin).grid(row=2,pady=10,padx=10)
    botonSesiones = Button(padmin, text='Superadministrador', bg='sky blue', font=("Helvetica", 18), command=SuperAdminLogin).grid(row=3,pady=10,padx=10)
    

def adminUsuariosLogin():
    global adminUser
    global adminpassLogin
    global loginNotif
    global padminLogin

    padminLogin = Toplevel(root)
    padminLogin.title("Admin Usuario Login")

    l_adminLogin = Label(padminLogin, text= "ID de usuario:")
    l_adminLogin.grid(row= 0, column= 0, pady= 10, padx= 10)

    adminUser = Entry(padminLogin, font=("Helvetica", 18))
    adminUser.grid(row=0, column=1, pady=10, padx=10)

    l_adminpassLogin = Label(padminLogin, text= "Contraseña:")
    l_adminpassLogin.grid(row= 1, column= 0, pady= 10, padx= 10)

    adminpassLogin = Entry(padminLogin, show = "*")
    adminpassLogin.grid(row=1, column=1, pady=10, padx=10)

    loginNotif = Label(padminLogin, font=("Helvetica", 18))
    loginNotif.grid(row= 2, column= 0, pady= 10, padx= 10)

    submitLogin = Button(padminLogin, text= "Ingresar", font=("Helvetica", 18, "bold"), command = validarAdminULogin, width= 20)
    submitLogin.grid(row=2,column=1,pady=10,padx=10)

def validarAdminULogin():
    try:
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user2,
            password = password2,
            port = port1)
            

        nivel_aislamiento = extensions.ISOLATION_LEVEL_SERIALIZABLE
        conn.set_isolation_level(nivel_aislamiento)
        c = conn.cursor()

        query = '''SELECT user_admin, pass_admin FROM adminu WHERE user_admin = %s AND pass_admin = %s'''
        c.execute(query, (adminUser.get(), adminpassLogin.get()))
        global credencialesAdmin
        credencialesAdmin = c.fetchone()

        if credencialesAdmin[0] == adminUser.get() and credencialesAdmin[1] == adminpassLogin.get():
            padminLogin.destroy()
            padmin = Toplevel(root)
            padmin.title("Funciones de administrador de usuarios")

            
            botonUsuarios = Button(padmin, text='Editar usuarios', bg='sky blue', font=("Helvetica", 18), command=AdmUsuario).grid(row=0,pady=10,padx=10)
           


    except (Exception, psycopg2.Error) as error:
        loginNotif.config(fg="red", text= "Credenciales incorrectos")
        print(error)

def adminSesionesLogin():
    global adminUser
    global adminpassLogin
    global loginNotif
    global padminLogin

    padminLogin = Toplevel(root)
    padminLogin.title("Admin Sesiones Login")

    l_adminLogin = Label(padminLogin, text= "ID de usuario:")
    l_adminLogin.grid(row= 0, column= 0, pady= 10, padx= 10)

    adminUser = Entry(padminLogin, font=("Helvetica", 18))
    adminUser.grid(row=0, column=1, pady=10, padx=10)

    l_adminpassLogin = Label(padminLogin, text= "Contraseña:")
    l_adminpassLogin.grid(row= 1, column= 0, pady= 10, padx= 10)

    adminpassLogin = Entry(padminLogin, show = "*")
    adminpassLogin.grid(row=1, column=1, pady=10, padx=10)

    loginNotif = Label(padminLogin, font=("Helvetica", 18))
    loginNotif.grid(row= 2, column= 0, pady= 10, padx= 10)

    submitLogin = Button(padminLogin, text= "Ingresar", font=("Helvetica", 18, "bold"), command = validarAdminSeLogin, width= 20)
    submitLogin.grid(row=2,column=1,pady=10,padx=10)

def validarAdminSeLogin():
    try:
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user3,
            password = password3,
            port = port1)
            

        nivel_aislamiento = extensions.ISOLATION_LEVEL_SERIALIZABLE
        conn.set_isolation_level(nivel_aislamiento)
        c = conn.cursor()

        query = '''SELECT user_admin, pass_admin FROM admins WHERE user_admin = %s AND pass_admin = %s'''
        c.execute(query, (adminUser.get(), adminpassLogin.get()))
        global credencialesAdmin
        credencialesAdmin = c.fetchone()

        if credencialesAdmin[0] == adminUser.get() and credencialesAdmin[1] == adminpassLogin.get():
            padminLogin.destroy()
            padmin = Toplevel(root)
            padmin.title("Funciones de administrador")

            botonInstructores = Button(padmin, text='Editar instructores', bg='sky blue', font=("Helvetica", 18), command=AdmInstructor).grid(row=1,pady=10,padx=10)
            botonSesiones = Button(padmin, text='Editar sesiones', bg='sky blue', font=("Helvetica", 18), command=AdmSesion).grid(row=2,pady=10,padx=10)
           
    except (Exception, psycopg2.Error) as error:
        loginNotif.config(fg="red", text= "Credenciales incorrectos")
        print(error)

def SuperAdminLogin():
    global adminUser
    global adminpassLogin
    global loginNotif
    global padminLogin

    padminLogin = Toplevel(root)
    padminLogin.title("SuperAdmin Login")

    l_adminLogin = Label(padminLogin, text= "ID de usuario:")
    l_adminLogin.grid(row= 0, column= 0, pady= 10, padx= 10)

    adminUser = Entry(padminLogin, font=("Helvetica", 18))
    adminUser.grid(row=0, column=1, pady=10, padx=10)

    l_adminpassLogin = Label(padminLogin, text= "Contraseña:")
    l_adminpassLogin.grid(row= 1, column= 0, pady= 10, padx= 10)

    adminpassLogin = Entry(padminLogin, show = "*")
    adminpassLogin.grid(row=1, column=1, pady=10, padx=10)

    loginNotif = Label(padminLogin, font=("Helvetica", 18))
    loginNotif.grid(row= 2, column= 0, pady= 10, padx= 10)

    submitLogin = Button(padminLogin, text= "Ingresar", font=("Helvetica", 18, "bold"), command = validarSuperadminLogin, width= 20)
    submitLogin.grid(row=2,column=1,pady=10,padx=10)

def validarSuperadminLogin():
    try:
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user4,
            password = password4,
            port = port1)
            

        nivel_aislamiento = extensions.ISOLATION_LEVEL_SERIALIZABLE
        conn.set_isolation_level(nivel_aislamiento)
        c = conn.cursor()

        query = '''SELECT user_admin, pass_admin FROM superadm WHERE user_admin = %s AND pass_admin = %s'''
        c.execute(query, (adminUser.get(), adminpassLogin.get()))
        global credencialesAdmin
        credencialesAdmin = c.fetchone()

        if credencialesAdmin[0] == adminUser.get() and credencialesAdmin[1] == adminpassLogin.get():
            padminLogin.destroy()
            padmin = Toplevel(root)
            padmin.title("Funciones de administrador")

            botoneditaradmin = Button(padmin, text='Editar administradores', bg='sky blue', font=("Helvetica", 18), command=Admadmins).grid(row=1,pady=10,padx=10)
            botonReportes = Button(padmin, text='Reportería', bg='sky blue', font=("Helvetica", 18), command=reportes).grid(row=2,pady=10,padx=10)


    except (Exception, psycopg2.Error) as error:
        loginNotif.config(fg="red", text= "Credenciales incorrectos")
        print(error)
    
def Admadmins():
    conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user4,
            password = password4,
            port = port1

        )

    c = conn.cursor()

    c.execute("SELECT * FROM admins")
    data = c.fetchall()

    pAdministrador = Toplevel(root)
    pAdministrador.title("Editar administradores")
    pAdministrador.geometry("1000x500")

    conn.commit()
    conn.close()

    def borrarAdmS(host1, database1, user4, password4, port1):
       
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user4,
            password = password4,
            port = port1

        )

        c = conn.cursor()

        c.execute("DELETE from admins WHERE user_admin = %s", (fn_entry.get(),))

        conn.commit()

        conn.close()

        despejar_casillas()

        messagebox.showinfo("Administrador Eliminado!", "Eliminado exitósamente")

    def despejar_casillas():
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)

    def borrarAdmU(host1, database1, user4, password4, port1):
       
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user4,
            password = password4,
            port = port1

        )

        c = conn.cursor()

        c.execute("DELETE from adminu WHERE user_admin = %s", (fn_entry.get(),))

        conn.commit()

        conn.close()

        despejar_casillas()

        messagebox.showinfo("Administrador Eliminado!", "Eliminado exitósamente")

    def despejar_casillas():
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)

    def add_adminU():
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user4,
            password = password4,
            port = port1

        )

        c = conn.cursor()
        c.execute("INSERT INTO adminu VALUES (%s,%s)",
            (
                fn_entry.get(),
                ln_entry.get(),
            ))

        conn.commit()
        conn.close()

        despejar_casillas()


    def add_adminS():
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

        c = conn.cursor()
        c.execute("INSERT INTO admins VALUES (%s,%s)",
            (
                fn_entry.get(),
                ln_entry.get(),
            ))

        conn.commit()
        conn.close()

        despejar_casillas()

        

    data_frame = LabelFrame(pAdministrador, text="Selección")
    data_frame.pack(fill="x", expand="yes", padx=20)

    fn_label = Label(data_frame, text="Usuario")
    fn_label.grid(row=0, column=0, padx=10, pady=10)
    fn_entry = Entry(data_frame)
    fn_entry.grid(row=0, column=1, padx=10, pady=10)

    ln_label = Label(data_frame, text="Constraseña")
    ln_label.grid(row=0, column=2, padx=10, pady=10)
    ln_entry = Entry(data_frame)
    ln_entry.grid(row=0, column=3, padx=10, pady=10)

    button_frame = LabelFrame(pAdministrador, text="Funciones")
    button_frame.pack(fill="x", expand="yes", padx=20)
   

    add_button = Button(button_frame, text="Agregar administrador de usuarios", command=add_adminU)
    add_button.grid(row=0, column=0, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Agregar administrador de sesiones", command=add_adminS)
    remove_one_button.grid(row=0, column=3, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Eliminar administrador de usuarios", command=borrarAdmU)
    remove_one_button.grid(row=0, column=5, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Eliminar administrador de sesiones", command=borrarAdmS)
    remove_one_button.grid(row=0, column=5, padx=10, pady=10)


def AdmInstructor():
    conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user3,
            password = password3,
            port = port1

        )

    c = conn.cursor()

    c.execute("SELECT * FROM instructor")
    data = c.fetchall()

    pInstructor = Toplevel(root)
    pInstructor.title("Administrador de instructores")
    pInstructor.geometry("1000x500")

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    style.map('Treeview',
        background=[('selected', "#347083")])
    
    tree_frame = Frame(pInstructor)
    tree_frame.pack(pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("Nombre de instructor", "Apellido de instructor")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Nombre de instructor", anchor=W, width=140)
    my_tree.column("Apellido de instructor", anchor=W, width=140)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Nombre de instructor", text="Nombre de instructor", anchor=W)
    my_tree.heading("Apellido de instructor", text="Apellido de instructor", anchor=W)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    global count
    count = 0

    for record in data:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('oddrow',))
        
        count += 1
    conn.commit()
    conn.close()

    def borrarUno():
        x = my_tree.selection()[0]
        my_tree.delete(x)

        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user3,
            password = password3,
            port = port1

        )

        c = conn.cursor()

        c.execute("DELETE from instructor WHERE nombre_instructor = %s", (fn_entry.get(),))

        conn.commit()

        conn.close()

        despejar_casillas()

        messagebox.showinfo("Eliminado!", "Eliminado exitósamente")

    def borrarMuchos():
        response = messagebox.askyesno("Seguridad", "Esto borrará todas las selecciones\nEstá seguro!")

        if response == 1:
            x = my_tree.selection()

            ids_to_delete = []
            
            for record in x:
                ids_to_delete.append(my_tree.item(record, 'values')[0])

            for record in x:
                my_tree.delete(record)

            conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user3,
            password = password3,
            port = port1

            )

            c = conn.cursor()
            
            for record in ids_to_delete:
                c.execute('''DELETE FROM instructor WHERE nombre_instructor = %s''', (record,))

            ids_to_delete = []

            conn.commit()

            conn.close()

            despejar_casillas()

    def despejar_casillas():
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)

    def update_record():

        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user3,
            password = password3,
            port = port1

        )

        c = conn.cursor()
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        c.execute("""UPDATE instructor SET
            nombre_instructor = %s,
            apellido_instructor = %s

            WHERE nombre_instructor = %s""",
            (
                fn_entry.get(),
                ln_entry.get(),
                values[0]
            ))

        conn.commit()
        conn.close()

        my_tree.item(selected, text="", values=(fn_entry.get(), ln_entry.get()))

        despejar_casillas()

    def add_record():
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user3,
            password = password3,
            port = port1

        )

        c = conn.cursor()

        c.execute("INSERT INTO instructor VALUES (%s,%s)",
            (
                fn_entry.get(),
                ln_entry.get(),
            ))

        conn.commit()

        conn.close()

        despejar_casillas()

        my_tree.delete(*my_tree.get_children())

        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user3,
            password = password3,
            port = port1

        )

        c = conn.cursor()

        c.execute("SELECT * FROM instructor")
        data = c.fetchall()
        global count
        count = 0

        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('oddrow',))
            
            count += 1
        
        conn.commit()
        conn.close()

    def select_record(e):
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        fn_entry.insert(0, values[0])
        ln_entry.insert(0, values[1])


    data_frame = LabelFrame(pInstructor, text="Selección")
    data_frame.pack(fill="x", expand="yes", padx=20)

    fn_label = Label(data_frame, text="Nombre")
    fn_label.grid(row=0, column=0, padx=10, pady=10)
    fn_entry = Entry(data_frame)
    fn_entry.grid(row=0, column=1, padx=10, pady=10)

    ln_label = Label(data_frame, text="Apellido")
    ln_label.grid(row=0, column=2, padx=10, pady=10)
    ln_entry = Entry(data_frame)
    ln_entry.grid(row=0, column=3, padx=10, pady=10)

    button_frame = LabelFrame(pInstructor, text="Funciones")
    button_frame.pack(fill="x", expand="yes", padx=20)

    update_button = Button(button_frame, text="Actualizar", command=update_record)
    update_button.grid(row=0, column=0, padx=10, pady=10)

    add_button = Button(button_frame, text="Agregar", command=add_record)
    add_button.grid(row=0, column=1, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Eliminar uno", command=borrarUno)
    remove_one_button.grid(row=0, column=3, padx=10, pady=10)

    remove_many_button = Button(button_frame, text="Eliminar muchos", command=borrarMuchos)
    remove_many_button.grid(row=0, column=4, padx=10, pady=10)

    select_record_button = Button(button_frame, text="Despejar casillas", command= despejar_casillas)
    select_record_button.grid(row=0, column=5, padx=10, pady=10)

    my_tree.bind("<ButtonRelease-1>", select_record)

def AdmSesion():
    conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

    c = conn.cursor()

    c.execute("SELECT * FROM sesion")
    data = c.fetchall()

    pInstructor = Toplevel(root)
    pInstructor.title("Administrador de sesiones")

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    style.map('Treeview',
        background=[('selected', "#347083")])
    
    tree_frame = Frame(pInstructor)
    tree_frame.pack(pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("ID sesión", "Categoría", "Nombre del instructor", "Fecha y hora de inicio", "Fecha y hora de fin")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID sesión", anchor=W, width=140)
    my_tree.column("Categoría", anchor=W, width=140)
    my_tree.column("Nombre del instructor", anchor=W, width=140)
    my_tree.column("Fecha y hora de inicio", anchor=W, width=140)
    my_tree.column("Fecha y hora de fin", anchor=W, width=140)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ID sesión", text="ID sesión", anchor=W)
    my_tree.heading("Categoría", text="Categoría", anchor=W)
    my_tree.heading("Nombre del instructor", text="Nombre del instructor", anchor=W)
    my_tree.heading("Fecha y hora de inicio", text="Fecha y hora de inicio", anchor=W)
    my_tree.heading("Fecha y hora de fin", text="Fecha y hora de fin", anchor=W)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    global count
    count = 0

    for record in data:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
        
        count += 1
    conn.commit()
    conn.close()

    def borrarUno():
        x = my_tree.selection()[0]
        my_tree.delete(x)

        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

        c = conn.cursor()

        c.execute("DELETE from sesion WHERE id_sesion = %s", (id_entry.get(),))

        conn.commit()

        conn.close()

        despejar_casillas()

        messagebox.showinfo("Eliminado!", "Eliminado exitósamente")

    def borrarMuchos():
        response = messagebox.askyesno("Seguridad", "Esto borrará todas las selecciones\nEstá seguro!")

        if response == 1:
            x = my_tree.selection()

            ids_to_delete = []
            
            for record in x:
                ids_to_delete.append(my_tree.item(record, 'values')[0])

            for record in x:
                my_tree.delete(record)

            conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

            )

            c = conn.cursor()
            
            for record in ids_to_delete:
                c.execute('''DELETE FROM sesion WHERE id_sesion = %s''', (record,))

            ids_to_delete = []

            conn.commit()

            conn.close()

            despejar_casillas()

    def despejar_casillas():
        id_entry.delete(0, END)
        cat_entry.delete(0, END)
        inst_entry.delete(0, END)
        ini_entry.delete(0, END)
        fin_entry.delete(0, END)

    def update_record():

        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

        c = conn.cursor()
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        c.execute("""UPDATE sesion SET
            id_sesion = %s,
            categoria = %s,
            fk_nombre_instructor = %s,
            fecha_hora_inicio = %s,
            fecha_hora_fin = %s

            WHERE id_sesion = %s""",
            (
                id_entry.get(),
                cat_entry.get(),
                inst_entry.get(),
                ini_entry.get(),
                fin_entry.get(),
                values[0]
            ))

        conn.commit()
        conn.close()

        my_tree.item(selected, text="", values=(id_entry.get(), cat_entry.get(), inst_entry.get(), ini_entry.get(), fin_entry.get()))

        despejar_casillas()  

    def add_record():
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

        c = conn.cursor()

        c.execute("INSERT INTO sesion VALUES (%s,%s,%s,%s,%s)",
            (
                id_entry.get(),
                cat_entry.get(),
                inst_entry.get(),
                ini_entry.get(),
                fin_entry.get()
            ))

        conn.commit()

        conn.close()

        despejar_casillas()       

        my_tree.delete(*my_tree.get_children())

        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

        c = conn.cursor()

        c.execute("SELECT * FROM sesion")
        data = c.fetchall()
        global count
        count = 0

        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            
            count += 1
        
        conn.commit()
        conn.close()

    def select_record(e):
        id_entry.delete(0, END)
        cat_entry.delete(0, END)
        inst_entry.delete(0, END)
        ini_entry.delete(0, END)
        fin_entry.delete(0, END)

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        id_entry.insert(0, values[0])
        cat_entry.insert(0, values[1])
        inst_entry.insert(0, values[2])
        ini_entry.insert(0, values[3])
        fin_entry.insert(0, values[4])


    data_frame = LabelFrame(pInstructor, text="Selección")
    data_frame.pack(fill="x", expand="yes", padx=20)

    id_label = Label(data_frame, text="ID sesión")
    id_label.grid(row=0, column=0, padx=10, pady=10)
    id_entry = Entry(data_frame)
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    cat_label = Label(data_frame, text="Categoría")
    cat_label.grid(row=0, column=2, padx=10, pady=10)
    cat_entry = Entry(data_frame)
    cat_entry.grid(row=0, column=3, padx=10, pady=10)

    inst_label = Label(data_frame, text="Instructor")
    inst_label.grid(row=0, column=4, padx=10, pady=10)
    inst_entry = Entry(data_frame)
    inst_entry.grid(row=0, column=5, padx=10, pady=10)

    ini_label = Label(data_frame, text="Inicio (YYYY-MM-DD HH:MM:SS)")
    ini_label.grid(row=1, column=0, padx=10, pady=10)
    ini_entry = Entry(data_frame)
    ini_entry.grid(row=1, column=1, padx=10, pady=10)

    fin_label = Label(data_frame, text="Fin (YYYY-MM-DD HH:MM:SS)")
    fin_label.grid(row=1, column=2, padx=10, pady=10)
    fin_entry = Entry(data_frame)
    fin_entry.grid(row=1, column=3, padx=10, pady=10)

    button_frame = LabelFrame(pInstructor, text="Funciones")
    button_frame.pack(fill="x", expand="yes", padx=20)

    update_button = Button(button_frame, text="Actualizar", command=update_record)
    update_button.grid(row=0, column=0, padx=10, pady=10)

    add_button = Button(button_frame, text="Agregar", command=add_record)
    add_button.grid(row=0, column=1, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Eliminar uno", command=borrarUno)
    remove_one_button.grid(row=0, column=3, padx=10, pady=10)

    remove_many_button = Button(button_frame, text="Eliminar muchos", command=borrarMuchos)
    remove_many_button.grid(row=0, column=4, padx=10, pady=10)

    select_record_button = Button(button_frame, text="Despejar casillas", command= despejar_casillas)
    select_record_button.grid(row=0, column=5, padx=10, pady=10)

    my_tree.bind("<ButtonRelease-1>", select_record)

def AdmUsuario():
    conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

    c = conn.cursor()

    c.execute("SELECT * FROM usuario")
    data = c.fetchall()

    pInstructor = Toplevel(root)
    pInstructor.title("Administrador de usuarios")

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    style.map('Treeview',
        background=[('selected', "#347083")])
    
    tree_frame = Frame(pInstructor)
    tree_frame.pack(pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("ID usuario", "Nombre", "Apellido", "Edad", "Altura", "Calorías diarias", "Peso registrado", "Contraseña")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID usuario", anchor=W, width=100)
    my_tree.column("Nombre", anchor=W, width=100)
    my_tree.column("Apellido", anchor=W, width=100)
    my_tree.column("Edad", anchor=W, width=100)
    my_tree.column("Altura", anchor=W, width=100)
    my_tree.column("Calorías diarias", anchor=W, width=100)
    my_tree.column("Peso registrado", anchor=W, width=100)
    my_tree.column("Contraseña", anchor=W, width=100)
    

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ID usuario", text="ID usuario", anchor=W)
    my_tree.heading("Nombre", text="Nombre", anchor=W)
    my_tree.heading("Apellido", text="Apellido", anchor=W)
    my_tree.heading("Edad", text="Edad", anchor=W)
    my_tree.heading("Altura", text="Altura", anchor=W)
    my_tree.heading("Calorías diarias", text="Calorías diarias", anchor=W)
    my_tree.heading("Peso registrado", text="Peso registrado", anchor=W)
    my_tree.heading("Contraseña", text="Contraseña", anchor=W)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    global count
    count = 0

    for record in data:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]), tags=('oddrow',))
        
        count += 1
    conn.commit()
    conn.close()

    def borrarUno():
        x = my_tree.selection()[0]
        my_tree.delete(x)

        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user2,
            password = password2,
            port = port1
        )

        c = conn.cursor()

        c.execute("DELETE from usuario WHERE id_usuario = %s", (id_entry.get(),))

        conn.commit()

        conn.close()

        despejar_casillas()

        messagebox.showinfo("Eliminado!", "Eliminado exitósamente")

    def borrarMuchos():
        response = messagebox.askyesno("Seguridad", "Esto borrará todas las selecciones\nEstá seguro?")

        if response == 1:
            x = my_tree.selection()

            ids_to_delete = []
            
            for record in x:
                ids_to_delete.append(my_tree.item(record, 'values')[0])

            for record in x:
                my_tree.delete(record)

            conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user2,
            password = password2,
            port = port1

            )

            c = conn.cursor()
            
            for record in ids_to_delete:
                c.execute('''DELETE FROM usuario WHERE id_usuario = %s''', (record,))

            ids_to_delete = []

            conn.commit()

            conn.close()

            despejar_casillas()

    def despejar_casillas():
        id_entry.delete(0, END)
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)
        edad_entry.delete(0, END)
        alt_entry.delete(0, END)
        cal_entry.delete(0, END)
        w_entry.delete(0, END)
        pw_entry.delete(0, END)

    def update_record():

        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user2,
            password = password2,
            port = port1

        )

        c = conn.cursor()
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        c.execute("""UPDATE usuario SET
            id_usuario = %s,
            nombre = %s,
            apellido = %s,
            edad = %s,
            altura = %s,
            calorias_diarias = %s,
            peso_actual = %s,
            password = %s

            WHERE id_usuario = %s""",
            (
                id_entry.get(),
                fn_entry.get(),
                ln_entry.get(),
                edad_entry.get(),
                alt_entry.get(),
                cal_entry.get(),
                w_entry.get(),
                pw_entry.get(),
                values[0]
            ))

        conn.commit()
        conn.close()

        my_tree.item(selected, text="", values=(id_entry.get(), fn_entry.get(), ln_entry.get(), edad_entry.get(), alt_entry.get(), cal_entry.get(), w_entry.get(), pw_entry.get()))

        despejar_casillas()  

    def add_record():
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user2,
            password = password2,
            port = port1

        )

        c = conn.cursor()

        c.execute("INSERT INTO usuario VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                id_entry.get(),
                fn_entry.get(),
                ln_entry.get(),
                edad_entry.get(),
                alt_entry.get(),
                cal_entry.get(),
                w_entry.get(),
                pw_entry.get()
            ))

        conn.commit()

        conn.close()

        despejar_casillas()       

        my_tree.delete(*my_tree.get_children())

        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

        c = conn.cursor()

        c.execute("SELECT * FROM sesion")
        data = c.fetchall()
        global count
        count = 0

        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            
            count += 1
        
        conn.commit()
        conn.close()

    def select_record(e):
        despejar_casillas()

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        id_entry.insert(0, values[0])
        fn_entry.insert(0, values[1])
        ln_entry.insert(0, values[2])
        edad_entry.insert(0, values[3])
        alt_entry.insert(0, values[4])
        cal_entry.insert(0, values[5])
        w_entry.insert(0, values[6])
        pw_entry.insert(0, values[7])

    data_frame = LabelFrame(pInstructor, text="Selección")
    data_frame.pack(fill="x", expand="yes", padx=20)

    id_label = Label(data_frame, text="ID usuario")
    id_label.grid(row=0, column=0, padx=10, pady=10)
    id_entry = Entry(data_frame)
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    fn_label = Label(data_frame, text="Nombre")
    fn_label.grid(row=0, column=2, padx=10, pady=10)
    fn_entry = Entry(data_frame)
    fn_entry.grid(row=0, column=3, padx=10, pady=10)

    ln_label = Label(data_frame, text="Apellido")
    ln_label.grid(row=0, column=4, padx=10, pady=10)
    ln_entry = Entry(data_frame)
    ln_entry.grid(row=0, column=5, padx=10, pady=10)

    edad_label = Label(data_frame, text="Edad")
    edad_label.grid(row=0, column=6, padx=10, pady=10)
    edad_entry = Entry(data_frame)
    edad_entry.grid(row=0, column=7, padx=10, pady=10)

    alt_label = Label(data_frame, text="Altura")
    alt_label.grid(row=1, column=0, padx=10, pady=10)
    alt_entry = Entry(data_frame)
    alt_entry.grid(row=1, column=1, padx=10, pady=10)

    cal_label = Label(data_frame, text="Calorías")
    cal_label.grid(row=1, column=2, padx=10, pady=10)
    cal_entry = Entry(data_frame)
    cal_entry.grid(row=1, column=3, padx=10, pady=10)

    w_label = Label(data_frame, text="Peso")
    w_label.grid(row=1, column=4, padx=10, pady=10)
    w_entry = Entry(data_frame)
    w_entry.grid(row=1, column=5, padx=10, pady=10)

    pw_label = Label(data_frame, text="Contraseña")
    pw_label.grid(row=1, column=6, padx=10, pady=10)
    pw_entry = Entry(data_frame)
    pw_entry.grid(row=1, column=7, padx=10, pady=10)

    button_frame = LabelFrame(pInstructor, text="Funciones")
    button_frame.pack(fill="x", expand="yes", padx=20)

    update_button = Button(button_frame, text="Actualizar", command=update_record)
    update_button.grid(row=0, column=0, padx=10, pady=10)

    add_button = Button(button_frame, text="Agregar", command=add_record)
    add_button.grid(row=0, column=1, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Eliminar uno", command=borrarUno)
    remove_one_button.grid(row=0, column=3, padx=10, pady=10)

    remove_many_button = Button(button_frame, text="Eliminar muchos", command=borrarMuchos)
    remove_many_button.grid(row=0, column=4, padx=10, pady=10)

    select_record_button = Button(button_frame, text="Despejar casillas", command= despejar_casillas)
    select_record_button.grid(row=0, column=5, padx=10, pady=10)

    my_tree.bind("<ButtonRelease-1>", select_record)

def suscripcion():
    conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1
        )

    c = conn.cursor()

    psus = Toplevel(root)
    psus.title("Administrador de suscripción")
    labelStatus = Label(psus, font=("Helvetica", 18))
    labelStatus.grid(row=0)
    user = credenciales[0]
    c.execute('''
    SELECT fecha_expiracion FROM suscripcion WHERE fk_ID_usuario = %s
    ''', (user,))
    fechaExp = c.fetchone()

    if type(fechaExp) is NoneType:
        labelStatus.config(fg='red',text="No se encuentra suscrito actualmente")
        extenderSub = Button(psus, text="Extender suscripción", bg='sky blue', font=("Helvetica", 18), command=botonSub)
        extenderSub.grid(row=1)

    elif fechaExp[0] >= datetime.today().date():
        def cancelarSub():
            conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

            )

            c = conn.cursor()

            c.execute('''
            DELETE FROM suscripcion
            WHERE fk_id_usuario = %s
            ''', (credenciales[0],))
            
            conn.commit()
            conn.close()

            labelStatus.config(fg='red',text="No se encuentra suscrito actualmente")
            botonCancelar.destroy()
            messagebox.showinfo("Cancelada", "Su suscripción fue cancelada con éxito")

        labelStatus.config(fg='green',text="Su suscripción se encuentra activa")
        botonCancelar = Button(psus, text="Cancelar suscripción", command=cancelarSub)
        botonCancelar.grid(row=2)
        
    else:
        labelStatus.config(fg='red',text="No se encuentra suscrito actualmente")
        extenderSub = Button(psus, text="Extender suscripción", bg='sky blue', font=("Helvetica", 18), command=botonSub)
        extenderSub.grid(row=1)

    conn.commit()
    conn.close()
    
def botonSub():
    global entryNumTarjeta
    global entryCV
    global entryVence

    pextender = Toplevel(root)
    Label(pextender, text="Número de tarjeta", font=("Helvetica", 18)).pack(anchor=W)
    entryNumTarjeta = Entry(pextender, font=("Helvetica", 18))
    entryNumTarjeta.pack(anchor=E)

    Label(pextender, text="Código de seguridad", font=("Helvetica", 18)).pack(anchor=W)
    entryCV = Entry(pextender, font=("Helvetica", 18))
    entryCV.pack(anchor=E)

    Label(pextender, text="Fecha de vencimiento", font=("Helvetica", 18)).pack(anchor=W)
    entryVence = Entry(pextender, font=("Helvetica", 18))
    entryVence.pack(anchor=E)

    global radio
    radio = StringVar()

    Label(pextender, text="Tipo", font=("Helvetica", 18)).pack(anchor=W)
    rOro = Radiobutton(pextender, font=("Helvetica", 12), variable= radio, value= "Oro", command= seleccionTipo, text="Oro - 30 días - $30")
    rOro.pack(anchor=E)
    rDiamante = Radiobutton(pextender, font=("Helvetica", 12), variable= radio, value= "Diamante", command= seleccionTipo, text="Diamante - 90 días - $50")
    rDiamante.pack(anchor=E)

    global labelNotifSus
    labelNotifSus = Label(pextender, font=("Helvetica", 18))
    labelNotifSus.pack(anchor=W)
    botonSubmitSus = Button(pextender, font=("Helvetica", 18), text="Pagar", command=submitSuscripcion)
    botonSubmitSus.pack(anchor=E)

def submitSuscripcion():
    longSub = 0
    if seleccion == "Oro":
        longSub = 30
    elif seleccion == "Diamante":
        longSub = 90
    conn = psycopg2.connect(
        host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1
    )

    c = conn.cursor()

    c.execute('''INSERT INTO suscripcion(fk_ID_usuario, tipo, num_tarjeta, cv_tarjeta, vence_tarjeta, fecha_registro, fecha_expiracion)
    VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
    (credenciales[0] ,seleccion, entryNumTarjeta.get(), int(entryCV.get()), entryVence.get(), datetime.today().strftime('%Y-%m-%d'), (datetime.today() + timedelta(days= longSub)).strftime('%Y-%m-%d'))
    )

    labelNotifSus.config(text="Se ha suscrito con éxito", fg='green')

    conn.commit()
    conn.close()

def seleccionTipo():
    global seleccion
    seleccion = radio.get()

def sesiones():
    def queryDatabase():
        for item in my_tree.get_children():
            my_tree.delete(item)

        conn = psycopg2.connect(
                host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

            )

        c = conn.cursor()

        c.execute('''
        SELECT * 
        FROM sesion
        WHERE NOT EXISTS (SELECT registro_sesion.fk_id_sesion FROM registro_sesion WHERE sesion.id_sesion = registro_sesion.fk_id_sesion AND registro_sesion.fk_id_usuario = %s)
        AND NOW() <= fecha_hora_fin
        ''', (credenciales[0], )
        )
        data = c.fetchall()

        global count
        count = 0

        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            
            count += 1
        conn.commit()
        conn.close()
    
    def add_record():
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

        c = conn.cursor()

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        c.execute("INSERT INTO registro_sesion VALUES (%s,%s)",
            (
                values[0],
                credenciales[0]
            ))

        conn.commit()

        conn.close()

        queryDatabase()

        messagebox.showinfo("Agregado", "La sesión ha sido agregada con éxito")

    def busqueda():
        global fecha_entry, hora_entry, dura_entry, inst_entry, cat_entry, search

        search = Toplevel(root)
        search.title("Busqueda")

        fecha_frame = LabelFrame(search, text="Fecha")
        fecha_frame.pack(padx=10, pady=10)

        fecha_entry = Entry(fecha_frame, font=("Helvetica", 18))
        fecha_entry.pack(pady=5, padx=20)

        fecha_button = Button(fecha_frame, text="Buscar fecha", command=search_fecha)
        fecha_button.pack(padx=20)

        hora_frame = LabelFrame(search, text="Hora (Número de 0 a 23)")
        hora_frame.pack(padx=10, pady=10)

        hora_entry = Entry(hora_frame, font=("Helvetica", 18))
        hora_entry.pack(pady=5, padx=20)

        hora_button = Button(hora_frame, text="Buscar hora", command=search_hora)
        hora_button.pack(padx=20)

        dura_frame = LabelFrame(search, text="Duración (Cantidad de minutos)")
        dura_frame.pack(padx=10, pady=10)

        dura_entry = Entry(dura_frame, font=("Helvetica", 18))
        dura_entry.pack(pady=5, padx=20)

        dura_button = Button(dura_frame, text="Buscar duración", command=search_dura)
        dura_button.pack(padx=20)

        inst_frame = LabelFrame(search, text="Instructor")
        inst_frame.pack(padx=10, pady=10)

        inst_entry = Entry(inst_frame, font=("Helvetica", 18))
        inst_entry.pack(pady=5, padx=20)

        inst_button = Button(inst_frame, text="Buscar instructor", command=search_inst)
        inst_button.pack(padx=20)

        cat_frame = LabelFrame(search, text="Categoría")
        cat_frame.pack(padx=10, pady=10)

        cat_entry = Entry(cat_frame, font=("Helvetica", 18))
        cat_entry.pack(pady=5, padx=20)

        cat_button = Button(cat_frame, text="Buscar categoría", command=search_cat)
        cat_button.pack(padx=20)

    def search_fecha():
        lookup_record = fecha_entry.get()
        search.destroy()
        
        for record in my_tree.get_children():
            my_tree.delete(record)
        
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

        c = conn.cursor()

        c.execute('''
        SELECT * 
        FROM sesion 
        WHERE fecha_hora_inicio::TIMESTAMP::DATE = %s
        AND NOW() <= fecha_hora_fin::TIMESTAMP
        AND NOT EXISTS
        (SELECT registro_sesion.fk_id_sesion FROM registro_sesion WHERE sesion.id_sesion = registro_sesion.fk_id_sesion AND registro_sesion.fk_id_usuario = %s)
        ''', (lookup_record, credenciales[0]))
        records = c.fetchall()
        
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            count += 1

        conn.commit()
        conn.close()

    def search_hora():
        lookup_record = hora_entry.get()
        search.destroy()
        
        for record in my_tree.get_children():
            my_tree.delete(record)
        
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

        c = conn.cursor()

        c.execute('''
        SELECT * 
        FROM sesion 
        WHERE date_part('hour', fecha_hora_inicio) = %s
        AND NOW() <= fecha_hora_fin::TIMESTAMP
        AND NOT EXISTS
        (SELECT registro_sesion.fk_id_sesion FROM registro_sesion WHERE sesion.id_sesion = registro_sesion.fk_id_sesion AND registro_sesion.fk_id_usuario = %s)
        ''', (lookup_record, credenciales[0]))
        records = c.fetchall()
        
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            count += 1

        conn.commit()
        conn.close()

    def search_dura():
        lookup_record = hora_entry.get()
        search.destroy()
        
        for record in my_tree.get_children():
            my_tree.delete(record)
        
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

        c = conn.cursor()

        c.execute('''
        SELECT * 
        FROM sesion 
        WHERE date_part('minute', fecha_hora_fin - fecha_hora_inicio) = %s
        AND NOW() <= fecha_hora_fin::TIMESTAMP
        AND NOT EXISTS
        (SELECT registro_sesion.fk_id_sesion FROM registro_sesion WHERE sesion.id_sesion = registro_sesion.fk_id_sesion AND registro_sesion.fk_id_usuario = %s)
        ''', (lookup_record, credenciales[0]))
        records = c.fetchall()
        
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            count += 1

        conn.commit()
        conn.close()

    def search_inst():
        lookup_record = hora_entry.get()
        search.destroy()
        
        for record in my_tree.get_children():
            my_tree.delete(record)
        
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1
        )

        c = conn.cursor()

        c.execute('''
        SELECT * 
        FROM sesion 
        WHERE fk_nombre_instructor = %s
        AND NOW() <= fecha_hora_fin::TIMESTAMP
        AND NOT EXISTS
        (SELECT registro_sesion.fk_id_sesion FROM registro_sesion WHERE sesion.id_sesion = registro_sesion.fk_id_sesion AND registro_sesion.fk_id_usuario = %s)
        ''', (lookup_record, credenciales[0]))
        records = c.fetchall()
        
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            count += 1

        conn.commit()
        conn.close()

    def search_cat():
        lookup_record = hora_entry.get()
        search.destroy()
        
        for record in my_tree.get_children():
            my_tree.delete(record)
        
        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1
        )

        c = conn.cursor()

        c.execute('''
        SELECT * 
        FROM sesion 
        WHERE categoria = %s
        AND NOW() <= fecha_hora_fin::TIMESTAMP
        AND NOT EXISTS
        (SELECT registro_sesion.fk_id_sesion FROM registro_sesion WHERE sesion.id_sesion = registro_sesion.fk_id_sesion AND registro_sesion.fk_id_usuario = %s)
        ''', (lookup_record, credenciales[0]))
        records = c.fetchall()
        
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            count += 1

        conn.commit()
        conn.close()

    pSesiones = Toplevel(root)
    pSesiones.title("Sesiones")

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    style.map('Treeview',
        background=[('selected', "#347083")])
    
    tree_frame = Frame(pSesiones)
    tree_frame.pack()

    botonSelec = Button(pSesiones, font="Helvetica 14", text="Agregar sesión", command=add_record)
    botonSelec.pack(pady=20)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack(pady=20)

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("ID", "Categoría", "Nombre del instructor", "Fecha y hora de inicio", "Fecha y hora de fin")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID", anchor=W, width=140)
    my_tree.column("Categoría", anchor=W, width=140)
    my_tree.column("Nombre del instructor", anchor=W, width=140)
    my_tree.column("Fecha y hora de inicio", anchor=W, width=140)
    my_tree.column("Fecha y hora de fin", anchor=W, width=140)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ID", text="ID", anchor=W)
    my_tree.heading("Categoría", text="Categoría", anchor=W)
    my_tree.heading("Nombre del instructor", text="Nombre del instructor", anchor=W)
    my_tree.heading("Fecha y hora de inicio", text="Fecha y hora de inicio", anchor=W)
    my_tree.heading("Fecha y hora de fin", text="Fecha y hora de fin", anchor=W)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    my_menu = Menu(pSesiones)
    pSesiones.config(menu=my_menu)

    search_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Busqueda", menu=search_menu)
    # Drop down menu
    search_menu.add_command(label="Busqueda", command=busqueda)
    search_menu.add_separator()
    search_menu.add_command(label="Deshacer", command=queryDatabase)

    queryDatabase()

def calendario():
    pCalendario = Toplevel(root)
    pCalendario.title("Calendario")
    cal = Calendar(pCalendario, font="Helvetica 18", selectmode='day', year=date.today().year, month=date.today().month, day=date.today().day)
    cal.pack(pady=20)

    def queryDatabase():
        for item in my_tree.get_children():
            my_tree.delete(item)

        conn = psycopg2.connect(
                host = host1,
                database = database1,
                user = user1,
                password = password1,
                port = port1

            )

        c = conn.cursor()

        c.execute('''
        SELECT fk_id_sesion, categoria, fk_nombre_instructor, fecha_hora_inicio, fecha_hora_fin FROM sesion
        INNER JOIN registro_sesion
        ON sesion.id_sesion = registro_sesion.fk_id_sesion
        WHERE registro_sesion.fk_id_usuario = %s AND fecha_hora_inicio::TIMESTAMP::DATE = %s
        ''', (credenciales[0], datetime.strptime(datetime.strptime(cal.get_date(), '%m/%d/%y').strftime('%Y-%m-%d'), '%Y-%m-%d').date())
        )
        data = c.fetchall()

        global count
        count = 0

        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            
            count += 1
        conn.commit()
        conn.close()

    def entrarSesion():
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        x = my_tree.selection()[0]
        my_tree.delete(x)

        conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

        c = conn.cursor()

        c.execute("DELETE from registro_sesion WHERE fk_id_usuario = %s AND fk_id_sesion = %s", (credenciales[0], values[0]))

        conn.commit()

        conn.close()

        queryDatabase()

        messagebox.showinfo("Sesion", "Has ingresado a la sesión")


    botonSelec = Button(pCalendario, font="Helvetica 14", text="Seleccionar fecha", command=queryDatabase)
    botonSelec.pack(pady=20)
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    style.map('Treeview',
        background=[('selected', "#347083")])
    
    tree_frame = Frame(pCalendario)
    tree_frame.pack(pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack(pady=20)

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("ID sesión", "Categoría", "Nombre del instructor", "Fecha y hora de inicio", "Fecha y hora de fin")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID sesión", anchor=W, width=140)
    my_tree.column("Categoría", anchor=W, width=140)
    my_tree.column("Nombre del instructor", anchor=W, width=140)
    my_tree.column("Fecha y hora de inicio", anchor=W, width=140)
    my_tree.column("Fecha y hora de fin", anchor=W, width=140)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ID sesión", text="ID sesión", anchor=W)
    my_tree.heading("Categoría", text="Categoría", anchor=W)
    my_tree.heading("Nombre del instructor", text="Nombre del instructor", anchor=W)
    my_tree.heading("Fecha y hora de inicio", text="Fecha y hora de inicio", anchor=W)
    my_tree.heading("Fecha y hora de fin", text="Fecha y hora de fin", anchor=W)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    botonEntrar = Button(pCalendario, font="Helvetica 14", text="Ingresar a sesión", command=entrarSesion)
    botonEntrar.pack(pady=5)
    queryDatabase()

def consulta():
    pConsultaPeso = Toplevel(root)
    headers = Label(pConsultaPeso, font=("Helvetica", 18))
    headers.config(text=f'{"Semana"}\t{"Peso"}\t{"Progreso"}')
    headers.pack()
    output_label = Label(pConsultaPeso, font=("Helvetica", 18))
    output_label.pack()
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''SELECT semana, peso_semanal, diferencia_sem FROM progreso WHERE fk_ID_usuario = %s''', (credenciales[0],))
    records = c.fetchall()

    output = ''

    for record in records:
        output_label.config(text=f'{output}\n{record[0]}\t{record[1]}\t{record[2]}')
        output = output_label['text']

def top10():
    pTop10 = Toplevel(root)
    pTop10.title("Top 10 sesiones que más usuarios tuvieron")

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    style.map('Treeview',
        background=[('selected', "#347083")])
    
    tree_frame = Frame(pTop10)
    tree_frame.pack(pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("Sesiones", "Cantidad de usuarios")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Sesiones", anchor=W, width=140)
    my_tree.column("Cantidad de usuarios", anchor=W, width=140)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Sesiones", text="Sesiones", anchor=W)
    my_tree.heading("Cantidad de usuarios", text="Cantidad de usuarios", anchor=W)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''SELECT fk_id_sesion, count(fk_id_sesion) as conteo 
    FROM registro_sesion 
    GROUP BY fk_id_sesion
    ORDER BY conteo desc
    LIMIT 10''')
    records = c.fetchall()

    output = ''
    
    global count
    count = 0
    
    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('oddrow',))
        
        count += 1
    conn.commit()
    conn.close()

def bitacora():
    pBitacora = Toplevel(root)
    pBitacora.title("Bitácora de operaciones en el sistema")

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    style.map('Treeview',
        background=[('selected', "#347083")])
    
    tree_frame = Frame(pBitacora)
    tree_frame.pack(pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("Usuario", "Accion", "Fecha", "Hora")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Usuario", anchor = W, width = 120)
    my_tree.column("Accion", ancho = W, width = 120)
    my_tree.column("Fecha", anchor = W, width = 120)
    my_tree.column("Hora", anchor = W, width = 120)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Usuario", text="Usuario", anchor=W)
    my_tree.heading("Accion", text="Accion", anchor=W)
    my_tree.heading("Fecha", text="Fecha", anchor=W)
    my_tree.heading("Hora", text="Hora", anchor=W)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute(''' select usuario, accion, to_char(tiempo, 'HH24:MI:SS') as hora, to_char(fecha, 'DD-HH-YYYY') as fecha 
    from log_admin 
    ''')
    records = c.fetchall()

    output = ''
    
    global count
    count = 0
    
    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
        
        count += 1
    conn.commit()
    conn.close()

def sesiones_categoria():
    pSesiones = Toplevel(root)
    pSesiones.title("Cantidad de sesiones y usuarios por categoria")

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    style.map('Treeview',
        background=[('selected', "#347083")])
    
    tree_frame = Frame(pSesiones)
    tree_frame.pack(pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("Sesiones", "Cantidad de usuarios", "Categoría")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Sesiones", anchor=W, width=140)
    my_tree.column("Cantidad de usuarios", anchor=W, width=140)
    my_tree.column("Categoría", anchor=W, width=140)
    

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Sesiones", text="Sesiones", anchor=W)
    my_tree.heading("Cantidad de usuarios", text="Cantidad de usuarios", anchor=W)
    my_tree.heading("Categoría", text="Categoría", anchor=W)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    my_tree.tag_configure('oddrow', background="white")
    conn = psycopg2.connect(
        host = host1,
        database = database1,
        user = user1,
        password = password1,
        port = port1

    )

    c = conn.cursor()

    c.execute('''
    SELECT SUM(sesionCount) as cuentaSesion, SUM(userCount) as cuentaUser, categoria
    FROM (
        SELECT      categoria , COUNT(*) sesionCount, 0 userCount
        FROM        sesion
        GROUP BY    categoria

        UNION

        SELECT      categoria, 0, COUNT(*)
        FROM        sesion
        JOIN        registro_sesion
        ON          sesion.id_sesion = registro_sesion.fk_id_sesion
        GROUP BY    categoria
    ) cuentas
    GROUP BY cuentas.categoria
    ''')
    records = c.fetchall()
    
    global count
    count = 0
    
    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('oddrow',))
        
        count += 1
    conn.commit()
    conn.close()

def top5_entrenadores():
    conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1
        )

    c = conn.cursor()

    c.execute('''SELECT fk_nombre_instructor, count(fk_nombre_instructor)as cuenta 
    FROM sesion
    GROUP BY fk_nombre_instructor
    ORDER BY cuenta desc
    LIMIT 5''')
    data = c.fetchall()

    pInstructor = Toplevel(root)
    pInstructor.title("Administrador de instructores")

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    style.map('Treeview',
        background=[('selected', "#347083")])
    
    tree_frame = Frame(pInstructor)
    tree_frame.pack(pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("Nombre de instructor", "Cantidad")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Nombre de instructor", anchor=W, width=140)
    my_tree.column("Cantidad", anchor=W, width=140)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Nombre de instructor", text="Nombre de instructor", anchor=W)
    my_tree.heading("Cantidad", text="Cantidad", anchor=W)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    global count
    count = 0

    for record in data:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('oddrow',))
        
        count += 1
    conn.commit()
    conn.close()


def cuen_diamante():
    conn = psycopg2.connect(
            host = host1,
            database = database1,
            user = user1,
            password = password1,
            port = port1

        )

    c = conn.cursor()

    c.execute('''SELECT tipo, count(tipo)as cuenta 
    FROM suscripcion
    WHERE extract(month from suscripcion.fecha_registro)=05 or extract(month from suscripcion.fecha_registro)=06 or 
    extract(month from suscripcion.fecha_registro)=07 or extract(month from suscripcion.fecha_registro)=08 or  
    extract(month from suscripcion.fecha_registro)=09 or  extract(month from suscripcion.fecha_registro)=10  and tipo = 'Diamante' 
    GROUP BY tipo''')
    data = c.fetchall()

    pInstructor = Toplevel(root)
    pInstructor.title("Administrador de instructores")

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    style.map('Treeview',
        background=[('selected', "#347083")])
    
    tree_frame = Frame(pInstructor)
    tree_frame.pack(pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("Tipo", "Cantidad")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Tipo", anchor=W, width=140)
    my_tree.column("Cantidad", anchor=W, width=140)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Tipo", text="Tipo", anchor=W)
    my_tree.heading("Cantidad", text="Cantidad", anchor=W)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    global count
    count = 0

    for record in data:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('oddrow',))
        
        count += 1
    conn.commit()
    conn.close()

def reportes():
    pReportes = Toplevel(root)
    headers = Label(pReportes, font=("Helvetica", 18))
    headers.config(text=f'{"Reportes"}')
    headers.pack()
    output_label = Label(pReportes, font=("Helvetica", 18))
    output_label.pack()
    root.geometry('100x100')
    top10_boton = Button(pReportes, text = "El top 10 de sesiones", font=("Helvetica", 18), command=top10)
    top10_boton.pack(padx=20)

    sesiones_button = Button(pReportes, text = "Sesiones por categoría", font = ("Helvetica", 18), command = sesiones_categoria)
    sesiones_button.pack(padx = 20)

    top5_button = Button(pReportes, text = "El top 5 entrenadores",font=("Helvetica", 18), command=top5_entrenadores)
    top5_button.pack(padx = 20)

    cuentas_diamante_button = Button(pReportes, text = "La cantidad de cuentas diamante",font=("Helvetica", 18), command=cuen_diamante)
    cuentas_diamante_button.pack(padx = 20)

    bitacora_button = Button(pReportes, text = "Bitacora",font=("Helvetica", 18), command=bitacora)
    bitacora_button.pack(padx = 20)
    

crearTablas()
#insertAdm()
#CreacionGrupos()
#crearPrivilegios()
#CreacionRoles()
crearTriggers()
crearVista()
Button(root, text='Login', command= login, font=("Helvetica", 24)).grid(row=0)
Button(root, text='Registro', command=signup, font=("Helvetica", 24)).grid(row=1)
Button(root, text='Admin', command=tiposAdmin, font=("Helvetica", 24)).grid(row=2)

root.mainloop()
