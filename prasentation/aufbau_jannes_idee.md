# Präsentation Struktur/Aufbau

## 1 Motivation (Wie sind wir auf unser Thema gekommen)

### 1.1 Leistungskurse

    Beide Informatik LK, Physik Grundkurs -> Gemeinsamer Physikunterricht -> Schall als Thema

### 1.2 Jannes Projekt

    Jannes Projekt: Soundvisualisierungs Brille; Gescheitert wegen zu schlechten technischen Möglichkeiten -> Übertragung von Konzept auf andere Bereiche -> GPS Tracking -> flache Ebene 2D Simulation

## 2 Unser Thema (Was ist unser Thema)

    Kurzfassung: Trilateration mit distanzen berechnet von Latenzen von Schallsignalen

### 2.1 GPS Tracking 

#### 2.1.1 Grundprinzip

    - Trilateration durch distanzen berechnet von Latenzen von Elektromagnetischen Signalen
    - Frequenzen: 
        - L1-Band: 1575,42 MHz (Hauptband, unverschlüsselt, öffentlich)
        - L2-Band: 1227,60 MHz (Korrekturband, verschlüsselt, landvermessung)
        - L5-Band: 1176,45 MHz (Bessere Signalqualität, wiederstandsfähiger gegenüber Störungen, landvermessung, Luft- und Raumfahrt, nicht überall unterstützt)
    - Ablauf:
        1. Sateliten senden Signale mit Zeitstempel und Position aus
        2. Empfänger empfängt Signale und berechnet Latenzen
        3. Empfänger berechnet Distanzen zu Sateliten
        4. Empfänger berechnet eigene Position durch Trilateration

#### 2.1.2 Genauigkeit

    - abhängig von: 
        * Anzahl der Sateliten
        * Signalblockaden
        * Qualität des GPS-Empfängers
    - durchschnittliche genauigkeit: 5-10m

#### 2.1.3 Probleme

    - Da die Distanz Messung über Latenzen funktioniert, ist die Genauigkeit abhängig von der Geschwindigkeit der Signale, da sich Elektromagnetische Wellen mit Lichtgeschwindigkeit ausbreiten, ist die Abweichung pro Sekunde 300.000km -> 0,3m pro Nanosekunde:
        - 1 Nanosekunde: 0,3m
        - 1 Mikrosekunde: 300m
        - 1 Millisekunde: 300.000m
        - 1 Sekunde: 300.000.000m

### 2.2 Schallbasiertes Tracking

#### 2.2.1 Unterschied zum GPS Tracking

    - Anstatt Elektromagnetischen Wellen verwenden wir Schallwellen (Aubreitungsgeschwindigkeit: 343 m/s)

#### 2.2.2 Vorteile

    - Durch die geringere Ausbreitungsgeschwindigkeit der Schallwellen, gelten hier folgende abweichungsregeln:
        - 1 Nanosekunde: 3,43e-7m
        - 1 Mikrosekunde: 0,000343m
        - 1 Millisekunde: 0,343m
        - 1 Sekunde: 343m
    - Hierbei verwenden WIR ein herkömliches Mikrofon zur Aufnahme der Schallwellen, welche eine Abtastrate von 50100 Hz hat -> genauigkeit von 0.00622m welches für unsere Zwecke ausreichen genau ist

#### 2.2.3 Nachteile

    Durch die verwendung von Schallwellen, vorallem im Hochfrequenzbereich, klingen die Schallwellen schneller ab, als elektromagnetische Wellen, woraus folgt, dass wir in einem kleinerem und einem großteils freiem umfeld arbeiten müssen

## 3 Leitfrage (Was ist unsere Leitfrage)

    "Inwiefern wäre ein schallbasiertes Ortungssystem umsetzbar und nützlich?"

## 4 Relevanz (Warum ist unser Thema relevant)

### 4.1 Genauigkeit 

    0.00622m 

### 4.2 Andere Anwendungsbereiche

    Wer braucht diese Genauigkeit? -> 
    - Roboter
    - Drohnen
    - Autonome Fahrzeuge

    KEIN ERSATZ FÜR GPS!!

## 5 Ausgrenzung (Was ist nicht Teil unseres Themas)

    Wir werden uns nicht mit tieferen Informationen und Prinzipen des GPS Systems beschäftigen, sondern dies nur oberflächlich behandeln. Da es für uns eher ein Vergleichsobjekt ist, als ein Teil unseres Projektes.

## 6 Vorgehen (Wie sind wir vorgegangen)

    Aufteilung von uns in Recherche und Experiment

## 7 Allgeimeines Wissen 

## 7.1 Mathematische Grundlage

