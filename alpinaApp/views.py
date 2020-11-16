import io
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import fech_corta, donaciones
from .forms import OrderForm
from random import sample
from datetime import datetime 
from datetime import date
#####################################################################################################################################
class TreeNode(object): 
    def __init__(self, val): 
        self.val = val 
        self.left = None
        self.right = None
        self.height = 1
class AVL_Tree(object): 
    def insert(self, root, key): 
        if not root: 
            return TreeNode(key) 
        elif key[2] < root.val[2]: 
            root.left = self.insert(root.left, key) 
        else: 
            root.right = self.insert(root.right, key) 
        root.height = 1 + max(self.getHeight(root.left), 
                           self.getHeight(root.right)) 
        balance = self.getBalance(root)
        if balance > 1 and key[2] < root.left.val[2]: 
            return self.rightRotate(root) 
        if balance < -1 and key[2] > root.right.val[2]: 
            return self.leftRotate(root) 
        if balance > 1 and key[2] > root.left.val[2]: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 
        if balance < -1 and key[2] < root.right.val[2]: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
  
        return root 
    def leftRotate(self, z): 
        y = z.right 
        T2 = y.left 
        y.left = z 
        z.right = T2  
        z.height = 1 + max(self.getHeight(z.left), 
                         self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                         self.getHeight(y.right)) 
        return y 
    def rightRotate(self, z):  
        y = z.left 
        T3 = y.right 
        y.right = z 
        z.left = T3 
        z.height = 1 + max(self.getHeight(z.left), 
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                        self.getHeight(y.right)) 
        return y  
    def getHeight(self, root): 
        if not root: 
            return 0
  
        return root.height  
    def getBalance(self, root): 
        if not root: 
            return 0
  
        return self.getHeight(root.left) - self.getHeight(root.right) 
    def preOrder(self, root):  
        if not root:
            return  
        print("{0} ".format(root.val[2]), end="") 
        self.preOrder(root.left) 
        self.preOrder(root.right) 
    def buscar(self,root,data):
        current=root
        if(current.val[2]==data):
            return current.val
        while(current):
            if(data<current.val[2]):
                current=current.left
                if(current):
                    if(current.val[2]==data):
                        return current.val
            else:
                current=current.right
                if(current):
                    if(current.val[2]==data):
                        return current.val
        return False
    def buscar_h(self,root,data,fecha):
        current=root
        if(current.val[2]==data and current.val[0]==fecha ):
            return current.val
        while(current):
            if(data<current.val[2]):
                current=current.left
                if(current):
                    if(current.val[2]==data and current.val[0]==fecha):
                        return current.val                      
            else:
                current=current.right
                if(current):
                    if(current.val[2]==data and current.val[0]==fecha):
                        return current.val
        return False
    def actualizar(self,root,data,cantidad):
        current=root
        if(current.val[2]==data):
            return current.val
        while(current):
            if(data<current.val[2]):
                current=current.left
                if(current):
                    if(current.val[2]==data):
                        current.val[6]=cantidad
                        return current.val
            else:
                current=current.right
                if(current):
                    if(current.val[2]==data):
                        current.val[6]=cantidad
                        return current.val
        return False
##############################################################################################################################
#HISTORIAL
class nodo_historial:
    def __init__(self,año,arbol=AVL_Tree()):
        self.año=año
        self.next=None
        self.data=arbol
class lista_historial:
    def __init__(self):
        self.head=None
    def insert(self,año,arbol):
        new_node=nodo_historial(año, arbol)
        new_node.next=self.head
        self.head=new_node
        return self.head
    def imprimir(self,root):
        current=self.head
        current.data.preOrder(root)
    def buscar(self,root,año,arbol,dato,fecha):
        current=self.head
        while(current):
            if(current.año==año):
                if(current.año==2019):
                    return arbol.buscar_h(root1,dato,fecha)
                elif(current.año==2018):
                    return arbol.buscar_h(root2,dato,fecha)
                elif(current.año==2017):
                    return arbol.buscar_h(root3,dato,fecha)
            current=current.next
