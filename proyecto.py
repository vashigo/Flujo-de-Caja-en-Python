import sys #lib control de archivos
import sqlite3 #lib de base de datos SQLLITE
import os as Os #lib control de archivos
import os.path as path #lib leer archivos
import tkinter as tk #lib tkinter
from tkinter import messagebox #lib messagebox de tkinter
import numpy as np #numpy
import webbrowser #lib para manejar el link

Ubicacion_bd = Os.getcwd()+"\prueba.db" #variable de la ruta de base de datos
#variables de control de ventanas de tkinter para abrir y cerrarlas libremente
ventana=0
ventana_Act = 0
ventana_Pas = 0
ventana_Pat = 0
ventana_Res = 0
ventana_autentificacion = 0
#llevar control de los id
contID=0
#llevar control para eliminar cuentas correctamente
contCuentaPas = 0
contCuentaAct = 0
contCuentaPat = 0
usuarioPasw = "sppc" #variable de la contraseña

#ventana de bienvenida
def ventana_Principal():
    global ventana, ventana_Act, contID, ventana_Res
    #crea ventana y se le hacen configuraciones
    ventana=tk.Tk()
    ventana.title("Bienvenido")
    ventana.configure(background="dark turquoise")
    ventana.geometry("550x350")
    ventana.resizable(width=False, height=False)#no se podra grandar
    ventana.attributes("-topmost", True) #Siempre este la ventana encima de otras
    fondo = tk.PhotoImage(file="fondo.png")#carga imagen
    lblFondo = tk.Label(ventana,image = fondo).place(x=0,y=0) #fonde
    TEXT1 = tk.Label(ventana,text=" Bienvenido al programa de Flujo de Caja ", bg="black", fg="white",font='Helvetica 20 bold')
    TEXT1.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    crea_basededatos()#llamado a la funcion que crea el arcivo de base de datos
    boton2 = tk.Button(ventana,text="Iniciar",command=ventana_autentificacion,font='Helvetica 16 bold') #boton iniciar
    boton2.pack(padx=5,pady=50,ipadx=5,ipady=5,side=tk.TOP)
    boton3 = tk.Button(ventana,text="Cerrar",command=ventana.destroy) #boton cerrar
    boton3.pack(padx=5,pady=5,ipadx=5,ipady=5,side=tk.BOTTOM)
    TEXT2 = tk.Label(ventana,text=" By: ", bg="black", fg="maroon2",font='Helvetica 16 bold')
    TEXT2.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X,side=tk.BOTTOM,before=boton3)
    TEXT3 = tk.Label(ventana,text=" Andres Vasquez ", bg="black", fg="maroon2",font='Helvetica 16 bold')
    TEXT3.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X,side=tk.BOTTOM,before=TEXT2)
    center(ventana)#centrar ventana
    ventana.mainloop()

