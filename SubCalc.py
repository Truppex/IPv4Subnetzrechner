# Subnetzrechner für IPv4-Adressen

# Funktion: IP-Adresse (als String) in eine Liste umwandeln
def ip_str_zu_liste(ip_str):
    teile = ip_str.strip().split('.')
    # Hab bei Google gesehen, dass ne IP 4 Blöcke braucht
    if len(teile) != 4:
        return None
    ip = []
    for block in teile:
        # Muss ne Zahl sein, sonst ists keine IP
        if not block.isdigit():
            return None
        zahl = int(block)
        # Jedes Oktett nur 0 bis 255, steht überall so
        if zahl < 0 or zahl > 255:
            return None
        ip.append(zahl)
    return ip

# Funktion: IP-Liste wieder in nen String machen
def ip_liste_zu_str(ip):
    return '.'.join(str(x) for x in ip)

# Aus Präfix (z.B. 24) wird Subnetzmaske (z.B. 255.255.255.0)
def präfix_zu_maske(präfix):
    maske = []
    rest_bits = präfix
    for i in range(4):
        if rest_bits >= 8:
            maske.append(255)
            rest_bits -= 8
        elif rest_bits > 0:
            maske.append(256 - 2 ** (8 - rest_bits))
            rest_bits = 0
        else:
            maske.append(0)
    return maske

# Funktion: Zu einer IP so und so viele Adressen draufrechnen, inkl. Übertrag (bei 256)
def addiere_zu_ip(ip, wert):
    ergebnis = ip[:]
    # von hinten nach vorne addieren (wegen Übertrag)
    for i in range(3, -1, -1):
        temp = ergebnis[i] + (wert % 256)
        ergebnis[i] = temp % 256
        # Das was über 255 geht ins nächste Oktett "tragen"
        wert = wert // 256 + temp // 256
    return ergebnis

# Wieviele Bits brauche ich für mindestens n Hosts/Subnetze (hab ich gegoogelt, 2^x >= n)
def benötigte_bits(n):
    bits = 0
    zahl = 1
    while zahl < n:
        zahl = zahl * 2
        bits += 1
    return bits

# Funktion zum Anzeigen von allen Infos zu einem Subnetz
def zeige_subnetz_info(netzadresse, präfix, größe, maske, nummer, hosts_gewünscht=None):
    print(f"\nSubnetz {nummer+1}:")
    print("  Netzadresse:", ip_liste_zu_str(netzadresse))
    print("  Subnetzmaske:", ip_liste_zu_str(maske), f"/{präfix}")
    # Broadcast ist letzte Adresse
    broadcast = addiere_zu_ip(netzadresse, größe - 1)
    print("  Broadcast:", ip_liste_zu_str(broadcast))
    if größe > 2:
        erster_host = addiere_zu_ip(netzadresse, 1)
        letzter_host = addiere_zu_ip(netzadresse, größe - 2)
        print("  Hostbereich:", ip_liste_zu_str(erster_host), "-", ip_liste_zu_str(letzter_host))
    else:
        print("  Kein Hostbereich, da zu klein (nur Punkt-zu-Punkt-Verbindung möglich)")
    print(f"  Maximale Hosts: {größe - 2 if größe > 2 else 0}")
    if hosts_gewünscht is not None:
        print(f"  Hosts (gewünscht): {hosts_gewünscht}")

# Funktion, die nach Ja oder Nein fragt (User kann auch mit "exit" abbrechen)
def frage_ja_nein(frage):
    while True:
        antwort = input(frage + " (j/n): ").strip().lower()
        if antwort == "exit":
            print("Programm beendet.")
            exit()
        if antwort.startswith(("j", "y")):
            return True
        if antwort.startswith("n"):
            return False
        print('Bitte "j" oder "y" für Ja oder "n" für Nein eingeben.')

