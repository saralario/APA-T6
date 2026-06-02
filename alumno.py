"""
Tasca 6 d'APA
Nom: Sara Lario Garrido
"""

import re

class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'

def leeAlumnos(ficAlum):
    """
    llegeix un fitxer de text amb les dades dels alumnes i retorna un diccionari

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171\tBlanca Agirrebarrenetse\t9.5
    23\tCarles Balcell de Lara\t4.9
    68\tDavid Garcia Fuster\t7.0
    """
    diccionari_alumnes = {}
    
    # patró per separar: 1. número ID | 2. nom de l'alumne | 3. notes del final
    patro = re.compile(r"^\s*(\d+)\s+(.+?)\s+([\d.\s\t]+)$")

    with open(ficAlum, 'r', encoding='utf-8') as f:
        for linia in f:
            linia = linia.strip()
            if not linia:
                continue
            
            match = patro.match(linia)
            if match:
                num_iden = int(match.group(1))
                nombre = match.group(2).strip()
                notes_str = match.group(3)
                
                # busquem tots els números decimals o enters dins la secció de notes
                notes = [float(n) for n in re.findall(r"\d+\.\d+|\d+", notes_str)]
                
                # afegim l'alumne al diccionari utilitzant el seu nom com a clau
                diccionari_alumnes[nombre] = Alumno(nombre, num_iden, notes)
                
    return diccionari_alumnes


if __name__ == "__main__":
    print("--- Executant proves manuals ---")
    
    # 1. Cridem la funció per llegir el fitxer que acabem de crear
    try:
        meus_alumnes = leeAlumnos('alumnos.txt')
        
        # 2. Si ha trobat alumnes, els mostrem un a un per pantalla
        for nom in meus_alumnes:
            print(f"Alumne trobat: {nom}")
            print(f"Dades oficials: {meus_alumnes[nom]}")
            print("-" * 30)
            
    except FileNotFoundError:
        print("ERROR: No s'ha trobat el fitxer 'alumnos.txt'. Revisa que estigui a la mateixa carpeta!")

    print("\n--- Executant Doctest (Tests obligatoris) ---")
    # Executa els tests unitaris automàtics
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
    
