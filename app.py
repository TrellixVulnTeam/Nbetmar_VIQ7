from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import bd

app = Flask(__name__)
app.secret_key =b'clave'

global user
a = ["<div class='box has-text-primary'>esto se genero por feo</div>", "es a", 'recarga1.html']
b = ["<div class='card is-primary'>esto se genero por horrible</div>", "es b"]




@app.route('/')
def home():
    """Home de la aplicacion"""
    flash('Bienvenido al home')
    flash('Disfruta tu estadia')
    return render_template('index.html', navbar='navbarout.html', cont=b, contenido='home.html', vendedor='admin', reca='recas', banca='banca', bancadmin=1, userdat='')




@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """pagina de registro para usuarios nuevos"""
    vendedores = bd.vendedores()
    if request.method == 'POST': 
        datos = []
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['password']
        celular = request.form['tlf']
        vendedor = request.form['vendedor']

        datos.extend([nombre,correo,password,vendedor,celular])
        try:
            bd.crear(datos)
            flash('Registro Correcto')
            return redirect(url_for('home'))
        except:
            flash('No se pudo registrar')
            return render_template('index.html', navbar='navbarout.html', cont=a, contenido='registro.html', vendedores=vendedores, vendedor='admin', reca='recas', banca='banca', bancadmin=1, userdat='')
    else:    
        flash('Bienvenido al registro')
        return render_template('index.html', navbar='navbarout.html', cont=a, contenido='registro.html', vendedores=vendedores, vendedor='admin', reca='recas', banca='banca', bancadmin=1, userdat='')



