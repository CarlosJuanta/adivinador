#Carlos Enrique Juantá Tax
#AGENTE MUNDO JUGUETE
#ADIVINADOR DE CIUDADES
#1490-19-21295

import pickle
import os


FILE_NAME = "raiz.txt"


class Node:
    
    #Implementación de un arbol binario de búsqueda simple
    #esta función se utiliza para crear una instancia de un nodo en un árbol binario de búsqueda,
    #donde se asigna un valor dato al nodo y se inicializan los atributos izquierda y derecha como None.
    
    def crear_arbol(a, dato):
        a.izquierda = None
        a.derecha = None
        a.dato = dato


def obtener_nodo_inicial(
        pregunta="¿Está en Guatemala?",
        noAdivina="New York",
        siAdivina="Xela") -> Node:
    
    #Esta función retorna el nodo inicial con el cual comenzar el juego.
    #El parámetro pregunta para empezar el juego.
    #El parámetro noAdivina:Respuesta cuando la respuesta es no a la pregunta. 
    #El parámetro siAdivina: Respuesta cuando la respuesta es si a la pregunta.
    #:return: . Nodo inicial con hijos izquierdo y derecho.
    raiz = Node(pregunta)
    raiz.izquierda = Node(noAdivina)
    raiz.derecha = Node(siAdivina)
    return raiz


def obtener_respuesta_usuario() -> Node:
    
   #Función que permite al jugador guardar su respuesta.
   #:return: Nodo con la respuesta .

    print("No puedo adivinar la ciudad, ¿Qué ciudad es?")
    while True:  # Bucle para agurar que la respuesta al menos tenga un caracter.
        respuesta = input(">>").lower() #la respuesta se pasa a minúscula
        if len(respuesta) < 1:
            print("Por favor ingresa la respuesta correcta")
            continue
        return Node(respuesta)  # Retornar el nodo con la respuesta correcta


def respuesta_si() -> bool:
    while True:
        respuesta = input(">>").lower()  # convierte la intrada de texto a minúscula
        if len(respuesta) < 1 or respuesta[0] not in ('s', 'n'):  # Si el usuario no ingresa bien la respuesta, pedirla nuevamente.
            print("Lo siento, no puedo entenderte muy bien, puedes escribir s o n.")
            continue  # Repetir el bucle mientras la respuesta no sea ingresada correctamente.

        if respuesta[0] == 's':
            return True
        else:
            return False


def obtener_pregunta_usuario(nodoIncorrecto) -> Node:
    
    #Esta función ayuda para que el usuario ingrese una pregunta para lo que se está adivinando.
    #:parámetro nodoIncorrecto: El nodo incorrecto se mostrará para que el usuario haga una pregunta que se distinga de la respuesta incorrecta
    #:return: retorna el nodo con la pregunta.

    print(f"Escribe una repuesta de si o no que se distinga de: {nodoIncorrecto.dato}.")
    while True:  # Bucle para asegurar que el usuario ingrse una respuesta valida.
        pregunta = input(">>").capitalize()
        if len(pregunta) < 2 or pregunta[-1] != "?":
            print("Asegurate que estés ingresando una respuesta válida, puede ser esta estructura ¿Van muchos turistas?")
            continue
        return Node(pregunta)


def ingresar_pregunta_respuesta(nodoIncorrecto) -> Node:
    
    #Se a esta función en una etapa en la que el nodo no tiene un nodo hijo adecuado.
    #:parámetro nodoIncorrecto: El nodo incorrecto que será modificado.
    #:return: Nuevo nodo modificado con la pregunta y la respuesta.
    
    nodoRespuesta = obtener_respuesta_usuario()
    nodoPregunta = obtener_pregunta_usuario(nodoIncorrecto)

    print("Excelente, ¿la respuesta a tu pregunta es s o n?")
    if respuesta_si():
        nodoPregunta.derecha = nodoRespuesta
        nodoPregunta.izquierda = nodoIncorrecto
    else:
        nodoPregunta.izquierda = nodoRespuesta
        nodoPregunta.derecha = nodoIncorrecto

    return nodoPregunta


def modificar_nodo(nodohijo, nodopadre, direccion):
    
    #Modifica el nodo en su lugar
    #:parámetro nodohijo: El nodo hijo que va ser modifica en una pregunta pregunta.
    #:parámetro nodopadre: Nodo padre que va actualizar su referencia
    #:parámetro direccion: Dirección del nodo padre que cambiará su referencia
    #:return: None
    
    if direccion == 'izquierda':
        nodopadre.izquierda = ingresar_pregunta_respuesta(nodohijo)
    else:
        nodopadre.derecha = ingresar_pregunta_respuesta(nodohijo)


def bucleJuego(raiz):
    
    #Bucle principal para recorrer a traves del juego.
    #:parámetro raiz: padre raiz desde donde se empezará a hacer preguntas.
    #:return: nodo raíz modificado con nuevas respuestas.
    
    copia = raiz  # Obtener una copia del nodo raiz que servirá posteriormente.
    padre = None  # Mantener la posicion del padre mientras se hace el recorrido
    direccion = None  #  Mantener la posicion de la dirección del nodo hijo del nodo padre.

    while raiz:  # Recorrer a través de la raíz.
        if raiz.izquierda == raiz.derecha:  
            print(f"Es: {raiz.dato}?")
            if respuesta_si():
                print("Adiviné!!")
            else:
                modificar_nodo(raiz, padre, direccion)  # Modificar el nodo hoja y convertirlo en un nodo pregunta.
            raiz = None  # Colocar el nodo raiz a none cuando se acaba el juego
        else:  
            print(raiz.dato)
            padre = raiz
            if respuesta_si():
                direccion = "derecha"
                raiz = raiz.derecha
            else:  # El usuario contestó "no" a la pregunta.
                direccion = 'izquierda'
                raiz = raiz.izquierda

    return copia  # Regresar el nodo padre


def jugar():
    if os.path.exists(FILE_NAME):
        raiz = load_pickle(FILE_NAME)
    else:
        raiz = obtener_nodo_inicial()
    while True:
        raiz = bucleJuego(raiz)
        print("\nDeseas jugar nuevamente?")
        if respuesta_si():
            continue
        else:
            print("Adiós")
            dump_pickle(FILE_NAME, raiz)
            break


def dump_pickle(file, raiz):
    with open(file, 'wb') as f:
        pickle.dump(raiz, f)


def load_pickle(file):
    with open(file, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    print("WELCOME TO CITIES GUSSER")
    print("I KNOW WHAT YOU THINK")
    jugar()