def historial(archivo, root,arbol):
    for line in open(archivo, encoding="utf8").readlines():
            data=line.strip().split(",")
            data[0]= data[0].strip("\ufeff")
            data[0]=str(data[0])
            #codigo producto
            data[2]=int(data[2])
            #fecha de vencimiento
            data[5] =str(data[5])
            #Unidades producto
            data[6]=float(data[6])
            #Vida útil producto
            data[7]=0
            #Costo unitario
            data[8]=float(data[8])
            #Costo total
            data[9]=float(data[9])
            #print("fecha arreglada")
            #print(fecha_str)
            #Se crea la tupla con los datos y se agrega a la lista enlazada
            datos=[data[0], data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]]
            root=arbol.insert(root,datos)
    return root
##############################################################################################################################
class Node:
    def __init__(self,data):
        self.data = data
        self.next = None
class lista_enlazada:
    def __init__(self):
        self.head=None
    def insertar(self,data):
        new_node=Node(data)
        new_node.next=self.head
        self.head=new_node
        return self.head
    def eliminar(self,dato):
        current=self.head
        data=current.data
        if(data[2]==dato):
            if(current.next==None):
                self.head=None
                return self.head
            elif(current.next!=None):
                current=current.next
                self.head=current
                return self.head
        else:
            while(current):
                siguiente=current.next
                if(siguiente):
                    if(siguiente.data[2]==dato):
                        current.next=current.next.next
                        break
                current=current.next
            return self.head
    def eliminar_fecha_corta(self,dato):
        current=self.head
        data=current.data
        if(data[1]==dato):
            if(current.next==None):
                self.head=None
                return self.head
            elif(current.next!=None):
                current=current.next
                self.head=current
                return self.head
        else:
            while(current):
                siguiente=current.next
                if(siguiente):
                    if(siguiente.data[1]==dato):
                        current.next=current.next.next
                        break
                current=current.next
            return self.head
    def ver(self):
        current=self.head
        while(current):
            print(current.data)
            current=current.next
    def lista_actualizada(self,archivo):
        current = self.head
        while current:
            lista=current.data
            if type(lista[0]) != str:
                lista[0] = lista[0].strftime('%d/%m/%Y')
            else:
                lista[0]=lista[0].lstrip("'")
                lista[0]=lista[0].rstrip("'")
            lista[1]=lista[1].lstrip("'")
            lista[1]=lista[1].rstrip("'")
            lista[3]=lista[3].lstrip("'")
            lista[3]=lista[3].rstrip("'")
            lista[4]=lista[4].lstrip("'")
            lista[4]=lista[4].rstrip("'")
            if type(lista[5]) != str:
                lista[5] = lista[5].strftime('%d/%m/%Y')
            else:
                lista[5]=lista[5].lstrip("'")
                lista[5]=lista[5].rstrip("'")            
            dato=str(lista)
            dato=dato.lstrip("[")
            dato=dato.rstrip("]")
            archivo.write(lista[0]+","+lista[1]+","+str(lista[2])+","+lista[3]+","+lista[4]+","+lista[5]+","+str(lista[6])+","+
            str(lista[7])+","+str(lista[8])+","+str(lista[9])+"\n")
            current = current.next
    def lista_fech_corta(self,archivo):
        current = self.head
        while current:
            lista=current.data
            if type(lista[0]) != str:
                lista[0] = lista[0].strftime('%d/%m/%Y')
            else:
                lista[0]=lista[0].lstrip("'")
                lista[0]=lista[0].rstrip("'")
            lista[2]=lista[2].lstrip("'")
            lista[2]=lista[2].rstrip("'")
            lista[3]=lista[3].lstrip("'")
            lista[3]=lista[3].rstrip("'")
            #lista[4]=lista[4].lstrip("'")
            #lista[4]=lista[4].rstrip("'")          
            dato=str(lista)
            dato=dato.lstrip("[")
            dato=dato.rstrip("]")
            archivo.write(lista[0]+","+str(lista[1])+","+str(lista[2])+","+str(lista[3])+","+str(lista[4])+","+str(lista[5])+"\n")
            current = current.next   
    def metodo_grafica(self):
        current=self.head
        graf_data=dict()
        cantidad=0
        while(current):
            tupla=current.data
            fecha=tupla[0]
            mes=fecha.month
            cantidad+= tupla[9]
            graf_data[mes]=cantidad
            current=current.next
        return graf_data
    def imprimir(self):
        current=self.head
        while(current):
            kk=current.data
            fecha=kk[0]
            print(fecha.month)
            current=current.next
    def agregar(self,codigo,fecha,datos):
        actual=self.head
        existe=False
        while(actual):
            producto=actual.data
            if(producto[2]==codigo and producto[0]==fecha):
                    existe=True
                    return False
            actual=actual.next
        if(not existe):
            inventario.insertar(datos)
            return True
    def actualizar(self, codigo, fecha_lote ,cantidad):
        current=self.head
        while(current):
            producto=current.data
            if(codigo==producto[2]):
                producto[6]= cantidad
                return True
            current=current.next
    def actualizacion_BD(self):
        art=fech_corta.objects.all().delete()
        current=self.head
        while(current):
            current_time = datetime.now()
            data= current.data
            fecha_str=str(data[0])
        #codigo producto
            data[2]=int(data[2])
        #fecha de vencimiento
            fechav_str= str(data[5])
            data[5]=str(data[5])
            data[5] = datetime.strptime(data[5],'%d/%m/%Y')
        #Unidades producto
            data[6]=float(data[6])
        #Vida útil producto
            if(((data[5]- current_time).days)>0):
               data[7]=(abs(data[5]- current_time)).days
            else:
               data[7]=0
            data[9]=float(data[9])
            fecha_str=fecha_str.split("/")
            fecha_str= fecha_str[2]+"-"+fecha_str[1]+"-"+fecha_str[0]
        #print(fecha vencimiento)
            fechav_str=fechav_str.split("/")
            fechav_str=fechav_str[2]+"-"+fechav_str[1]+"-"+fechav_str[0]
            if(((data[5]- current_time).days)<15):
                art=fech_corta(lote=fecha_str,codigo=data[2], producto=data[4],vencimiento=fechav_str,vida=data[7], cantidad=data[6])
                art.save()
            current=current.next
    def donaciones(self,codigo, fecha_lot):
        current=self.head
        while(current):
            data= current.data
            #print(data[1])
            #print(codigo)
            if(codigo==data[1] or str(codigo)==data[1]):
                return True 
            current=current.next
    def buscar_fecha_corta(self,codigo):
        current= self.head
        while(current):
            if(current.data[1]==codigo):
                data= [current.data[0],current.data[1],current.data[2],current.data[3],current.data[4],current.data[5]]
                return data
            current=current.next
    def isEmpty(self):
        if(self.head==None):
            return True
        else:
            return False