def ventana_Activos():
    global ventana, ventana_Act, ventana_autentificacion, contCuentaAct
    contCuentaAct = 0
    def agrega():
        global contID, contCuentaAct
        if not(is_number(valor.get())):
            messagebox.showerror(message="Valor incorrecto, por favor ingrese el numero correctamente sin comas o otros caracteres, ejemplo(123.5 o 123)", title="Error")
        elif len(cuenta.get())==0:
            messagebox.showerror(message="No tiene nada en cuenta, por favor ingrese la cuenta", title="Error")
        else:   
            listCuentas.insert(tk.END,cuenta.get())
            listValores.insert(tk.END,valor.get())
            contID+=1
            contCuentaAct+=1
            AgregarDatosBD(contID,cuenta.get(),valor.get(),"activo")
            caja1.delete(0,tk.END) #limpia las cajas
            caja2.delete(0,tk.END) #limpia las cajas
            
    def elimina():
        global contID, contCuentaAct
        if contCuentaAct > 0:
            listCuentas.delete(tk.END)
            listValores.delete(tk.END)
            EliminarDatosBD(contID)
            contCuentaAct-=1
            contID-=1
        else:
            messagebox.showerror(message="No hay cuenta por eliminar!", title="Error")
    def ventanas():
        global ventana_Act, ventana_Pas
        if ventana_Pas == 0:
            ventana_Pasivos()
        else:
            ventana_Pas.deiconify()
            ventana_Act.withdraw()

    ventana_autentificacion.withdraw()
    ventana_Act = tk.Toplevel()
    ventana_Act.title("Cuentas Activo")
    ventana_Act.attributes("-topmost", True)#Siempre este la ventana encima de otras
    fondo = tk.PhotoImage(file="fondo.png")
    lblFondo = tk.Label(ventana_Act,image = fondo).place(x=0,y=0)
    
    TEXT1 = tk.Label(ventana_Act,text=" Añada Todas Las Cuentas de Activos ", bg="black", fg="white",font='Helvetica 16 bold')
    TEXT1.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    
    cuenta = tk.StringVar(ventana_Act)
    tk.Label(ventana_Act, text = "Cuenta:").pack(padx=5,pady=5,ipadx=5,ipady=5)
    caja1 = tk.Entry(ventana_Act, textvariable=cuenta,justify=tk.CENTER)
    caja1.pack(padx=5,pady=5,ipadx=50,ipady=5)

    TEXT = tk.Label(ventana_Act,text=" si no esta seguro de la cuenta a la que pertenece\n entonces consulte en el siguiente link: ", bg="black", fg="white",font='Helvetica 8 bold')
    TEXT.pack(after=caja1)
    lbl = tk.Label(ventana_Act, text=r"https://puc.com.co/cuentas/", fg="blue", cursor="hand2", bg="white",font='Helvetica 8 bold')
    lbl.pack()
    lbl.bind("<Button-1>", callback)

    valor = tk.StringVar(ventana_Act)
    tk.Label(ventana_Act, text = "Valor:").pack(padx=5,pady=5,ipadx=5,ipady=5)
    caja2 = tk.Entry(ventana_Act, textvariable=valor,justify=tk.CENTER)
    caja2.pack(padx=5,pady=5,ipadx=40,ipady=5)

    listCuentas = tk.Listbox(ventana_Act,width=40,height=15,relief="solid",font="Times 10",justify=tk.CENTER)
    listValores = tk.Listbox(ventana_Act,width=20,height=15, relief="solid",font="Times 10",justify=tk.CENTER)
    listCuentas.pack(padx=5,side=tk.LEFT,fill=tk.X,expand=True)
    listValores.pack(side=tk.LEFT,fill=tk.X,expand=True)
    
    botonAgregar = tk.Button(ventana_Act, text= "Eliminar Cuenta", command=elimina,font='Helvetica 16 bold',bg="maroon2")
    botonAgregar.pack(padx=5,pady=2,ipadx=40,ipady=0,before=listCuentas,side=tk.TOP)
    
    botonElimina = tk.Button(ventana_Act, text= "Agregar Cuenta", command=agrega,font='Helvetica 16 bold',bg= "dark turquoise")
    botonElimina.pack(padx=5,pady=2,ipadx=40,ipady=0,before=botonAgregar,side=tk.TOP)

    botonPasivos = tk.Button(ventana_Act, text= "Pasar a Pasivos", command=ventanas,font='Helvetica 16 bold',bg= "gold")
    botonPasivos.pack(padx=5,pady=2,ipadx=40,ipady=0,after=botonAgregar,side=tk.TOP)
    
    center(ventana_Act)
    ventana_Act.mainloop()
    

