 
import csv
import unicodedata

#CONSTANTES
OPCIONES_MENU = "1. Mostrar Países \n2. Agregar Nuevo País \n3. Actualizar Población y Superficie de un País \n4. Buscar País \n5. Filtrar Países \n6. Ordenar Países \n7. Estadísticas \n8. Salir"
OPCIONES_FILTRAR = "1. Continente \n2. Rango de Población \n3. Rango de Superficie"
OPCIONES_ORDENAR = "1. Nombre \n2. Población \n3. Superficie"
ERROR_VALOR_NUMERO = "Solo son permitidos valores numéricos"

#VALIDACIONES
def validacion_de_textos(texto):
    texto_limpio = texto.strip()

    try:
        if not texto_limpio:
            raise ValueError("No se aceptan espacion vacios")
        
        if not texto_limpio.replace(" ", "").isalpha():
            raise ValueError("Solo se permiten valores alfabeticos")

        return True
    except ValueError as error:
        raise error

def validacion_numerica(numero):
    try:
        if not numero.isdigit():
            raise ValueError("Solo se permiten valores numéricos")
        
        return True
    except ValueError as error:
        raise error

def remover_acentos(texto):
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def validar_opcion_menu(opcion, rango):
    try:
        if opcion.isalpha() or opcion.strip() == "":
            raise ValueError(ERROR_VALOR_NUMERO)
        elif not opcion.isdigit():
            raise ValueError("El valor ingresado no es valido")
        elif int(opcion) > rango or int(opcion) == 0:
            raise ValueError("Opción fuera del menú")
        
        if int(opcion) and int(opcion) in range(1, rango+1):
            return True
    except ValueError as error:
        print(f"* Error: {error} *")
        print()
        return False


#LECTURA DE DATOS
def lectura_inicial_de_datos():
    lista_paises = []
    try:
        with open("paises_dataset.txt", "r", encoding="utf-8") as archivo:
            lectura = csv.DictReader(archivo)
            for fila in lectura:
                nuevo_valor = {}
                for llave, valor in fila.items():
                    nuevo_valor[llave.strip()] = valor.strip()
                lista_paises.append(nuevo_valor)
            return lista_paises
    except:
        print("Ocurrio un error al intentar abrir el archivo")
        return lista_paises

def guardado_de_datos(lista_paises):
    columnas = []
    try:
        with open("paises_dataset.txt", "r", encoding="utf-8") as archivo:
            lectura = csv.DictReader(archivo)
            for fila in lectura:
                for llave, valor in fila.items():
                    if llave.strip() not in columnas:
                        columnas.append(llave.strip())

        with open("paises_dataset.txt", "w", encoding="utf-8", newline="") as archivo:
            datos = csv.DictWriter(archivo, fieldnames=columnas)
            datos.writeheader()
            datos.writerows(lista_paises)
    except:
        return "Ocurrio un error al intentar guardar el archivo"


#LOGICA
def busqueda_pais(lista_paises, texto):
    pais = input(f"Ingrese el país que desea {texto}: ")
    try:
        validacion_de_textos(pais)

        listado_encontrado = []
        for item in lista_paises:
            nombre = remover_acentos(item['nombre'].lower())
            if pais.lower() in nombre:
                listado_encontrado.append(item)
        return listado_encontrado, pais
    except ValueError as error:
        raise error


def ordenar_paises(lista_paises, llave, descendente=False):
    return sorted(lista_paises, key=lambda x: x[llave] if llave == 'nombre' else int(x[llave]), reverse=descendente)


def filtrar_paises(lista_paises):
    valor = input(f"Ingrese el nombre del continente que quiere filtrar: ")
    try:
        validacion_de_textos(valor)
        listado_filtro = []
        for pais in lista_paises:
            for llave, value in pais.items():
                if llave == 'continente' and remover_acentos(value).lower() == valor.lower():
                    listado_filtro.append(pais)
        
        return listado_filtro
    except ValueError as error:
        raise error