class colaPrioridad:
    def __init__(self):
        self.cola=[[0]]
    def lon(self):
        return len(self.cola)-1
    def ordenar(self,i):
        if i==1:
            return self.cola
        else:
            if(self.cola[i][5]<= self.cola[int((i/2))][5]):
                self.cola[i][5], self.cola[int((i/2))][5]= self.cola[int((i/2))][5],self.cola[i][5]
                self.ordenar(int((i/2)))
        return self.cola
    def insertar(self, dato):
        self.cola.append(dato)
        return self.cola
archivo_2019='C:/Users/Laura Ceballos/Desktop/Proyecto ED/proyecto/alpinaApp/data/2019.txt'
archivo_2018='C:/Users/Laura Ceballos/Desktop/Proyecto ED/proyecto/alpinaApp/data/2018.txt'
archivo_2017='C:/Users/Laura Ceballos/Desktop/Proyecto ED/proyecto/alpinaApp/data/2017.txt'
inventario=lista_enlazada()
grafica=lista_enlazada()
fecha_cort=lista_enlazada()
cola_donaciones=colaPrioridad()
myTree=AVL_Tree()
root=None
arbol2019=AVL_Tree()
root1=None
arbol2018=AVL_Tree()
root2=None
arbol2017=AVL_Tree()
root3=None
root1=historial(archivo_2019, root1, arbol2019)
root2=historial(archivo_2018, root2, arbol2018)
root3=historial(archivo_2017, root3, arbol2017)      
historial=lista_historial()
historial.insert(2019,arbol2019)
historial.insert(2018,arbol2018)
historial.insert(2017,arbol2017)
for line in open('C:/Users/Laura Ceballos/Desktop/Proyecto ED/proyecto/alpinaApp/data/grafica.txt', encoding="utf8").readlines():
        data=line.strip().split(",")
        current_time = datetime.now()
        fecha_str=str(data[0])
        data[0]= data[0].strip("\ufeff")
        data[0]=datetime.strptime(data[0],'%d/%m/%Y')
        #codigo producto
        data[2]=int(data[2])
        #fecha de vencimiento
        fechav_str= str(data[5])
        data[5] = datetime.strptime(data[5],'%d/%m/%Y')
        #Unidades producto
        data[6]=float(data[6])
        #Vida útil producto
        if(((data[5]- current_time).days)>0):
            data[7]=(abs(data[5]- current_time)).days
        else:
            data[7]=0
        #Costo unitario
        data[8]=float(data[8])
        #Costo total
        data[9]=float(data[9])
        fecha_str=fecha_str.split("/")
        fecha_str= fecha_str[2]+"-"+fecha_str[1]+"-"+fecha_str[0]
        #print("fecha arreglada")
        #print(fecha_str)
        fechav_str=fechav_str.split("/")
        fechav_str=fechav_str[2]+"-"+fechav_str[1]+"-"+fechav_str[0]
        #Se crea la tupla con los datos y se agrega a la lista enlazada
        if(((data[5]- current_time).days)<15):
            datos=[data[0], data[2], data[3], data[4], data[6],data[7]]
            #art=fech_corta.objects.all().delete()
            #art=fech_corta(lote=fecha_str,codigo=data[2], producto=data[4],vencimiento=fechav_str,vida=data[7], cantidad=data[6])
            #art.save()
        datos=[data[0], data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]]
        grafica.insertar(datos)