def ventana_Pasivos():
    global ventana, ventana_Act, ventana_Pas, contID, contCuentaPas
    contCuentaPas = 0
    def agrega():
        global contID, contCuentaPas
        if not(is_number(valor.get())):
            messagebox.showerror(message="Valor incorrecto, por favor ingrese el numero correctamente sin comas o otros caracteres, ejemplo(123.5 o 123)", title="Error")
        elif len(cuenta.get())==0:
            messagebox.showerror(message="No tiene nada en cuenta, por favor ingrese la cuenta", title="Error")
        else:   
            listCuentas.insert(tk.END,cuenta.get())
            listValores.insert(tk.END,valor.get())
            contID+=1
            contCuentaPas+=1
            AgregarDatosBD(contID,cuenta.get(),valor.get(),"pasivo")
            caja1.delete(0,tk.END) #limpia las cajas
            caja2.delete(0,tk.END) #limpia las cajas
    def elimina():
        global contID, contCuentaPas
        if contCuentaPas > 0:
            listCuentas.delete(tk.END)
            listValores.delete(tk.END)
            EliminarDatosBD(contID)
            contCuentaPas-=1
            contID-=1
        else:
            messagebox.showerror(message="No hay cuenta por eliminar!", title="Error")
    def ventanas(num):
        global ventana_Act, ventana_Pas, ventana_Pat
        if num==1:
            if ventana_Pat==0:
                ventana_Patrimonio()
            else:
                ventana_Pat.deiconify()
                ventana_Pas.withdraw()
        elif num==0:
            ventana_Act.deiconify()
            ventana_Pas.withdraw()
                
    ventana_Act.withdraw()
    ventana_Pas = tk.Toplevel()
    ventana_Pas.title("Cuentas Pasivo")
    ventana_Pas.attributes("-topmost", True)#Siempre este la ventana encima de otras
    fondo = tk.PhotoImage(file="fondo.png")
    lblFondo = tk.Label(ventana_Pas,image = fondo).place(x=0,y=0)

    TEXT1 = tk.Label(ventana_Pas,text=" Añada Todas Las Cuentas de Pasivos ", bg="black", fg="white", font='Helvetica 16 bold')
    TEXT1.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    
    cuenta = tk.StringVar(ventana_Pas)
    tk.Label(ventana_Pas, text = "Cuenta:").pack(padx=5,pady=5,ipadx=5,ipady=5)
    caja1 = tk.Entry(ventana_Pas, textvariable=cuenta,justify=tk.CENTER)
    caja1.pack(padx=5,pady=5,ipadx=50,ipady=5)

    TEXT = tk.Label(ventana_Pas,text=" si no esta seguro de la cuenta a la que pertenece\n entonces consulte en el siguiente link: ", bg="black", fg="white",font='Helvetica 8 bold')
    TEXT.pack(after=caja1)
    lbl = tk.Label(ventana_Pas, text=r"https://puc.com.co/cuentas/", fg="blue", cursor="hand2", bg="white",font='Helvetica 8 bold')
    lbl.pack()
    lbl.bind("<Button-1>", callback)    

    valor = tk.StringVar(ventana_Pas)
    tk.Label(ventana_Pas, text = "Valor:").pack(padx=5,pady=5,ipadx=5,ipady=5)
    caja2 = tk.Entry(ventana_Pas, textvariable=valor,justify=tk.CENTER)
    caja2.pack(padx=5,pady=5,ipadx=40,ipady=5)

    listCuentas = tk.Listbox(ventana_Pas,width=40,height=15,relief="solid",font="Times 10",justify=tk.CENTER)
    listValores = tk.Listbox(ventana_Pas,width=20,height=15,relief="solid",font="Times 10",justify=tk.CENTER)
    listCuentas.pack(side=tk.LEFT,fill=tk.X,expand=True)
    listValores.pack(side=tk.LEFT,fill=tk.X,expand=True)
    
    botonAgregar = tk.Button(ventana_Pas, text= "Eliminar Cuenta", command=elimina,font='Helvetica 16 bold',bg="maroon2")
    botonAgregar.pack(padx=5,pady=2,ipadx=40,ipady=0,before=listCuentas,side=tk.TOP)
    
    botonElimina = tk.Button(ventana_Pas, text= "Agregar Cuenta", command=agrega,font='Helvetica 16 bold',bg="dark turquoise")
    botonElimina.pack(padx=5,pady=2,ipadx=40,ipady=0,before=botonAgregar,side=tk.TOP) 

    botonPatrimonios = tk.Button(ventana_Pas, text= "pasar a\n Patrimonios", command=lambda: ventanas(1),font='Helvetica 16 bold',bg="gold")
    botonPatrimonios.pack(after=botonAgregar,side=tk.RIGHT)

    botonActivos = tk.Button(ventana_Pas, text= "Devolverse a\n Activos", command=lambda: ventanas(0),font='Helvetica 16 bold',bg="gold")
    botonActivos.pack(after=botonAgregar,side=tk.LEFT)
    
    center(ventana_Pas)
    ventana_Pas.mainloop()