# Hauptprogramm (eigentlich alles zusammen)
def main():
    print("IPv4 Subnetzrechner. Mit 'exit' kann man immer abbrechen.\n")

    # IP-Adresse abfragen, prüfen ob korrekt
    while True:
        ip_str = input("Basisnetzadresse eingeben (z.B. 192.168.0.0): ").strip()
        if ip_str.lower() == "exit":
            print("Programm beendet.")
            return
        basis_ip = ip_str_zu_liste(ip_str)
        if basis_ip is not None:
            break
        print("Ungültige IP-Adresse! Muss so aussehen: x.x.x.x und Werte von 0 bis 255.")

    # Präfix abfragen, prüfen ob Zahl zwischen 1 und 32
    while True:
        präfix_input = input("Präfix eingeben (z.B. 24 für /24): ").strip()
        if präfix_input.lower() == "exit":
            print("Programm beendet.")
            return
        if präfix_input.isdigit():
            präfix = int(präfix_input)
            if 1 <= präfix <= 32:
                break
        print("Präfix muss eine Zahl zwischen 1 und 32 sein!")

    # Nach VLSM fragen
    vlsm = frage_ja_nein("Willst du VLSM (verschiedene Hostgrößen) benutzen?")

    if vlsm:
        # Für jedes Subnetz Hostbedarf abfragen
        while True:
            wie_viele_input = input("Wie viele Subnetze brauchst du?: ").strip()
            if wie_viele_input.lower() == "exit":
                print("Programm beendet.")
                return
            if wie_viele_input.isdigit() and int(wie_viele_input) > 0:
                wie_viele = int(wie_viele_input)
                break
            print("Bitte eine positive Zahl eingeben.")
        host_wunsch_liste = []
        for i in range(wie_viele):
            while True:
                hosts_input = input(f"  Hosts im Subnetz {i+1}: ").strip()
                if hosts_input.lower() == "exit":
                    print("Programm beendet.")
                    return
                if hosts_input.isdigit() and int(hosts_input) > 0:
                    host_wunsch_liste.append(int(hosts_input))
                    break
                print("Bitte mindestens 1 Host und als Zahl eingeben.")
        # Größte Subnetze zuerst (damit Adressraum reicht)
        host_wunsch_liste.sort(reverse=True)
        aktuelle_ip = basis_ip[:]
        aktuelle_präfix = präfix
        noch_frei = 2 ** (32 - präfix)
        for idx, hostwunsch in enumerate(host_wunsch_liste):
            bits_needed = benötigte_bits(hostwunsch + 2)  # +2 für Netz/Broadcast
            subnet_präfix = 32 - bits_needed
            if subnet_präfix < aktuelle_präfix:
                print(f"Nicht genug Platz für Subnetz {idx+1}.")
                break
            subnet_größe = 2 ** bits_needed
            maske = präfix_zu_maske(subnet_präfix)
            zeige_subnetz_info(aktuelle_ip, subnet_präfix, subnet_größe, maske, idx, hostwunsch)
            aktuelle_ip = addiere_zu_ip(aktuelle_ip, subnet_größe)
            noch_frei -= subnet_größe
            if noch_frei < 0:
                print("Adressraum voll, keine weiteren Subnetze möglich.")
                break
    else:
        # Normales Subnetting, alle Subnetze gleich groß
        while True:
            wie_viele_input = input("Wie viele gleich große Subnetze willst du?: ").strip()
            if wie_viele_input.lower() == "exit":
                print("Programm beendet.")
                return
            if wie_viele_input.isdigit() and int(wie_viele_input) > 0:
                wie_viele = int(wie_viele_input)
                break
            print("Bitte eine positive Zahl eingeben.")
        hostbits_vorher = 32 - präfix
        subnet_bits = benötigte_bits(wie_viele)
        if subnet_bits > hostbits_vorher:
            print("Zu viele Subnetze für das Netz.")
            return
        neuer_präfix = präfix + subnet_bits
        maske = präfix_zu_maske(neuer_präfix)
        subnet_größe = 2 ** (32 - neuer_präfix)
        for i in range(wie_viele):
            netzadresse = addiere_zu_ip(basis_ip, i * subnet_größe)
            zeige_subnetz_info(netzadresse, neuer_präfix, subnet_größe, maske, i)

if __name__ == "__main__":
    main()
