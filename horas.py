"""
Tasca 6 d'APA Part 2
Nom: Sara Lario
"""

import re

PATRO_GLOBAL = re.compile(
    r"\b(\d{1,2}):(\d{1,2})\b|"
    r"\b(\d{1,2})h(?:(\d{1,2})m?)?\b|"
    r"\b(\d{1,2})(?:\s+(y media|y cuarto|menos cuarto|en punto))?(?:\s+(?:de la\s+(mañana|tarde|noche|madrugada)|del\s+(mediodía)))?\b"
)

def processa_match(match):
    text_original = match.group(0)
    
    # --- CAS 1: Format HH:MM ---
    if match.group(1) is not None:
        hora = int(match.group(1))
        min_str = match.group(2)
        if len(min_str) != 2: 
            return text_original  # '17:5' incorrecte
        minuts = int(min_str)
        if hora > 23 or minuts > 59: 
            return text_original
        return f"{hora:02d}:{minuts:02d}"

    # --- CAS 2: Format XhXXm o Xh ---
    elif match.group(3) is not None:
        hora = int(match.group(3))
        min_str = match.group(4)
        minuts = int(min_str) if min_str else 0
        if hora > 23 or minuts > 59: 
            return text_original
        return f"{hora:02d}:{minuts:02d}"

    # --- CAS 3: Format Parlat (Text i/o Franges) ---
    elif match.group(5) is not None:
        hora = int(match.group(5))
        modificador = match.group(6)
        
        # Recuperem la franja manualment buscant el text final del match original
        franja = None
        if "mañana" in text_original: franja = "mañana"
        elif "tarde" in text_original: franja = "tarde"
        elif "noche" in text_original: franja = "noche"
        elif "madrugada" in text_original: franja = "madrugada"
        elif "mediodía" in text_original: franja = "mediodía"

        # Si no hi ha modificador ni tampoc franja, no és una hora (ex: "7 puertas")
        if not modificador and not franja:
            return text_original

        minuts = 0
        if modificador == "y cuarto": minuts = 15
        elif modificador == "y media": minuts = 30
        elif modificador == "menos cuarto":
            minuts = 45
            hora -= 1
            if hora == 0: hora = 12
        elif modificador == "en punto":
            minuts = 0

        if franja:
            # El rellotge amb franja de text NOMÉS accepta de l'1 al 12 (Ex: "17 de la tarde" és INCORRECTE)
            if hora < 1 or hora > 12: 
                return text_original
            
            # Validacions semàntiques estrictes de l'enunciat
            if franja == "mañana" and not (4 <= hora <= 12): return text_original
            if franja == "mediodía" and not (12 <= hora <= 3 or hora == 1): return text_original
            if franja == "tarde" and not (3 <= hora <= 8): return text_original
            if franja == "noche" and not (8 <= hora <= 12 or 1 <= hora <= 4): return text_original
            if franja == "madrugada" and not (1 <= hora <= 6): return text_original

            # Conversió real a sistema 24h
            if franja in ["tarde", "mediodía"] and hora != 12:
                hora += 12
            elif franja == "noche":
                if hora == 12: hora = 0
                elif 1 <= hora <= 4: pass
                else: hora += 12
            elif franja == "mañana" and hora == 12:
                hora = 12
            elif franja == "madrugada" and hora == 12:
                hora = 0
        else:
            # Si és format parlat pur sense franja (ex: "4 y media" o "23 en punto")
            # El rellotge ha de començar en 1 i acabar a 12. "23 en punto" és INCORRECTE.
            if hora < 1 or hora > 12:
                return text_original
            if hora == 12: 
                hora = 0

        if hora < 0: hora += 24
        return f"{hora:02d}:{minuts:02d}"

    return text_original

def normalizaHoras(ficText, ficNorm):
    """
    Llegeix el fitxer ficText, analitza en busca d'expressions horàries 
    i escriu el fitxer ficNorm normalitzat.
    """
    # 1. Llegim el fitxer que ens demanin des de la variable 'ficText'
    with open(ficText, 'r', encoding='utf-8') as f_entrada:
        texto = f_entrada.read()
        
    # 2. Apliquem el teu patró intel·ligent a tot el text
    texto_transformado = PATRO_GLOBAL.sub(processa_match, texto)
    
    # 3. Guardem el resultat al nom de fitxer que contingui 'ficNorm'
    with open(ficNorm, 'w', encoding='utf-8') as f_sortida:
        f_sortida.write(texto_transformado)


if __name__ == "__main__":
    print("Normalitzant el fitxer horas.txt amb la lògica de la Sara...")
    normalizaHoras('horas.txt', 'horas_normalizadas.txt')
    print("Fet! S'ha generat 'horas_normalizadas.txt' perfectament.")