def leer_datos():
    for line in open('C:/Users/Laura Ceballos/Desktop/Proyecto ED/proyecto/alpinaApp/data/10k_Datos_.txt', encoding="utf8").readlines():
        data=line.strip().split(",")
        current_time = datetime.now()
        fecha_str=str(data[0])
        data[0]= data[0].strip("\ufeff")
        data[0]=datetime.strptime(data[0],'%d/%m/%Y')
        #codigo producto
        data[2]=int(data[2])
        #fecha de vencimiento
        fechav_str= str(data[5])
        data[5] = datetime.strptime(data[5],'%d/%m/%Y')
        #Unidades producto
        data[6]=float(data[6])
        #Vida útil producto
        if(((data[5]- current_time).days)>0):
            data[7]=(abs(data[5]- current_time)).days
        else:
            data[7]=0
        #Costo unitario
        data[8]=float(data[8])
        #Costo total
        data[9]=float(data[9])
        fecha_str=fecha_str.split("/")
        fecha_str= fecha_str[2]+"-"+fecha_str[1]+"-"+fecha_str[0]
        #print("fecha arreglada")
        #print(fecha_str)
        fechav_str=fechav_str.split("/")
        fechav_str=fechav_str[2]+"-"+fechav_str[1]+"-"+fechav_str[0]
        #Se crea la tupla con los datos y se agrega a la lista enlazada
        if(((data[5]- current_time).days)<15):
            datos=[data[0], data[2], data[3], data[4], data[6],data[7]]
            fecha_cort.insertar(datos)
            #art=fech_corta.objects.all().delete()
            #art=fech_corta(lote=fecha_str,codigo=data[2], producto=data[4],vencimiento=fechav_str,vida=data[7], cantidad=data[6])
            #art.save()
        datos=[data[0], data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]]
        inventario.insertar(datos)