def ventana_Patrimonio():
    global ventana, ventana_Act, ventana_Pas, ventana_Pat, contID, contCuentaPat
    contCuentaPat = 0
    def agrega():
        global contID, contCuentaPat
        if not(is_number(valor.get())):
            messagebox.showerror(message="Valor incorrecto, por favor ingrese el numero correctamente sin comas o otros caracteres, ejemplo(123.5 o 123)", title="Error")
        elif len(cuenta.get())==0:
            messagebox.showerror(message="No tiene nada en cuenta, por favor ingrese la cuenta", title="Error")
        else:   
            listCuentas.insert(tk.END,cuenta.get())
            listValores.insert(tk.END,valor.get())
            contID+=1
            contCuentaPat+=1
            AgregarDatosBD(contID,cuenta.get(),valor.get(),"patrimonio")
            caja1.delete(0,tk.END) #limpia las cajas
            caja2.delete(0,tk.END) #limpia las cajas
    def elimina():
        global contID, contCuentaPat
        if contCuentaPat > 0 :
            listCuentas.delete(tk.END)
            listValores.delete(tk.END)
            EliminarDatosBD(contID)
            contID-=1
            contCuentaPat-=1
        else:
            messagebox.showerror(message="No hay cuenta por eliminar!", title="Error")
    def ventanas(num):
        global ventana_Act, ventana_Pas, ventana_Pat
        if num==1:
            ventana_Resultados()
        elif num==0:
            ventana_Pas.deiconify()
            ventana_Pat.withdraw()
    ventana_Pas.withdraw()
    ventana_Pat = tk.Toplevel()
    ventana_Pat.title("Cuentas Patrimonio")
    fondo = tk.PhotoImage(file="fondo.png")
    lblFondo = tk.Label(ventana_Pat,image = fondo).place(x=0,y=0)
    ventana_Pat.attributes("-topmost", True)#Siempre este la ventana encima de otras
    
    TEXT1 = tk.Label(ventana_Pat,text=" Añada Todas Las Cuentas de Patrimonio ", bg="black", fg="white", font='Helvetica 16 bold')
    TEXT1.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    
    cuenta = tk.StringVar(ventana_Pat)
    tk.Label(ventana_Pat, text = "Cuenta:").pack(padx=5,pady=5,ipadx=5,ipady=5)
    caja1 = tk.Entry(ventana_Pat, textvariable=cuenta,justify=tk.CENTER)
    caja1.pack(padx=5,pady=5,ipadx=50,ipady=5)
    
    TEXT = tk.Label(ventana_Pat,text=" si no esta seguro de la cuenta a la que pertenece\n entonces consulte en el siguiente link: ", bg="black", fg="white",font='Helvetica 8 bold')
    TEXT.pack(after=caja1)
    lbl = tk.Label(ventana_Pat, text=r"https://puc.com.co/cuentas/", fg="blue", cursor="hand2", bg="white",font='Helvetica 8 bold')
    lbl.pack()
    lbl.bind("<Button-1>", callback)    

    valor = tk.StringVar(ventana_Pat)
    tk.Label(ventana_Pat, text = "Valor:").pack(padx=5,pady=5,ipadx=5,ipady=5)
    caja2 = tk.Entry(ventana_Pat, textvariable=valor,justify=tk.CENTER)
    caja2.pack(padx=5,pady=5,ipadx=40,ipady=5)

    listCuentas = tk.Listbox(ventana_Pat,width=40,height=15,relief="solid",font="Times 10",justify=tk.CENTER)
    listValores = tk.Listbox(ventana_Pat,width=20,height=15,relief="solid",font="Times 10",justify=tk.CENTER)
    listCuentas.pack(side=tk.LEFT,fill=tk.X,expand=True)
    listValores.pack(side=tk.LEFT,fill=tk.X,expand=True)
    
    botonAgregar = tk.Button(ventana_Pat, text= "Eliminar Cuenta", command=elimina,font='Helvetica 16 bold',bg="maroon2")
    botonAgregar.pack(padx=5,pady=2,ipadx=40,ipady=0,before=listCuentas,side=tk.TOP)
    
    botonElimina = tk.Button(ventana_Pat, text= "Agregar Cuenta", command=agrega,font='Helvetica 16 bold',bg="dark turquoise")
    botonElimina.pack(padx=5,pady=2,ipadx=40,ipady=0,before=botonAgregar,side=tk.TOP)

    botonPasivo = tk.Button(ventana_Pat, text= "Devolverse a\n Pasivo", command=lambda: ventanas(0),font='Helvetica 16 bold',bg="gold")
    botonPasivo.pack(after=botonAgregar,side=tk.LEFT)
    
    botonFlujoCaja = tk.Button(ventana_Pat, text= "Realizar Flujo\n de Caja", command=lambda: ventanas(1),font='Helvetica 16 bold',bg="gold")
    botonFlujoCaja.pack(after=botonAgregar,side=tk.RIGHT)
    
    center(ventana_Pat)
    ventana_Pat.mainloop()