def filtar_paises_rango(lista_paises, llave):
    try:
        rango_superior = input("Ingrese el rango superior del filtro: ")
        validacion_numerica(rango_superior)
        rango_inferior = input("Ingrese el rango inferior del filtro: ")
        validacion_numerica(rango_inferior)
        listado_filtro = []

        for pais in lista_paises:
            for key, value in pais.items():
                if key == llave and rango_inferior <= int(value) <= rango_superior:
                    listado_filtro.append(pais)
        
        return listado_filtro
    except ValueError as error:
        raise error


#ESTADISTICAS
def calcular_promedio(lista_paises):
    poblacion = 0
    superficie = 0
    contador = 0

    for pais in lista_paises:
        for key, value in pais.items():
            if key == 'poblacion':
                poblacion += int(value)

            if key == 'superficie':
                superficie += int(value)
        contador += 1
            
    poblacion = poblacion // contador
    superficie = superficie // contador
    return {'prom_poblacion': poblacion, 'prom_superficie': superficie}

def poblacion_maxima_minima(lista_paises):
    listado_poblacion = []

    for pais in lista_paises:
        for key, value in pais.items():
            if key == 'poblacion':
                listado_poblacion.append(int(value))
        
    for pais in lista_paises:
        if pais['poblacion'] == str(max(listado_poblacion)):
            print(pais['nombre'], pais['poblacion'],"- Mayor")

        if pais['poblacion'] == str(min(listado_poblacion)):
            print(pais['nombre'], pais['poblacion'], "- Menor")


def paises_continente(lista_paises):
    paises_por_continente = {}
    for pais in lista_paises: 
        continente = pais['continente'].title()
        if continente in paises_por_continente:
            paises_por_continente[continente] += 1
        else:
            paises_por_continente[continente] = 1

    for nombre, valor in paises_por_continente.items():
        print(f"{nombre}: {valor}")


#LOGICA MENU
def mostrar_paises(lista_paises):
    print("Listado de países")
    try:
        if lista_paises == 0:
            raise ValueError("No hay países guardados")
        
        for pais in lista_paises:
            print(f"Nombre: {pais['nombre']} - Continente: {pais['continente']} - Población: {pais['poblacion']} - Superficie: {pais['superficie']} km²")
    except ValueError as error:
        print(f"Error: {error}")
    print()

def agregar_nuevo(lista_paises):
    print("Agregar Nuevo Pais")
    try:
        nombre = busqueda_pais(lista_paises, "agregar")
        if len(nombre[0]) > 0:
            raise ValueError("Ya existe un país con el nombre ingresado")
        
        poblacion = input("Ingrese la población: ")
        validacion_numerica(poblacion)
        superficie = input("Ingrese la superficie: ")
        validacion_numerica(superficie)
        continente = input("Ingrese el continente: ")
        validacion_de_textos(continente)

        nuevo_pais = {'nombre': nombre[1], 'poblacion': poblacion, 'superficie': superficie, 'continente': continente}
        lista_paises.append(nuevo_pais)
    except ValueError as error:
        print(f"Error: {error}")
    print()

def buscar_pais(lista_paises):
    print("Buscar País")
    try:
        resultado = busqueda_pais(lista_paises, "buscar")
        
        if len(resultado[0]) == 0:
            raise ValueError(f"No se encontraron resultados para el país {resultado[1]}")
        
        print(f"Resultados para {resultado[1]}")
        for pais in resultado[0]:
            print(f"Nombre: {pais['nombre']} - Continente: {pais['continente']} - Población: {pais['poblacion']} - Superficie: {pais['superficie']} km²")
    except ValueError as error:
        print(f"Error: {error}")
    print()