@app.route('/login', methods=['GET', 'POST'])
def login():
    """Pagina de login a la plataforma para usuarios registrados"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        if bd.existecorreo(nombre):
            if bd.existepassword(password):
                user = bd.leer(nombre)
                return redirect(url_for('user', user=user[1]))

            else:
                flash('Error en Password')
                return redirect(request.path)
        else:
            flash('Error en Correo')
            return redirect(request.path)
    else:
        flash('Ingresa a la Plataforma')
        return render_template('index.html', navbar='navbarout.html', cont=a, contenido='login.html', vendedor='admin', reca='recas', banca='banca', bancadmin=1, userdat='')



@app.route('/<user>', methods=['GET', 'POST'])
def user(user):
    panelv = '<a class="navbar-item" href="/'+user+'/clientes">Clientes</a><a class="navbar-item" href="/'+user+'/metricas">Metricas</a>'
    panelu = '<a class="navbar-item" href="/'+user+'/metricas">Metricas</a>'
    global reca
    reca = bd.leertodoreca(1)
    reca = bd.tresillo(reca,3)
    userdat = bd.leeruser(user)
    if userdat == None:
        pass
    else:
        global vendedor
        vendedor = bd.leervend(userdat[8])
        global banca
        banca = bd.leer_banca(userdat[8])
        global bancadmin
        bancadmin = bd.leer_banca(1)
        global servi
        servi = bd.leertodoservi(userdat[8])
        servi = bd.tresillo(servi,3)
        global nivel
        nivel = userdat[7]
        global listareca
        listareca = bd.ListaRecargas(userdat[0])
        global listacuentas
        listacuentas = bd.ListaCuentas(userdat[0])

    if request.method == 'POST':
        user = user
        solicitudes = request.form['solicitud']
        ref = request.form['referencia']
        vend = request.form['vendedor']
        formulario = request.form
        if formulario['action'] == 'recarga':
            recarganeta = request.form['recarganeta']
            bd.recarga(userdat[0], solicitudes, vend, ref, recarganeta)
            flash('Solicitud de recarga enviada')
            return redirect(url_for('user', user=user))
        elif formulario['action'] == 'servicio':
            solicitudes = solicitudes.split(',')
            bd.cuentas(userdat[0], solicitudes[1], solicitudes[0], solicitudes[2], solicitudes[3], vend, ref)
            flash('solicitud de cuenta enviada')
            return redirect(url_for('user', user=user))

    else:
        userdat = bd.leeruser(user)
        if userdat == None:
            pass
        else:
            nivel = userdat[7]
            if nivel == 3:
                flash('Bienvenido' + ' '+ user)
                return render_template('index.html', navbar='navbarin.html', cont=a, contenido='user.html', user=user, userdat=userdat, tabla='vendedor.html', servi=servi, reca=reca, listareca=listareca, listacuenta=listacuentas, vendedor=vendedor, banca=banca, bancadmin=bancadmin, PanelClient=panelu)

            if nivel == 2:
                flash('Bienvenido' + ' '+'vendedor'+' '+user)
                return render_template('index.html', navbar='navbarin.html', cont=a, contenido='user.html', user=user, userdat=userdat, tabla='vendedor.html', servi=servi, reca=reca, listareca=listareca, listacuenta=listacuentas, vendedor=vendedor, banca=banca, bancadmin=bancadmin, PanelClient=panelv)

            if nivel == 1:
                flash('Bienvenido' + ' '+'administrador'+' '+user)
                return render_template('index.html', navbar='navbarin.html', cont=a, contenido='user.html', user=user, userdat=userdat, tabla='admin.html', servi=servi, reca=reca, vendedor=vendedor, banca=banca, bancadmin=bancadmin, PanelClient=panelv)
    

@app.route('/<user>/clientes', methods=['GET', 'POST'])
def UserClients(user):
    userdat = bd.leeruser(user)
    nivel = userdat[7]
    global listacuenta
    listacuenta = bd.ListaCuentasvend(userdat[0])
    global listareca
    listareca = bd.ListaRecargasvend(userdat[0])
    global reca
    reca = bd.leertodoreca(1)
    reca = bd.tresillo(reca,3)
    global banca
    banca = bd.leer_banca(userdat[8])
    global bancadmin
    bancadmin = bd.leer_banca(1)
    panelv = '<a class="navbar-item" href="/'+user+'/clientes">Clientes</a><a class="navbar-item" href="/'+user+'/metricas">Metricas</a>'
    vendedor = bd.leervend(userdat[8])
    nivel = userdat[7]
    if request.method =='POST':
        formulario = request.form
        if formulario['action'] == 'aprobar_cuenta':
            aprobado = request.form['por_aprobar']
            aprobado = aprobado.split(',')
            bd.delcuent(aprobado[1].strip(), aprobado[0].strip())
            return redirect (request.path)
        else:
            aprobado = request.form['por_aprobar']
            aprobado = aprobado.split(',')
            bd.delrec(aprobado[1].strip(), aprobado[0].strip())
            return redirect(request.path)
    else:
        if nivel == 1:
            flash('bienvenido')
            return render_template('index.html', navbar='navbarin.html', cont=a, contenido='clientes.html', user=user, userdat=userdat, PanelClient=panelv, vendedor=vendedor, reca=reca, banca=banca, bancadmin=bancadmin, listacuenta=listacuenta, listareca = listareca, listas="recarga1.html")
        elif nivel == 2:
            flash('bienvenido')
            return render_template('index.html', navbar='navbarin.html', cont=a, contenido='clientes.html', user=user, userdat=userdat, PanelClient=panelv, vendedor=vendedor, reca=reca, banca=banca, bancadmin=bancadmin, listacuenta=listacuenta, listareca = listareca, listas="cuenta1.html")
        

@app.route('/<user>/metricas', methods=['GET', 'POST'])
def UserMetric(user):
    userdat = bd.leeruser(user)
    nivel = userdat[7]
    global listacuenta
    listacuenta = bd.ListaCuentasvend(userdat[0])
    global listareca
    listareca = bd.ListaRecargasvend(userdat[0])
    global reca
    reca = bd.leertodoreca(1)
    reca = bd.tresillo(reca,3)
    global banca
    banca = bd.leer_banca(userdat[8])
    global bancadmin
    bancadmin = bd.leer_banca(1)
    panelv = '<a class="navbar-item" href="/'+user+'/clientes">Clientes</a><a class="navbar-item" href="/'+user+'/metricas">Metricas</a>'
    panelu = '<a class="navbar-item" href="/'+user+'/metricas">Metricas</a>'
    vendedor = bd.leervend(userdat[8])
    nivel = userdat[7]
    if nivel == 1:
        flash('estadisticas del Administrador')
        return render_template('index.html', navbar='navbarin.html', cont=a, contenido='metricas.html', user=user, userdat=userdat, PanelClient=panelv, vendedor=vendedor, reca=reca, banca=banca, bancadmin=bancadmin, listacuenta=listacuenta, listareca = listareca, listas="recarga1.html")
    elif nivel == 2:
        flash('Estadisticas del vendedor')
        return render_template('index.html', navbar='navbarin.html', cont=a, contenido='metricas.html', user=user, userdat=userdat, PanelClient=panelv, vendedor=vendedor, reca=reca, banca=banca, bancadmin=bancadmin, listacuenta=listacuenta, listareca = listareca, listas="cuenta1.html")
    elif nivel == 3:
        flash('Estadisticas del usuario')
        return render_template('index.html', navbar='navbarin.html', cont=a, contenido='metricas.html', user=user, userdat=userdat, PanelClient=panelu, vendedor=vendedor, reca=reca, banca=banca, bancadmin=bancadmin, listacuenta=listacuenta, listareca = listareca, listas="cuenta1.html")


@app.route('/api/', methods=['GET', 'POST'])
def api():
    dato = request.args.get('dato')
    vendedorident = request.args.get('ident')
    if dato == 'ListaCuentasvend':
        keysN = ['id', 'nombre', 'time', 'orden', 'cantidad', 'status',
                'fcorte', 'vendedor', 'dolar', 'bolivares', 'banco', 'referencia']
        cuentasN =  bd.ListaCuentasvend(vendedorident)
        res = []
        for cuent in cuentasN:
            res.append(dict(zip(keysN, cuent)))
        return jsonify(res)
    
    if dato == 'ListaRecargasvend':
        keysN = ['id', 'nombre', 'time', 'orden', 'status', 'vendedor', 'banco', 'referencia', 'montoneto']
        recargasN =  bd.ListaRecargasvend(1)
        res = []
        for rec in recargasN:
            res.append(dict(zip(keysN, rec)))
        return jsonify(res)
        
            




app.run(host='0.0.0.0', port=5000, debug=True)