def ventana_Resultados():
    global ventana, ventana_Act, ventana_Pas, ventana_Pat, contID, ventana_Res
    def cerrarCaja():
        if (activos==pasYpat):
             messagebox.showinfo(message="Caja cerrada con Exito!", title="Felicitaciones")
        else:
            messagebox.showinfo(message="Su caja no cerro adecuadamente por una diferencia de: "+str(abs(activos-pasYpat)), title="Error")
    def reiniciarDatos():
        global ventana,ventana_Act,ventana_Pas,ventana_Pat,ventana_Res,ventana_autentificacion,contID,contCuentaPas,contCuentaAct,contCuentaPat
        #se destruye las ventanas en memoria osea todas
        destroyven()
        #pongo ventanas en 0
        ventana_Act,ventana_Pas,ventana_Pat,ventana_Res,ventana_autentificacion=0,0,0,0,0
        #reiniciar variables
        contID,contCuentaPas,contCuentaAct,contCuentaPat=0,0,0,0
        #reinicializar base de datos
        crea_basededatos()
        #volver al principio
        ventana.deiconify()
        center(ventana)
        
 
    SUMATORIA_Activos = 0
    SUMATORIA_Pasivos = 0
    SUMATORIA_Patrimonio = 0
    TotalCuentasAct=0
    TotalCuentasPas=0
    TotalCuentasPat=0
    
    ventana_Pat.withdraw()
    ventana_Res = tk.Toplevel()
    ventana_Res.title("Flujo de caja")
    ventana_Res.resizable(width=False, height=False)
    ventana_Res.attributes("-topmost", True)#Siempre este la ventana encima de otras

    con = sqlite3.connect(Ubicacion_bd)
    cursor = con.cursor()
    #poner todos los ACTIVOS
    cursor.execute("SELECT ID, CUENTA, VALOR FROM CUENTAS where TIPO='activo'")
    cont=1
    tk.Label(ventana_Res, text="ACTIVOS",font='Helvetica 16 bold').grid(pady=1,padx=10, row=0, column=0, sticky=tk.W)
    for i in cursor:
        tk.Label(ventana_Res, text=i[1]).grid(pady=1,padx=1,ipadx=20,row=cont, column=0,sticky=tk.W)
        tk.Label(ventana_Res, text=i[2]).grid(pady=1,padx=1,ipadx=20,row=cont, column=1,sticky=tk.W)
        #usamos numpy para la sumatoria
        SUMATORIA_Activos=np.add(SUMATORIA_Activos, i[2])
        cont+=1
        TotalCuentasAct+=1
    #poner todos los pasivos
    cursor.execute("SELECT ID, CUENTA, VALOR FROM CUENTAS where TIPO='pasivo'")
    cont=1
    tk.Label(ventana_Res, text="PASIVOS",font='Helvetica 16 bold').grid(pady=1,padx=10, row=0, column=2, sticky=tk.W)
    for i in cursor:
        tk.Label(ventana_Res, text=i[1]).grid(pady=1,padx=1,ipadx=20,row=cont, column=2,sticky=tk.W)
        tk.Label(ventana_Res, text=i[2]).grid(pady=1,padx=1,ipadx=20,row=cont, column=3,sticky=tk.W)
        #usamos numpy para la sumatoria
        SUMATORIA_Pasivos=np.add(SUMATORIA_Pasivos, i[2])
        cont+=1
        TotalCuentasPas+=1

    #poner todos los patrimonios
    cursor.execute("SELECT ID, CUENTA, VALOR FROM CUENTAS where TIPO='patrimonio'")
    TotalCuentasPat = TotalCuentasPas + 1
    tk.Label(ventana_Res, text="PATRIMONIO",font='Helvetica 16 bold').grid(pady=1,padx=10, row=TotalCuentasPat, column=2, sticky=tk.W)
    TotalCuentasPat+=1
    for i in cursor:
        tk.Label(ventana_Res, text=i[1]).grid(pady=1,padx=1,ipadx=20,row=TotalCuentasPat, column=2,sticky=tk.W)
        tk.Label(ventana_Res, text=i[2]).grid(pady=1,padx=1,ipadx=20,row=TotalCuentasPat, column=3,sticky=tk.W)
        #usamos numpy para la sumatoria
        SUMATORIA_Patrimonio=np.add(SUMATORIA_Patrimonio, i[2])
        TotalCuentasPat+=1
    
    #Calcular la posicion del total para ponerlo
    if (TotalCuentasAct > TotalCuentasPas+TotalCuentasPat):
        posTotales=TotalCuentasAct+2
    else:
        posTotales = TotalCuentasPas+TotalCuentasPat+2
    #poner Total activos
    tk.Label(ventana_Res, text="TOTAL ACTIVO = ",font='Helvetica 16 bold').grid(pady=1,padx=10, row=posTotales, column=0, sticky=tk.W)
    tk.Label(ventana_Res, text=SUMATORIA_Activos).grid(pady=1,padx=10, row=posTotales, column=1, sticky=tk.W)
    #poner Total pasivos + patrimonio
    tk.Label(ventana_Res, text="TOTAL PASIVOS Y PATRIMONIO = ",font='Helvetica 16 bold').grid(pady=1,padx=10, row=posTotales, column=2, sticky=tk.W)
    tk.Label(ventana_Res, text=SUMATORIA_Pasivos+SUMATORIA_Patrimonio).grid(pady=1,padx=10, row=posTotales, column=3, sticky=tk.W)
    #boton de comprobación
    activos= SUMATORIA_Activos
    pasYpat= SUMATORIA_Pasivos+SUMATORIA_Patrimonio
    
    botonCerrarCaja = tk.Button(ventana_Res, text= "Cerrar Caja", command=cerrarCaja,fg="red",font='Helvetica 12 bold')
    botonCerrarCaja.grid(padx=5,pady=10,ipadx=40,ipady=5,row=posTotales+2,column=0)

    botonCerrarCaja = tk.Button(ventana_Res, text= "Salir", command=reiniciarDatos,fg="red",font='Helvetica 12 bold')
    botonCerrarCaja.grid(padx=5,pady=10,ipadx=40,ipady=5,row=posTotales+2,column=3)

    con.close()
    center(ventana_Res)
    ventana_Res.mainloop()

