from tkinter import *
from tkinter import ttk
import sqlite3



class Producto():


    db = "database/productos.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1,1)
        self.ventana.wm_iconbitmap("recursos/sunset_ok.ico")


        frame = LabelFrame(self.ventana, text = "Registrar un nuevo producto")
        frame.grid(row = 0, column =0, columnspan = 8, pady = 20 )

        # Label y entrada de nombre
        self.etiqueta_nombre = Label(frame, text="Nombre:")
        self.etiqueta_nombre.grid(row=1, column=0)
        self.nombre = Entry(frame, borderwidth=4)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1,padx=20, pady=20, ipadx=11, ipady=3)

        # Label y entrada de precio
        self.etiqueta_precio = Label(frame, text="Precio:")
        self.etiqueta_precio.grid(row=2, column=0)
        self.precio = Entry(frame, borderwidth=4)
        self.precio.grid(row=2, column=1,padx=20, pady=20, ipadx=11, ipady=3)

        self.etiqueta_categaoria = Label(frame, text="Categoría:")
        self.etiqueta_categaoria.grid(row=1, column=2)
        self.categoria = ttk.Combobox(frame, values=["Electrónica", "Fotografía", "Smartphone", "Informática"], state='readonly')
        self.categoria.grid(row=1, column=3)

        self.etiqueta_stock = Label(frame, text="Stock")
        self.etiqueta_stock.grid(row=2, column=2)
        self.stock = Entry(frame, justify= 'right', borderwidth=4)
        self.stock.grid(row=2, column=3,padx=20, pady=20, ipadx=11, ipady=3)

        # Creo un estilo para los botones
        style_buscar = ttk.Style()
        style_buscar.map("my.TButton",
                         foreground=[('pressed', 'purple'), ('active', 'blue')],
                         background=[('pressed', '!disabled', 'black'), ('active', 'green')]
                         )

        # Boton añadir
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto",style="my.TButton" , command=self.add_producto)
        self.boton_aniadir.grid(row=3, columnspan=8, padx=20, pady=20, ipadx=14, ipady=4, sticky=W+E)

        styleMensaje = ttk.Style()
        styleMensaje.configure("my.TLabel", foreground="red", background="blue", font=("Calibri", 20, "bold"))

        self.mensaje = ttk.Label(text="", anchor="center", style="my.TLabel")
        self.mensaje.grid(row=3, column=0, columnspan=8, sticky=W+E)

        # Tabla Productos
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlighthickness=0, bd=0, font=("Calibri", 11)) #se modifica la fuente
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 13, "bold")) # se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})]) # eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(frame, height = 10, columns=("#0","#1","#2"), style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=4)
        self.tabla.heading("#0", text="Nombre", anchor=CENTER)
        self.tabla.heading("#1", text="Precio", anchor=CENTER)
        self.tabla.heading("#2", text="Categoría", anchor=CENTER)
        self.tabla.heading("#3", text="Stock", anchor=CENTER)

        # Botones de eliminar y editar
        self.boton_eliminar = ttk.Button(text="ELIMINAR",style="my.TButton", command=self.del_producto)
        self.boton_eliminar.grid(row=5, column=1, columnspan=2, padx=20, pady=20, ipadx=14, ipady=4, sticky=W+E)
        self.boton_editar = ttk.Button(text="EDITAR",style="my.TButton", command = self.edit_producto)
        self.boton_editar.grid(row=5, column=3, columnspan=2, padx=20, pady=20, ipadx=14, ipady=4, sticky=W+E)
        self.boton_buscar = ttk.Button(text="BUSCAR",style="my.TButton", command= self.buscar_producto)
        self.boton_buscar.grid(row=5, columnspan=2, column=5, padx=20, pady=20, ipadx=14, ipady=4, sticky=W+E)

        self.get_protductos()

    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_protductos(self):

        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)
        for fila in registros:
            print(fila)
            self.tabla.insert("", 0, text=fila[1], values=(fila[2], fila[3], fila[4]))


    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0


    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_categoria(self):
        categoria_introducido_por_usuario = self.categoria.get()
        return len(categoria_introducido_por_usuario) != 0

    def validacion_stock(self):
        stock_introducido_por_usuario = self.stock.get()
        return len(stock_introducido_por_usuario) != 0


    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)"
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())
            self.db_consulta(query, parametros)
            self.mensaje["text"] = "Datos guardados"
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria() and self.validacion_stock():
            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() == False and self.validacion_stock():
            self.mensaje["text"] = "La categoría es obligatoria"
        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock() == False:
            self.mensaje["text"] = "Debe poner una cantidad de productos"
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock():
            self.mensaje["text"] = "El nombre es obligatorio"
        else:
            self.mensaje["text"] = "Todos los campos son obligatorios"

        self.nombre.delete(0, END)
        self.precio.delete(0, END)
        #self.categoria.delete(0, END)
        self.stock.delete(0, END)
        self.mensaje.delete()


        self.get_protductos()


    def del_producto(self):
        print(self.tabla.item(self.tabla.selection()))
        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))
        self.get_protductos()

    def edit_producto(self):
        self.mensaje["text"] = ""
        try:
            self.tabla.item(self.tabla.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Por favor, seleccione un producto"
            return
        nombre = self.tabla.item(self.tabla.selection())["text"]
        old_precio = self.tabla.item(self.tabla.selection())["values"][0]

        self.ventana_editar = Toplevel()
        self.ventana_editar.title = "Editar Producto"
        self.ventana_editar.resizable(1,1)
        self.ventana_editar.wm_iconbitmap("recursos/editar.ico")

        titulo = Label(self.ventana_editar, text="Edicion de Productos", font=("Calibri", 34, "bold"))
        titulo.grid(row=0, column=0)

        frame_edit = LabelFrame(self.ventana_editar, text="EDITAR PRODUCTO")
        frame_edit.grid(row=1, column=0, columnspan=20,padx=20, pady=20)


        # Label y entrada de nombre
        self.etiqueta_nombre = Label(frame_edit, text="Nombre:")
        self.etiqueta_nombre.grid(row=2, column=1, sticky=W + E)
        self.nombre_antiguo= Entry(frame_edit, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly')
        self.nombre_antiguo.grid(row=2, column=3, sticky=W + E)

        # Label y entrada de precio
        self.etiqueta_precio = Label(frame_edit, text="Precio:")
        self.etiqueta_precio.grid(row=3, column=1, sticky=W + E)
        self.precio_antiguo = Entry(frame_edit, textvariable=StringVar(self.ventana_editar, value=old_precio), state='readonly')
        self.precio_antiguo.grid(row=3, column=3, sticky=W + E)


        self.etiqueta_newNombre = Label(frame_edit, text="Nuevo nombre:")
        self.etiqueta_newNombre.grid(row=2, column=4)
        self.newNombre = Entry(frame_edit)
        self.newNombre.focus()
        self.newNombre.grid(row=2, column=6, sticky=W + E)
        self.etiqueta_newPrecio = Label(frame_edit, text="Nuevo precio:")
        self.etiqueta_newPrecio.grid(row=3, column=4, sticky=W + E)
        self.newPrecio = Entry(frame_edit)
        self.newPrecio.grid(row=3, column=6, sticky=W + E)

        self.boton_actualizar = ttk.Button(frame_edit, text="Actualizar Producto", style="my.TButton", command=lambda: self.actualizar_productos(self.newNombre.get(), self.nombre_antiguo.get(), self.newPrecio.get(), self.precio_antiguo.get()))

        self.boton_actualizar.grid(row=5, columnspan=8, padx=20, pady=20, sticky=W + E)
        
    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio): 
        producto_modificado = False
        query ="UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio =?"
        if nuevo_nombre != "" and nuevo_precio != "":
            parametros = (nuevo_nombre, nuevo_precio,antiguo_nombre, antiguo_precio)
            producto_modificado = True
        elif nuevo_nombre != "" and nuevo_precio == "":
            parametros = (nuevo_nombre, antiguo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True
        elif nuevo_nombre == "" and nuevo_precio != "":
            parametros = (antiguo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True

        if producto_modificado:
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()
            self.mensaje["text"] = f"El producto {antiguo_nombre} ha sido actualizado con éxito"
            self.get_protductos()
        else:
            self.ventana_editar.destroy()
            self.mensaje["text"] = f"El producto {antiguo_nombre} NO ha sido actualizado"


    def buscar_producto(self):

        self.ventana_busqueda = Toplevel()
        self.ventana_busqueda.title = "Buscar producto"
        self.ventana_busqueda.resizable(1,1)
        self.ventana_busqueda.wm_iconbitmap("recursos/buscar.ico")

        titulo_buscar = Label(self.ventana_busqueda, text="Busqueda de Productos", font=("Calibri", 30, "bold"))
        titulo_buscar.grid(row=0, column=0)

        frame_buscar = LabelFrame(self.ventana_busqueda, text="BUSCAR PRODUCTO")
        frame_buscar.grid(row=1, column=0, columnspan=20, padx=20, pady=20)

        self.nombre_buscar = Label(frame_buscar, text="Nombre", font=("Calibri", 20, "bold"))
        self.nombre_buscar.grid(row=1, columnspan=20, sticky=W+E)
        self.intro_nombre_buscar = Entry(frame_buscar, borderwidth=4)
        self.intro_nombre_buscar.grid(row=2, column=0, padx=20, pady=20, ipadx=15, ipady=8, columnspan=20, sticky=W+E)
        #self.intro_nombre_buscar.place(width=190, height=30)


        self.boton_busqueda = ttk.Button(frame_buscar, text="Buscar", style="my.TButton", command=self.get_busqueda)
        self.boton_busqueda.grid(row=3, column=0, columnspan=20, padx=20, pady=20, ipadx=15, ipady=5, sticky=W+E)
        #self.boton_busqueda.bind("<Return>", self.callback)

        # Tabla para los resulados de la busqueda
        self.tabla_buscar = ttk.Treeview(frame_buscar, height = 6, columns=("#0","#1","#2"), style="mystyle.Treeview")
        self.tabla_buscar.grid(row=4, column=0, columnspan=1)
        self.tabla_buscar.heading("#0", text="Nombre", anchor=CENTER)
        self.tabla_buscar.heading("#1", text="Precio", anchor=CENTER)
        self.tabla_buscar.heading("#2", text="Categoría", anchor=CENTER)
        self.tabla_buscar.heading("#3", text="Stock", anchor=CENTER)

    def get_busqueda(self):


        registros_tabla = self.tabla_buscar.get_children()
        for fila in registros_tabla:
            self.tabla_buscar.delete(fila)

        query = "SELECT * FROM producto WHERE nombre == ?"
        parametros = (self.intro_nombre_buscar.get(),)
        registros = self.db_consulta(query, parametros)
        for fila in registros:
            print(fila)
            self.tabla_buscar.insert("", 0, text=fila[1], values=(fila[2], fila[3], fila[4]))


    def __str__(self):
        return "{} --> {}".format(self.nombre, self.precio )





if __name__ == "__main__":

    root = Tk()
    app = Producto(root)
    root.mainloop()