for line in open('C:/Users/Laura Ceballos/Desktop/Proyecto ED/proyecto/alpinaApp/data/10k_Datos_.txt', encoding="utf8").readlines():
        data=line.strip().split(",")
        current_time = datetime.now()
        fecha_str=str(data[0])
        data[0]= data[0].strip("\ufeff")
        data[0]=datetime.strptime(data[0],'%d/%m/%Y')
        #codigo producto
        data[2]=int(data[2])
        #fecha de vencimiento
        fechav_str= str(data[5])
        data[5] = datetime.strptime(data[5],'%d/%m/%Y')
        #Unidades producto
        data[6]=float(data[6])
        #Vida útil producto
        if(((data[5]- current_time).days)>0):
            data[7]=(abs(data[5]- current_time)).days
        else:
            data[7]=0
        #Costo unitario
        data[8]=float(data[8])
        #Costo total
        data[9]=float(data[9])
        fecha_str=fecha_str.split("/")
        fecha_str= fecha_str[2]+"-"+fecha_str[1]+"-"+fecha_str[0]
        #print("fecha arreglada")
        #print(fecha_str)
        fechav_str=fechav_str.split("/")
        fechav_str=fechav_str[2]+"-"+fechav_str[1]+"-"+fechav_str[0]
        #Se crea la tupla con los datos y se agrega a la lista enlazada
        datos=[data[0], data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]]
        root=myTree.insert(root,datos) 
def actualizacion_BD_donaciones(lista):
    don=donaciones.objects.all().delete()
    for i in range(1,len(lista)):
        producto=lista[i]
        fecha_str=str(producto[0])
        fecha_str=fecha_str.split("/")
        fecha_str= fecha_str[2]+"-"+fecha_str[1]+"-"+fecha_str[0]
        producto[1]=int(producto[1])
        producto[3]=str(producto[3])
        producto[4]=int(producto[4])
        producto[5]= int(producto[5])
        don=donaciones(lote=fecha_str,codigo=producto[1], producto=producto[3],vida=producto[5], cantidad=producto[4])
        don.save()
leer_datos()
grafica_=grafica.metodo_grafica()
print(grafica_)
#ver lista enlazada
#inventario.ver()
#historial.imprimir(root1)
#kk=historial.buscar(root1,2019,arbol2019, 3, "07/11/2019")
#print(kk)
print("__________________")
def ingreso(request):
    if (request.method == 'POST'):
        correo=request.POST.get('correo')
        password=request.POST.get('password')
        user= authenticate(request, username= correo, password= password)
        if user is not None:
            login(request, user)
            return redirect('principal')
        else:
            messages.info(request, "Usuario o contraseña incorrecta")
    return render(request, "alpinaApp/inicio.html")
def salida(request):
    logout(request)
    return redirect('inicio')
def principal(request,raiz=root):
    if (request.method == 'POST'):
        try:
            codigo=request.POST.get("codigo")
            codigo=int(codigo)
            dato=myTree.buscar(raiz,codigo)
            if  dato==False:
                messages.info(request,"Producto No Encontrado")
            else:
                if type(dato[0]) != str:
                    dato[0] = dato[0].strftime('%d/%m/%Y')
                messages.info(request, "Lote:  "+str(dato[0]))
                messages.info(request, "Nombre:  "+str(dato[4]))
                messages.info(request, "Descripción:  "+str(dato[3]))
                if type(dato[5]) != str:
                    dato[5] = dato[5].strftime('%d/%m/%Y')
                messages.info(request, "Vencimiento:  "+str(dato[5]))
                messages.info(request, "Cantidad:  "+str(dato[6]))
        except:
            messages.error(request,"Ingrese Código")

    return render(request, "alpinaApp/principal.html")
def plot(request):
    cantidad=[]
    for key in grafica_:
        cantidad.append(int(grafica_[key]))
    cantidad.reverse()
    x=['Ene','Feb','Mar','Abr','May','Jun','Jul','Agos','Sept','Oct','Nov']
    y=cantidad
    f = plt.figure()
    axes = f.add_axes([0.18, 0.15, 0.75, 0.75]) # [left, bottom, width, height]
    axes.plot(x, y)
    plt.ticklabel_format(axis='y', style='plain')
    axes.set_xlabel("Mes")
    axes.set_ylabel("Costo" )
    axes.set_title("Costos producción 2020")
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)
    f.clear()
    response= HttpResponse(buf.getvalue(), content_type="image/png")
    response["Content-Lenght"]=str(len(response.content))
    return response