def ventana_autentificacion():
    global ventana, usuarioPasw, ventana_autentificacion
    def verifica():
        global usuarioPasw
        if (pasw.get() == usuarioPasw):
            ventana_Activos()
        else:
            messagebox.showinfo(message="Contraseña Incorrecta!", title="Error")
            caja1.delete(0,tk.END) #limpia la caja
    ventana.withdraw()
    ventana_autentificacion = tk.Toplevel()
    ventana_autentificacion.title("Flujo de caja")
    ventana_autentificacion.resizable(width=False, height=False)
    ventana_autentificacion.attributes("-topmost", True)#Siempre este la ventana encima de otras

    fondo = tk.PhotoImage(file="fondo.png")
    lblFondo = tk.Label(ventana_autentificacion,image = fondo).place(x=0,y=0)
    TEXT1 = tk.Label(ventana_autentificacion,text="Ingrese la contraseña para continuar", bg="black", fg="white",font='Helvetica 20 bold')
    TEXT1.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    
    pasw = tk.StringVar(ventana_autentificacion)
    tk.Label(ventana_autentificacion, text = "Contraseña:").pack(padx=5,pady=5,ipadx=5,ipady=5)
    caja1 = tk.Entry(ventana_autentificacion, textvariable=pasw,justify=tk.CENTER, show="*")
    caja1.pack(padx=5,pady=5,ipadx=50,ipady=5)

    botonVerifica = tk.Button(ventana_autentificacion, text= "INGRESAR", command=verifica,font='Helvetica 16 bold',bg="maroon2")
    botonVerifica.pack(padx=5,pady=2,ipadx=40,ipady=0,side=tk.TOP)
    
    center(ventana_autentificacion)
    ventana_autentificacion.mainloop()

