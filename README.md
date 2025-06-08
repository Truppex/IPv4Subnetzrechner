# Subnetzrechner (SubCalc)

Ein deutschsprachiger Subnetzrechner für IPv4, geschrieben in Python.  
Mit diesem Tool kannst du Netzadressen, Subnetzmasken, Broadcasts und Hostbereiche für beliebige Netze berechnen –
egal ob mit gleich großen oder unterschiedlich großen Subnetzen (VLSM).
Perfekt für Schule, Ausbildung, Studium oder eigene Netzwerkprojekte.

---

## Features

- Berechnet Subnetze für beliebige IPv4-Adressen und Präfixe
- Unterstützt klassisches Subnetting **und** VLSM (Variable Subnetzgrößen)
- Sichert die Eingaben ab (keine ungültigen IPs oder Präfixe möglich)
- Jederzeit mit `exit` abbrechbar
- Alle Ausgaben auf Deutsch
- Klar strukturierter Python-Code, verständlich kommentiert

---

## Installation & Nutzung

1. **Voraussetzung:**  
   Python 3 muss installiert sein (Download: [python.org](https://www.python.org/downloads/))

2. **Repository klonen:**  
   ```sh
   git clone https://github.com/Truppex/IPv4Subnetzrechner.git
   cd IPv4Subnetzrechner
   ```

3. **Programm starten:**  
   ```sh
   python3 SubCalc.py
   ```

---

## Bedienung

- **Basisnetzadresse eingeben:**  
  Beispiel: `192.168.1.0`
- **Präfix eingeben:**  
  Beispiel: `24` für /24
- **VLSM-Modus:**  
  Wähle, ob du unterschiedlich große Subnetze benötigst.
- **Subnetze & Hosts:**  
  Gib die Anzahl der Subnetze (und ggf. Hosts pro Subnetz) an.
- **Beenden:**  
  Mit `exit` kann das Programm an jeder Eingabestelle beendet werden.

---

## Beispiel

```
Basisnetzadresse eingeben (z.B. 192.168.0.0): 10.1.0.0
Präfix eingeben (z.B. 24 für /24): 24
Willst du VLSM (verschiedene Hostgrößen) benutzen? (j/n): j
Wie viele Subnetze brauchst du?: 2
  Hosts im Subnetz 1: 50
  Hosts im Subnetz 2: 10

Subnetz 1:
  Netzadresse: 10.1.0.0
  Subnetzmaske: 255.255.255.192 /26
  Broadcast: 10.1.0.63
  Hostbereich: 10.1.0.1 - 10.1.0.62
  Maximale Hosts: 62
  Hosts (gewünscht): 50

Subnetz 2:
  Netzadresse: 10.1.0.64
  Subnetzmaske: 255.255.255.240 /28
  Broadcast: 10.1.0.79
  Hostbereich: 10.1.0.65 - 10.1.0.78
  Maximale Hosts: 14
  Hosts (gewünscht): 10
```

---

## Hinweise

- Das Programm eignet sich besonders gut als Lernhilfe oder für die IT-Ausbildung.
- Kommentare und Variablennamen sind bewusst einfach und auf Deutsch gehalten.

---

## Lizenz und Copyright

Copyright (c) 2025 Truppex

Dieses Projekt steht unter der MIT-Lizenz.

---

> **Hinweis:** Diese README wurde mit Hilfe von KI (AI) erstellt.