def informe_produccion(request, raiz=root):
    current_time = datetime.now()
    if fecha_cort.isEmpty():
        mensaje=messages.info(request, "No productos próxmos a expirar :)")
    else:
        messages.info(request, "¡Hay productos próximos a expirar!")
    try:
        if (request.method == 'POST' and "agregar" in request.POST):
            fecha=request.POST.get('fecha_lote')
            #convertir formato de fecha aaaa-mm-dd a dd/mm/aaaa
            fecha=str(fecha)
            fecha= fecha.split("-")
            fecha.reverse()
            fecha= fecha[0]+"/"+fecha[1]+"/"+fecha[2]
            fecha= datetime.strptime(fecha,'%d/%m/%Y')
            #fin conversión
            ciudad=request.POST.get('ciudad')
            producto=request.POST.get('producto')
            codigo=request.POST.get('codigo_producto')
            codigo=int(codigo)
            producto=request.POST.get('producto')
            descripcion=request.POST.get('descrip_producto')
            fecha_ven=request.POST.get('vencimiento')
            #convertir formato de fecha aaaa-mm-dd a dd/mm/aaaa
            fecha_ven=str(fecha_ven)
            fecha_venc= fecha_ven.split("-")
            fecha_venc.reverse()
            fecha_venc= fecha_venc[0]+"/"+fecha_venc[1]+"/"+fecha_venc[2]
            fecha_venc = datetime.strptime(fecha_venc,'%d/%m/%Y')
            #fin conversión
            unidades=request.POST.get('unidades')
            unidades=int(unidades)
            vida=(abs(fecha_venc-current_time).days)
            costo_u=request.POST.get('costoU')
            costo_u=int(costo_u)
            costo_t=request.POST.get('costoT')
            costo_t=int(costo_t)
            if((fecha_venc-current_time).days<15):
                datos1=[fecha,codigo,descripcion,producto,unidades,vida]
                fecha_cort.insertar(datos1)
            datos=[fecha,ciudad,codigo,descripcion,producto,fecha_venc,unidades,vida,costo_u,costo_t]
            agregado=inventario.agregar(codigo, fecha, datos)
            raiz=myTree.insert(raiz,datos)
            #myTree.preOrder(root)
            #print("lista con agregado:")
            if(agregado==True):
                messages.success(request, "¡Ingreso exitoso!")
            else:
                messages.error(request, "El producto ya existe. Para modificar vaya a la sección de actualización")
    except:
        messages.error(request, "Digite Formulario")
    if (request.method == 'POST' and 'actualizar' in request.POST):
        try:
            codigo_act=request.POST.get("codigo_act")
            codigo_act=int(codigo_act)
            fecha_lot=request.POST.get("fecha_act")
            fecha_lot=str(fecha_lot)
            fecha_lot= fecha_lot.split("-")
            fecha_lot.reverse()
            fecha_lot= fecha_lot[0]+"/"+fecha_lot[1]+"/"+fecha_lot[2]
            fecha_lot = datetime.strptime(fecha_lot,'%d/%m/%Y')
            cantidad=request.POST.get("cantidad_act")
            cantidad=int(cantidad)
            actualizado=inventario.actualizar(codigo_act,fecha_lot,cantidad)
            actualizar_BST= myTree.actualizar(raiz,codigo_act,cantidad)
            if(actualizado==True):
                messages.success(request, "¡Actualización exitosa!")
            else:
                messages.error(request, "No se escuentra el producto. Verifique")
        except:
            messages.error(request,"Diligencie")
    return render(request, 'alpinaApp/informe_produccion.html') 