#funcion que crea el link
def callback(event):
    webbrowser.open_new(event.widget.cget("text"))

#verifica si efectivamente una cadena puede ser un float
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
#destruye todas las ventanas
def destroyven():
    global ventana_Act,ventana_Pas,ventana_Pat,ventana_Res,ventana_autentificacion
    ventana_Act.destroy()
    ventana_Pas.destroy()
    ventana_Pat.destroy()
    ventana_Res.destroy()
    ventana_autentificacion.destroy()
    

#agrega el id, cuenta, valor y tipo a la tabla CUENTAS dentro de la base de datos
def AgregarDatosBD(ID,cuenta,valor,tipo):
    con = sqlite3.connect(Ubicacion_bd)
    cursor = con.cursor()
    #se forma la cadena para insertar los datos correctamente
    valores= "VALUES ("+str(ID)+","+"'"+cuenta+"'"+","+str(valor)+","+"'"+tipo+"'"+")" 
    cursor.execute("INSERT INTO CUENTAS (ID, CUENTA, VALOR, TIPO)\
    	"+valores)
    con.commit()
    con.close()

#elimina el dato dentro de la base de datos que sea igual al ID
def EliminarDatosBD(ID):
    con = sqlite3.connect(Ubicacion_bd)
    cursor = con.cursor()
    cursor.execute("DELETE from CUENTAS where ID="+str(ID))
    con.commit()
    con.close()
    
#funcion que optimza y centra la ventana del programa a la ventana del computador
def center(toplevel): 
    toplevel.update_idletasks() 
    w = toplevel.winfo_screenwidth() 
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x')) 
    x = w/2 - size[0]/2 
    y = h/2 - size[1]/2 
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
    
#crea la base de datos 
def crea_basededatos():
    #se verifica que el archivo prueba.db no este ya creado
    if not(path.exists("prueba.db")):
        con = sqlite3.connect(Ubicacion_bd)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE CUENTAS
                        (ID 		        INT PRIMARY KEY NOT NULL,
                        CUENTA 		        TEXT NOT NULL,
                        VALOR 		        REAL NOT NULL,
                        TIPO			TEXT NOT NULL)''')
        con.close()
    #si ya esta la base de datos se elimina y se vuelve a crear para vaciarla
    else:
        Os.remove("prueba.db")
        crea_basededatos()
ventana_Principal()
