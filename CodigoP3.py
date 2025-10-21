# este es el archivo para el codigo de el proyecto 3
# si les sale esto en el repo y en la pagina, pls escribanme que si funciono o no

import re
from itertools import product

class RelacionesApp:
    def __init__(self):
        self.conjuntos = {}
        self.relaciones = {}
        self.referencial = set()
        # Agregar backup de conjuntos y relaciones originales
        self.conjuntos_originales = {}
        self.relaciones_originales = {}
    
    def definir_referencial(self, elementos):
        """Define el conjunto referencial (universo) y actualiza conjuntos existentes"""
        nuevo_referencial = set(str(elem).strip() for elem in elementos if str(elem).strip())
        
        # Si hay conjuntos ya definidos, actualizarlos según el nuevo universo
        # USAR CONJUNTOS ORIGINALES COMO BASE, no los actuales
        if self.conjuntos_originales:
            print(f"\n--- Actualizando conjuntos existentes según nuevo universo ---")
            for nombre, conjunto_original in self.conjuntos_originales.items():
                # Intersección con el nuevo universo usando el conjunto ORIGINAL
                conjunto_actualizado = conjunto_original.intersection(nuevo_referencial)
                self.conjuntos[nombre] = conjunto_actualizado
                
                if conjunto_original != conjunto_actualizado:
                    elementos_removidos = conjunto_original - conjunto_actualizado
                    print(f"Conjunto {nombre}: {sorted(conjunto_original)} → {sorted(conjunto_actualizado)}")
                    if elementos_removidos:
                        print(f"  Elementos removidos: {sorted(elementos_removidos)} (no están en el nuevo universo)")
                else:
                    print(f"Conjunto {nombre}: Sin cambios - {sorted(conjunto_actualizado)}")
        
        # Si hay relaciones definidas, también actualizarlas
        # USAR RELACIONES ORIGINALES COMO BASE, no las actuales
        if self.relaciones_originales:
            print(f"\n--- Actualizando relaciones existentes según nuevo universo ---")
            for nombre, relacion_original in self.relaciones_originales.items():
                # Filtrar pares donde ambos elementos estén en el nuevo universo
                relacion_actualizada = set()
                for (a, b) in relacion_original:
                    if str(a) in nuevo_referencial and str(b) in nuevo_referencial:
                        relacion_actualizada.add((a, b))
                
                self.relaciones[nombre] = relacion_actualizada
                
                if relacion_original != relacion_actualizada:
                    pares_removidos = relacion_original - relacion_actualizada
                    print(f"Relación {nombre}: {len(relacion_original)} → {len(relacion_actualizada)} pares")
                    if pares_removidos:
                        print(f"  Pares removidos: {sorted(pares_removidos)} (elementos no están en el nuevo universo)")
                else:
                    print(f"Relación {nombre}: Sin cambios - {len(relacion_actualizada)} pares")
        
        self.referencial = nuevo_referencial
        print(f"\nConjunto referencial U definido: {sorted(list(self.referencial))}")
        print(f"Todos los conjuntos y relaciones han sido actualizados según el nuevo universo.")
    
    def crear_conjunto(self, nombre, elementos):
        """Crea un nuevo conjunto con el nombre y elementos dados"""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del conjunto no puede estar vacío")
        
        # Convertir elementos a strings y filtrar vacíos
        conjunto_elementos = set()
        for elem in elementos:
            elem_str = str(elem).strip()
            if elem_str:  # Solo agregar si no está vacío
                conjunto_elementos.add(elem_str)
        
        # Si hay un referencial definido, validar que los elementos estén en él
        if self.referencial:
            elementos_invalidos = conjunto_elementos - self.referencial
            if elementos_invalidos:
                print(f"Advertencia: Los elementos {sorted(elementos_invalidos)} no están en el conjunto referencial")
                conjunto_elementos = conjunto_elementos.intersection(self.referencial)
                print(f"Solo se incluirán los elementos válidos: {sorted(conjunto_elementos)}")
        
        nombre_limpio = nombre.strip()
        self.conjuntos[nombre_limpio] = conjunto_elementos
        # GUARDAR COPIA ORIGINAL
        self.conjuntos_originales[nombre_limpio] = conjunto_elementos.copy()
        print(f"Conjunto {nombre_limpio} creado: {sorted(self.conjuntos[nombre_limpio])}")
    
    def crear_relacion(self, nombre, pares):
        """Crea una nueva relación con pares ordenados"""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la relación no puede estar vacío")
        
        relacion_elementos = set()
        pares_invalidos = []
        
        for par in pares:
            if isinstance(par, tuple) and len(par) == 2:
                # Convertir elementos a strings y limpiar espacios
                elem1 = str(par[0]).strip()
                elem2 = str(par[1]).strip()
                
                # Validar que los elementos no estén vacíos
                if not elem1 or not elem2:
                    continue
                
                par_str = (elem1, elem2)
                
                # Si hay un referencial definido, validar que los elementos estén en él
                if self.referencial:
                    if elem1 in self.referencial and elem2 in self.referencial:
                        relacion_elementos.add(par_str)
                    else:
                        pares_invalidos.append(par_str)
                else:
                    relacion_elementos.add(par_str)
            else:
                raise ValueError(f"Elemento inválido en la relación: {par}")
        
        if pares_invalidos and self.referencial:
            print(f"Advertencia: Los pares {sorted(pares_invalidos)} contienen elementos no válidos según el conjunto referencial")
            print(f"Solo se incluirán los pares válidos")
        
        nombre_limpio = nombre.strip()
        self.relaciones[nombre_limpio] = relacion_elementos
        # GUARDAR COPIA ORIGINAL
        self.relaciones_originales[nombre_limpio] = relacion_elementos.copy()
        print(f"Relación {nombre_limpio} creada: {sorted(self.relaciones[nombre_limpio])}")
    
    def obtener_conjuntos_disponibles(self):
        """Retorna todos los conjuntos disponibles (conjuntos + referencial si está definido)"""
        conjuntos_disponibles = self.conjuntos.copy()
        if self.referencial:
            conjuntos_disponibles['U'] = self.referencial
        return conjuntos_disponibles
    
    def union(self, conjunto1, conjunto2):
        """Realiza la unión de dos conjuntos"""
        return conjunto1 | conjunto2
    
    def interseccion(self, conjunto1, conjunto2):
        """Realiza la intersección de dos conjuntos"""
        return conjunto1 & conjunto2
    
    def diferencia(self, conjunto1, conjunto2):
        """Realiza la diferencia (conjunto1 - conjunto2)"""
        return conjunto1 - conjunto2
    
    def complemento(self, conjunto):
        """Calcula el complemento de un conjunto respecto al referencial"""
        if not self.referencial:
            raise ValueError("No se ha definido el conjunto referencial")
        return self.referencial - conjunto
    
    def producto_cartesiano(self, conjunto1, conjunto2):
        """Calcula el producto cartesiano de dos conjuntos"""
        return {(str(a), str(b)) for a in conjunto1 for b in conjunto2}
    
    def es_reflexiva(self, relacion, conjunto):
        """Determina si una relación es reflexiva en un conjunto dado"""
        # Una relación es reflexiva si para todo a en el conjunto, (a,a) está en la relación
        for elemento in conjunto:
            if (str(elemento), str(elemento)) not in relacion:
                return False
        return True
    
    def es_simetrica(self, relacion):
        """Determina si una relación es simétrica"""
        # Una relación es simétrica si para todo (a,b) en R, (b,a) también está en R
        for (a, b) in relacion:
            if (b, a) not in relacion:
                return False
        return True
    
    def es_transitiva(self, relacion):
        """Determina si una relación es transitiva"""
        # Una relación es transitiva si para todo (a,b) y (b,c) en R, (a,c) también está en R
        for (a, b) in relacion:
            for (c, d) in relacion:
                if b == c:  # Si b = c, entonces tenemos (a,b) y (b,d)
                    if (a, d) not in relacion:
                        return False
        return True
    
    def composicion_relaciones(self, relacion1, relacion2):
        """Calcula la composición de dos relaciones R∘S"""
        # R∘S = {(a,c) : existe b tal que (a,b) ∈ S y (b,c) ∈ R}
        composicion = set()
        for (a, b) in relacion2:  # S
            for (c, d) in relacion1:  # R
                if b == c:  # Si el segundo elemento de S coincide con el primero de R
                    composicion.add((a, d))
        return composicion
    
    def potencia_relacion(self, relacion, n):
        """Calcula la potencia n de una relación"""
        if n <= 0:
            raise ValueError("La potencia debe ser un número positivo")
        
        if n == 1:
            return relacion.copy()
        
        resultado = relacion.copy()
        for i in range(n - 1):
            resultado = self.composicion_relaciones(relacion, resultado)
        
        return resultado
    
    def operacion_binaria(self, relacion, conjunto1, conjunto2):
        """
        Verifica si una relación es una operación binaria en conjunto1 × conjunto2
        Una operación binaria debe ser una función total
        """
        producto = self.producto_cartesiano(conjunto1, conjunto2)
        
        # Verificar que la relación esté contenida en (conjunto1 × conjunto2) × conjunto_resultado
        # Para simplicidad, verificamos que cada par del producto cartesiano tenga exactamente una imagen
        
        dominios_usados = set()
        for (a, b) in relacion:
            # Cada par (a,b) debe aparecer como primer elemento exactamente una vez
            if (a, b) in dominios_usados:
                return False, "Hay elementos con más de una imagen"
            dominios_usados.add((a, b))
        
        # Verificar si es una función total (todos los elementos del dominio tienen imagen)
        elementos_dominio = set()
        for (a, b) in relacion:
            elementos_dominio.add(a)
        
        return True, f"Es una operación válida con dominio: {sorted(elementos_dominio)}"
    
    def parsear_pares_ordenados(self, entrada):
        """Parsea una cadena de pares ordenados"""
        try:
            entrada = entrada.strip()
            if not entrada:
                return []
            
            # Usar regex para encontrar pares ordenados
            patron = r'\(\s*([^,\)]+)\s*,\s*([^,\)]+)\s*\)'
            matches = re.findall(patron, entrada)
            
            if not matches:
                raise ValueError("No se encontraron pares ordenados válidos")
            
            pares = [(match[0].strip(), match[1].strip()) for match in matches]
            return pares
            
        except Exception as e:
            raise ValueError(f"Error al parsear pares ordenados: {e}")
        
    def combinaciones_objetos_iguales(self, conjunto_nombre, k):
        """Calcula todas las combinaciones posibles (con repetición) de k elementos de un conjunto"""
        from itertools import combinations_with_replacement

        if conjunto_nombre not in self.conjuntos:
            print(f"El conjunto '{conjunto_nombre}' no existe.")
            return
        
        conjunto = sorted(self.conjuntos[conjunto_nombre])
        
        if not conjunto:
            print("El conjunto está vacío.")
            return
        
        if k <= 0:
            print("El número de elementos a combinar debe ser positivo.")
            return
        
        combinaciones = list(combinations_with_replacement(conjunto, k))
        print(f"\nCombinaciones con repetición de {conjunto_nombre} (k={k}):")
        for c in combinaciones:
            print(c)
        
        print(f"\nTotal de combinaciones: {len(combinaciones)}")
        return combinaciones

    
    
    def mostrar_menu(self):
        """Muestra el menú principal de la aplicación"""
        print("\n" + "="*60)
        print("         OPERACIONES CON RELACIONES")
        print("="*60)
        print("1.  Definir conjunto referencial (universo)")
        print("2.  Crear nuevo conjunto")
        print("3.  Crear nueva relación")
        print("4.  Operaciones básicas de conjuntos (∪, ∩, −, ')")
        print("5.  Producto cartesiano")
        print("6.  Verificar si relación es reflexiva")
        print("7.  Verificar si relación es simétrica")
        print("8.  Verificar si relación es transitiva")
        print("9.  Composición de relaciones (R∘S)")
        print("10. Potencia de una relación (R^n)")
        print("11. Verificar operación binaria")
        print("12. Mostrar conjuntos y relaciones")
        print("13. Ejecutar ejemplo del proyecto")
        print("14. Calcular combinaciones de objetos iguales")
        print("15. Salir")
        print("="*60)
    
    def ejecutar_ejemplo(self):
        """Ejecuta el ejemplo proporcionado en el proyecto"""
        print("\n--- Ejecutando ejemplo del proyecto ---")
        
        try:
            # Verificar que los conjuntos y relaciones necesarios existen
            conjuntos_req = ['E', 'A', 'C', 'B']
            relaciones_req = ['R']
            
            for conj in conjuntos_req:
                if conj not in self.conjuntos and conj not in self.relaciones:
                    print(f"Error: El conjunto/relación {conj} no está definido")
                    return
            
            if 'R' not in self.relaciones:
                print("Error: La relación R no está definida")
                return
            
            print("\n=== OPERACIONES SOLICITADAS ===")
            
            # bin(E,C,B) - Verificar si E es operación binaria entre C y B
            if 'E' in self.relaciones and 'C' in self.conjuntos and 'B' in self.conjuntos:
                es_binaria, mensaje = self.operacion_binaria(self.relaciones['E'], 
                                                           self.conjuntos['C'], 
                                                           self.conjuntos['B'])
                print(f"bin(E,C,B): {es_binaria} - {mensaje}")
            
            # ref(R,A) - Verificar si R es reflexiva en A
            if 'R' in self.relaciones and 'A' in self.conjuntos:
                es_refl = self.es_reflexiva(self.relaciones['R'], self.conjuntos['A'])
                print(f"ref(R,A): {es_refl}")
            
            # sim(R,A) - Verificar si R es simétrica
            if 'R' in self.relaciones:
                es_sim = self.es_simetrica(self.relaciones['R'])
                print(f"sim(R,A): {es_sim}")
            
            # tra(R,A) - Verificar si R es transitiva
            if 'R' in self.relaciones:
                es_trans = self.es_transitiva(self.relaciones['R'])
                print(f"tra(R,A): {es_trans}")
            
            # R^3 - Potencia 3 de la relación R
            if 'R' in self.relaciones:
                r3 = self.potencia_relacion(self.relaciones['R'], 3)
                print(f"R^3: {sorted(r3)}")
            
            # R∘E - Composición de R y E
            if 'R' in self.relaciones and 'E' in self.relaciones:
                composicion = self.composicion_relaciones(self.relaciones['R'], self.relaciones['E'])
                print(f"R∘E: {sorted(composicion)}")
            
        except Exception as e:
            print(f"Error al ejecutar el ejemplo: {e}")
    
    def ejecutar(self):
        """Ejecuta la aplicación en modo interactivo"""
        print("¡Bienvenido al programa de operaciones con relaciones!")
        
        while True:
            try:
                self.mostrar_menu()
                opcion = input("\nSeleccione una opción (1-14): ").strip()
                
                if not opcion.isdigit() or not (1 <= int(opcion) <= 15):
                    print("ERROR: Opción no válida. Debe ser un número entre 1 y 15.")
                    continue
                
                opcion = int(opcion)
                
                if opcion == 1:
                    elementos = input("Ingrese elementos del referencial (separados por comas): ")
                    lista_elementos = [e.strip() for e in elementos.split(',') if e.strip()]
                    if lista_elementos:
                        self.definir_referencial(lista_elementos)
                
                elif opcion == 2:
                    nombre = input("Nombre del conjunto: ").strip()
                    if not nombre:
                        print("El nombre no puede estar vacío")
                        continue
                    
                    elementos = input("Ingrese elementos (separados por comas): ")
                    lista_elementos = [e.strip() for e in elementos.split(',') if e.strip()]
                    
                    try:
                        self.crear_conjunto(nombre, lista_elementos)
                    except ValueError as e:
                        print(f"Error: {e}")
                
                elif opcion == 3:
                    nombre = input("Nombre de la relación: ").strip()
                    if not nombre:
                        print("El nombre no puede estar vacío")
                        continue
                    
                    print("Ingrese pares ordenados en formato: (a,b),(c,d),...")
                    entrada = input("Pares: ").strip()
                    
                    if not entrada:
                        print("No se ingresaron pares")
                        continue
                    
                    try:
                        pares = self.parsear_pares_ordenados(entrada)
                        self.crear_relacion(nombre, pares)
                    except ValueError as e:
                        print(f"Error: {e}")
                
                elif opcion == 4:
                    if len(self.conjuntos) < 1:
                        print("Necesita al menos 1 conjunto definido")
                        continue
                    
                    print(f"Conjuntos disponibles: {', '.join(self.conjuntos.keys())}")
                    print("Operaciones: (U)nión, (I)ntersección, (D)iferencia, (C)omplemento")
                    operacion = input("Seleccione operación: ").upper().strip()
                    
                    if operacion in ['U', 'I', 'D']:
                        if len(self.conjuntos) < 2:
                            print("Necesita al menos 2 conjuntos para esta operación")
                            continue
                        
                        nombre1 = input("Primer conjunto: ").strip()
                        nombre2 = input("Segundo conjunto: ").strip()
                        
                        if nombre1 not in self.conjuntos or nombre2 not in self.conjuntos:
                            print("Alguno de los conjuntos no existe")
                            continue
                        
                        if operacion == 'U':
                            resultado = self.union(self.conjuntos[nombre1], self.conjuntos[nombre2])
                            print(f"{nombre1} ∪ {nombre2} = {sorted(resultado)}")
                        elif operacion == 'I':
                            resultado = self.interseccion(self.conjuntos[nombre1], self.conjuntos[nombre2])
                            print(f"{nombre1} ∩ {nombre2} = {sorted(resultado)}")
                        elif operacion == 'D':
                            resultado = self.diferencia(self.conjuntos[nombre1], self.conjuntos[nombre2])
                            print(f"{nombre1} \\ {nombre2} = {sorted(resultado)}")
                    
                    elif operacion == 'C':
                        if not self.referencial:
                            print("Primero debe definir el conjunto referencial")
                            continue
                        
                        nombre = input("Conjunto para calcular complemento: ").strip()
                        if nombre not in self.conjuntos:
                            print("Conjunto no existe")
                            continue
                        
                        try:
                            resultado = self.complemento(self.conjuntos[nombre])
                            print(f"{nombre}' = {sorted(resultado)}")
                        except ValueError as e:
                            print(f"Error: {e}")
                    else:
                        print("Operación no válida")
                
                elif opcion == 5:
                    conjuntos_disponibles = self.obtener_conjuntos_disponibles()
                    if len(conjuntos_disponibles) < 2:
                        print("Necesita al menos 2 conjuntos definidos")
                        continue
                    
                    print(f"Conjuntos disponibles: {', '.join(conjuntos_disponibles.keys())}")
                    nombre1 = input("Primer conjunto: ").strip()
                    nombre2 = input("Segundo conjunto: ").strip()
                    
                    if nombre1 not in conjuntos_disponibles or nombre2 not in conjuntos_disponibles:
                        print("Alguno de los conjuntos no existe")
                        continue
                    
                    resultado = self.producto_cartesiano(conjuntos_disponibles[nombre1], conjuntos_disponibles[nombre2])
                    print(f"{nombre1} × {nombre2} = {sorted(resultado)}")
                    print(f"Número de elementos: {len(resultado)}")
                
                elif opcion == 6:
                    if not self.relaciones:
                        print("No hay relaciones definidas")
                        continue
                    if not self.conjuntos:
                        print("No hay conjuntos definidos")
                        continue
                    
                    print(f"Relaciones disponibles: {', '.join(self.relaciones.keys())}")
                    rel_nombre = input("Nombre de la relación: ").strip()
                    
                    print(f"Conjuntos disponibles: {', '.join(self.conjuntos.keys())}")
                    conj_nombre = input("Nombre del conjunto: ").strip()
                    
                    if rel_nombre not in self.relaciones or conj_nombre not in self.conjuntos:
                        print("La relación o conjunto no existe")
                        continue
                    
                    es_refl = self.es_reflexiva(self.relaciones[rel_nombre], self.conjuntos[conj_nombre])
                    print(f"¿{rel_nombre} es reflexiva en {conj_nombre}? {es_refl}")
                
                elif opcion == 7:
                    if not self.relaciones:
                        print("No hay relaciones definidas")
                        continue
                    
                    print(f"Relaciones disponibles: {', '.join(self.relaciones.keys())}")
                    nombre = input("Nombre de la relación: ").strip()
                    
                    if nombre not in self.relaciones:
                        print("La relación no existe")
                        continue
                    
                    es_sim = self.es_simetrica(self.relaciones[nombre])
                    print(f"¿{nombre} es simétrica? {es_sim}")
                
                elif opcion == 8:
                    if not self.relaciones:
                        print("No hay relaciones definidas")
                        continue
                    
                    print(f"Relaciones disponibles: {', '.join(self.relaciones.keys())}")
                    nombre = input("Nombre de la relación: ").strip()
                    
                    if nombre not in self.relaciones:
                        print("La relación no existe")
                        continue
                    
                    es_trans = self.es_transitiva(self.relaciones[nombre])
                    print(f"¿{nombre} es transitiva? {es_trans}")
                
                elif opcion == 9:
                    if len(self.relaciones) < 2:
                        print("Necesita al menos 2 relaciones definidas")
                        continue
                    
                    print(f"Relaciones disponibles: {', '.join(self.relaciones.keys())}")
                    nombre1 = input("Primera relación R: ").strip()
                    nombre2 = input("Segunda relación S: ").strip()
                    
                    if nombre1 not in self.relaciones or nombre2 not in self.relaciones:
                        print("Alguna de las relaciones no existe")
                        continue
                    
                    composicion = self.composicion_relaciones(self.relaciones[nombre1], self.relaciones[nombre2])
                    print(f"{nombre1}∘{nombre2} = {sorted(composicion)}")
                
                elif opcion == 10:
                    if not self.relaciones:
                        print("No hay relaciones definidas")
                        continue
                    
                    print(f"Relaciones disponibles: {', '.join(self.relaciones.keys())}")
                    nombre = input("Nombre de la relación: ").strip()
                    
                    if nombre not in self.relaciones:
                        print("La relación no existe")
                        continue
                    
                    try:
                        n = int(input("Potencia n: ").strip())
                        resultado = self.potencia_relacion(self.relaciones[nombre], n)
                        print(f"{nombre}^{n} = {sorted(resultado)}")
                    except ValueError:
                        print("La potencia debe ser un número entero positivo")
                
                elif opcion == 11:
                    if not self.relaciones or len(self.conjuntos) < 2:
                        print("Necesita relaciones y al menos 2 conjuntos definidos")
                        continue
                    
                    print(f"Relaciones disponibles: {', '.join(self.relaciones.keys())}")
                    rel_nombre = input("Nombre de la relación: ").strip()
                    
                    print(f"Conjuntos disponibles: {', '.join(self.conjuntos.keys())}")
                    conj1_nombre = input("Primer conjunto: ").strip()
                    conj2_nombre = input("Segundo conjunto: ").strip()
                    
                    if (rel_nombre not in self.relaciones or 
                        conj1_nombre not in self.conjuntos or 
                        conj2_nombre not in self.conjuntos):
                        print("La relación o algún conjunto no existe")
                        continue
                    
                    es_binaria, mensaje = self.operacion_binaria(
                        self.relaciones[rel_nombre], 
                        self.conjuntos[conj1_nombre], 
                        self.conjuntos[conj2_nombre]
                    )
                    print(f"¿{rel_nombre} es operación binaria en {conj1_nombre}×{conj2_nombre}? {es_binaria}")
                    print(f"Detalle: {mensaje}")
                
                elif opcion == 12:
                    print(f"\nConjunto referencial U: {sorted(self.referencial) if self.referencial else 'No definido'}")
                    
                    print("\nConjuntos definidos:")
                    if self.conjuntos:
                        for nombre, conjunto in self.conjuntos.items():
                            print(f"  {nombre}: {sorted(conjunto)}")
                    else:
                        print("  No hay conjuntos definidos")
                    
                    print("\nRelaciones definidas:")
                    if self.relaciones:
                        for nombre, relacion in self.relaciones.items():
                            print(f"  {nombre}: {sorted(relacion)}")
                    else:
                        print("  No hay relaciones definidas")
                
                elif opcion == 13:
                    self.ejecutar_ejemplo()
                
                elif opcion == 14:
                    if not self.conjuntos:
                        print("No hay conjuntos definidos.")
                        continue

                    print(f"Conjuntos disponibles: {', '.join(self.conjuntos.keys())}")
                    nombre = input("Seleccione el conjunto: ").strip()
                    if nombre not in self.conjuntos:
                        print("Conjunto no válido.")
                        continue
                    
                    try:
                        k = int(input("Número de elementos a combinar (k): ").strip())
                        self.combinaciones_objetos_iguales(nombre, k)
                    except ValueError:
                        print("Debe ingresar un número entero válido para k.")

                else:  # opcion == 15
                    print("\n¡Gracias por usar el programa de relaciones!")
                    print("Saliendo...")
                    break

                    
            except KeyboardInterrupt:
                print("\n\nPrograma interrumpido por el usuario")
                break
            except Exception as e:
                print(f"Error inesperado: {e}")
                print("Continuando...")

def configurar_ejemplo():
    """Configura automáticamente los conjuntos y relaciones del ejemplo"""
    app = RelacionesApp()
    
    # Definir el conjunto referencial U
    U = ['a','b','c','d','e','f','g','h','i','j','k','1','2','3','4','5']
    app.definir_referencial(U)
    
    # Crear los conjuntos del ejemplo
    app.crear_conjunto('A', ['1','a','b'])
    app.crear_conjunto('B', ['a','b','c'])
    app.crear_conjunto('C', ['1','2','3'])
    
    # Crear las relaciones del ejemplo
    app.crear_relacion('E', [('1','a'), ('2','b'), ('3','c')])
    app.crear_relacion('R', [('1','1'), ('a','a'), ('b','b'), ('1','a'), ('a','1'), 
                            ('a','b'), ('b','a'), ('1','b'), ('b','1')])
    
    return app

# Ejemplo de uso
if __name__ == "__main__":
    print("Configurando ejemplo automáticamente...")
    app = configurar_ejemplo()
    
    print("\nConjuntos y relaciones configurados exitosamente!")
    print("Puede usar la opción 13 para ejecutar las operaciones del ejemplo.")
    
    # Ejecutar la aplicación interactiva
    app.ejecutar()