def actualizar_datos_pais(lista_paises):
    print("Actualización de datos")
    try:
        resultado = busqueda_pais(lista_paises, "actualizar")
        paises = resultado[0]

        if len(paises) == 0:
            raise ValueError(f"No se encontraron resultados del país {resultado[1]}")
        
        if len(paises) > 1:
            print(f"Se encontró mas de un pais para {resultado[1]}")
            for pais in paises:
                print(pais['nombre'])
            resultado = busqueda_pais(lista_paises, "actualizar")
            paises = resultado[0]

        if len(paises) == 1:
            pais = paises[0]
            print(f"Actualizar datos del pais {pais['nombre']}")
            
            poblacion = input("Ingrese el nuevo valor de población: ")
            validacion_numerica(poblacion)
            superficie = input("Ingrese el nuevo valor de superficie: ")
            validacion_numerica(superficie)

            pais['poblacion'] = poblacion
            pais['superficie'] = superficie
        else:
            print("No se encontro el país que desea actualizar")
    except ValueError as error:
        print(f"Error: {error}")
    print()

def menu_filtrar(lista_paises):
    print("Filtrar Países")
    print(OPCIONES_FILTRAR)
    opcion = input("Eliga una opción: ")
    paises = []

    try:
        if validar_opcion_menu(opcion, 3):
            if opcion == "1":
                paises = filtrar_paises(lista_paises)
            if opcion == "2":
                paises = filtar_paises_rango(lista_paises, 'poblacion')
            if opcion == "3":
                paises = filtar_paises_rango(lista_paises, 'superficie')

            if len(paises) == 0:
                print("No se encontraron países para el filtro")
            else:
                for pais in paises:
                    print(f"Nombre: {pais['nombre']} - Continente: {pais['continente']} - Población: {pais['poblacion']} - Superficie: {pais['superficie']} km²")
    except ValueError as error:
        print(f"Error: {error}")
    print()

def menu_ordenar(lista_paises):
    print("Ordenar Países")
    print(OPCIONES_ORDENAR)
    opcion = input("Eliga una opción: ")
    paises = []
    try:
        if validar_opcion_menu(opcion, 3):
            if opcion == "1":
                print("Países ordenados alfabéticamente")
                paises = ordenar_paises(lista_paises, 'nombre')
            if opcion == "2":
                print("Países ordenados por población")
                paises = ordenar_paises(lista_paises, 'poblacion')
            if opcion == "3":
                print("1. Ascendente \n2. Descedente")
                valor = input("Elige como ordenar: ")
                if validar_opcion_menu(valor, 2):
                    print(f"Países ordenados por superficie {"ascendente" if valor == "1" else "descendente"}")
                    paises = ordenar_paises(lista_paises, 'superficie', False if valor == "1" else True)
            
            if len(paises) == 0:
                print("No se encontraron países para ordenar")
            else:
                for pais in paises:
                    print(f"Nombre: {pais['nombre']} - Continente: {pais['continente']} - Población: {pais['poblacion']} - Superficie: {pais['superficie']} km²")
    except ValueError as error:
        print(f"Error: {error}")
    print()

def mostrar_estadisticas(lista_paises):
    print("Estadisticas")
    print()
    print("País con mayor y menor población:")
    poblacion_maxima_minima(lista_paises)
    print()
    print("Promedio de población:", calcular_promedio(lista_paises)['prom_poblacion'])
    print("Promedio de superficie en km²:", calcular_promedio(lista_paises)['prom_superficie'])
    print()
    print("Cantidad de países por continente:")
    paises_continente(lista_paises)
    print()



def menu_principal():
    listado_paises = lectura_inicial_de_datos()
    mostrar_menu = True

    print("--- BIENVENIDO AL GESTOR DE PAÍSES ---")
    while mostrar_menu:
        print("Elige una opción del menú")
        print(OPCIONES_MENU)
        opcion = input("opción: ")

        if validar_opcion_menu(opcion, 8):
            if opcion == "1":
                mostrar_paises(listado_paises)
            elif opcion == "2":
                agregar_nuevo(listado_paises)
            elif opcion == "3":
                actualizar_datos_pais(listado_paises)
            elif opcion == "4":
                buscar_pais(listado_paises)
            elif opcion == "5":
                menu_filtrar(listado_paises)
            elif opcion == "6":
                menu_ordenar(listado_paises)
            elif opcion == "7":
                mostrar_estadisticas(listado_paises)
            elif opcion == "8":
                guardado_de_datos(listado_paises)
                print("Cerrando sistema!")
                break

menu_principal()