def fecha_corta(request):
    archivo_nuevo=open('C:/Users/Laura Ceballos/Desktop/Proyecto ED/proyecto/alpinaApp/data/10k_Datos_.txt',"w",encoding="utf8")
    archivo_fc=open('C:/Users/Laura Ceballos/Desktop/Proyecto ED/proyecto/alpinaApp/data/fecha_corta.txt',"w",encoding="utf8")
    inventario.lista_actualizada(archivo_nuevo)
    inventario.actualizacion_BD()
    fecha_cort.lista_fech_corta(archivo_fc)   
    productos_fecha_corta= fech_corta.objects.all()
    contexto= {'productos':productos_fecha_corta}
    leer_datos()
    if (request.method == "POST"):
        codigo_act=request.POST.get("codigo_act")
        codigo_act=int(codigo_act)
        fecha_lot=request.POST.get("fecha_act")
        redireccion=request.POST.get("redireccion")
        redireccion=str(redireccion)
        if(redireccion=="donaciones"):
            lote=fecha_lot
            lote= lote.split("-")
            lote.reverse()
            lote= lote[0]+"/"+lote[1]+"/"+lote[2]
            donacion=fecha_cort.donaciones(codigo_act,lote)
            if(donacion==True):
                inventario.eliminar(codigo_act)
                inventario.ver()
                art=fech_corta.objects.filter(codigo=codigo_act).delete()
                fecha_cort.ver()
                producto=fecha_cort.buscar_fecha_corta(codigo_act)
                fecha_cort.eliminar_fecha_corta(codigo_act)
                cola_donaciones.insertar(producto)
                i=cola_donaciones.lon()
                cola_=cola_donaciones.ordenar(i)
                actualizacion_BD_donaciones(cola_)
    return render(request, 'alpinaApp/fecha_corta.html', contexto)
def frame_donaciones(request):
    donacion= donaciones.objects.all()
    contexto= {'productos':donacion}
    return render(request, "alpinaApp/donaciones.html",contexto)
def historial_(request):
    if (request.method == "POST"):
        try:
            codigo_act=request.POST.get("codigo_act")
            codigo_act=int(codigo_act)
            fecha_lot=request.POST.get("fecha_act")
            año=request.POST.get("año")
            año=int(año)
            if(año==2019):
                dato=historial.buscar(root1,año,arbol2019,codigo_act,fecha_lot)
                if(dato==False):
                    messages.info(request,"Producto No encontrado")
                else:
                    if type(dato[0]) != str:
                        dato[0] = dato[0].strftime('%d/%m/%Y')
                    messages.info(request, "Lote:  "+str(dato[0]))
                    messages.info(request, "Nombre:  "+str(dato[4]))
                    messages.info(request, "Descripción:  "+str(dato[3]))
                    if type(dato[5]) != str:
                        dato[5] = dato[5].strftime('%d/%m/%Y')
                    messages.info(request, "Vencimiento  :  "+str(dato[5]))
                    messages.info(request, "Cantidad  :  "+str(dato[6]))
                    dato[8]=int(dato[8])
                    messages.info(request,"Costo  :"+str(dato[8]) )
            elif (año==2018):
                dato=historial.buscar(root2,año,arbol2018,codigo_act,fecha_lot)
                if(dato==False):
                    messages.info(request,"Producto No encontrado")
                else:
                    if type(dato[0]) != str:
                        dato[0] = dato[0].strftime('%d/%m/%Y')
                    messages.info(request, "Lote:  "+str(dato[0]))
                    messages.info(request, "Nombre:  "+str(dato[4]))
                    messages.info(request, "Descripción:  "+str(dato[3]))
                    if type(dato[5]) != str:
                        dato[5] = dato[5].strftime('%d/%m/%Y')
                    messages.info(request, "Vencimiento:  "+str(dato[5]))
                    messages.info(request, "Cantidad:  "+str(dato[6]))
            elif(año==2017):
                dato=historial.buscar(root3,año,arbol2017,codigo_act,fecha_lot)
                if(dato==False):
                    messages.info(request,"Producto No encontrado")
                else:
                    if type(dato[0]) != str:
                        dato[0] = dato[0].strftime('%d/%m/%Y')
                    messages.info(request, "Lote:  "+str(dato[0]))
                    messages.info(request, "Nombre:  "+str(dato[4]))
                    messages.info(request, "Descripción:  "+str(dato[3]))
                    if type(dato[5]) != str:
                        dato[5] = dato[5].strftime('%d/%m/%Y')
                    messages.info(request, "Vencimiento:  "+str(dato[5]))
                    messages.info(request, "Cantidad:  "+str(dato[6]))
            else:
                messages.info(request,"Ingrese un año válido")
        except:
            messages.error(request,"Ingrese datos")
    return render(request,"alpinaApp/historial.html")