### 7.1.1 Trilateration

    Wir berechnen die Schnittpunkte von 2 von den 3 Kreisen, welche durch die Distanz und die Position der Sateliten entstehen. Nun haben wir 2 Punkte, welche die mögliche Position des Empfängers darstellen. Um nun den richtigen Punkt zu finden, berechnen wir die Distanz von den 2 Punkten zu dem 3. Sateliten. Der Punkt, welcher die Distanz am besten trifft, ist der richtige Punkt. 

    Formel für Schnittpunkte: 

$$ \frac{2 \frac{y_r \left( \frac{r_2^2 - r_1^2 - y_r^2 - x_r^2}{2x_r} \right)}{x_r^2} \pm \sqrt{4\frac{y_r^2 \left( \frac{r_2^2 - r_1^2 - y_r^2 - x_r^2}{2x_r} \right)^2}{x_r^2} - 4 \cdot (1 + \frac{y_r^2}{x_r^2}) \cdot (\left( \frac{r_2^2 - r_1^2 - y_r^2 - x_r^2}{2x_r} \right)^2 - r_1^2)}}{2 + 2\frac{y_r^2}{x_r^2}} = y_{1,2} \\ \\
$$

$$

\frac{2 \frac{x_r \left( \frac{r_2^2 - r_1^2 - x_r^2 - y_r^2}{2y_r} \right)}{y_r^2} \pm \sqrt{4\frac{x_r^2 \left( \frac{r_2^2 - r_1^2 - x_r^2 - y_r^2}{2y_r} \right)^2}{y_r^2} - 4 \cdot (1 + \frac{x_r^2}{y_r^2}) \cdot (\left( \frac{r_2^2 - r_1^2 - x_r^2 - y_r^2}{2y_r} \right)^2 - r_1^2)}}{2 + 2\frac{x_r^2}{y_r^2}} = x_{1,2}

$$

## 8 Recherche
 
### ... Davids kramm ...

## 9 Experiment

### 9.1 Ansatz

    Berechnung der Distanzen durch Latenz von Schallwellen: 
        1. Aufnahme starten
        2. Schallquelle auslösen
        3. Aufnahme stoppen
        4. Sound Analyse durchführen um zu überprüfen, wann der ton das erste mal gespielt wurde
        5. Aus der Differenz von Start der Schallquelle und der ersten Aufnahme die latenz berechnen
$$ 
    latenz_{sekunden} \cdot 343 \frac{m}{s} = distanz_{meter} 
$$ 

### 9.2 Umsetzung

    Simultanes Abspielen und Aufnehmen -> Threading
    Abspielen von Schallwellen -> PySine
    Aufnehmen von Schallwellen -> PyAudio

    Sound-Analyse: 
        - FFT -> SciPy
        - First Peak -> Numpy

### 9.3 Probleme


    In dieser Fourier Transformation zur Analyse von den gespielten Frequenzen, teilen wir unsere Aufnahme in Chunks ein, welche wir dann einzeln analysieren. Mit einer Samplerate von 44100hz und einer Chunk size 1028 (Werte die wir zusammen untersuchen) hätten wir nur eine Genauigkeit von 0,023s und damit 7,682m was für unsere Zwecke zu ungenau ist.

### 9.4 Lösungen

    Um dieses Problem zu umgehen, überprüfen wir nicht die Chunks: 0 - 1028; 1029 - 2057; 2057 - ...
    Sondern: 0 - 1028; 1 - 1029; 2 - 1030; 3 - 1031; 4 - ...
    Damit haben wir eine Genauigkeit von 0,00002267s oder 0,00757m


## Umsetzung

### 10.1 Experiment

    Wir zeigen Experiement und erklären, dass die Werte nicht akkurat sind. Danach zeigen wir, wie wir es ohne Mikrofon versucht haben um die Latenz zu überprüfen. 

### 10.2 Ergebnisse

    Die werte sind Stark Abhängig von der Latenz der Soundkarte, welche wir nicht beeinflussen können und auch nicht einsehen können. Weswegen es in unserem fall nicht wirklich präzise zu messen ist.

### 10.3 Simulation

    Damit wir unser System testen können, ohne die Latenz der Soundkarte zu berücksichtigen, haben wir eine Simulation geschrieben, welche die Latenz der Soundkarte simuliert.

## 11 Fazit

    Die Grundlagen unseres Experiments funktionieren, durch unsere Limitation an unser Betriebssystem und die dementsprechenden Treiber können wir jedoch keine präzisen Werte liefern.

### 11.1 Beantwortung der Leitfrage

    Ein 

### 11.2 Ausblick

    - Sinvoll und gut umsetzbar lol

## 12 Quellen