import math
import random
import streamlit as st

#----------------------------------------PRIMZAHLTEST----------------------------------------

def bruteforce(number, verbose):
    if number == 1:
        return False
    for i in range(2, int((number**(1/2))+1)):
        if number % i == 0:
            if verbose is True:
                st.text(f"{i} ist ein echter Teiler von {number}.")
                st.text(f"Die Zahl {number} ist zusammengesetzt.")
                st.text(f"{number} = {i} * {number // i}")
            return False
        else:
            if verbose is True:
                st.text(f"{i} ist kein Teiler von {number}")
    return True


def eratosthenes(number, verbose):
    primes = []
    if number == 1:
        return False
    for i in range(2, number):
        if bruteforce(i, 0) == 1:
            primes.append(i)
            if verbose is True:
                st.write(f"{i} ist die nächte Primzahl.")
            if number % i == 0:
                if verbose is True:
                    st.write(f"Die Primzahl {i} ist ein echter Teiler von {number}.")
                    st.write(f"Die Zahl {number} ist zusammengesetzt.")
                    st.write(f"{number} = {i} * {number // i}")
                return False
            else:
                if verbose is True:
                    st.write(f"Aber {i} ist kein Teiler von {number}.")
    if verbose is True:
        st.write(f"Alle Primzahlen bis {number} lauten: {primes}")
    return True


def atkin(number, verbose):
    if verbose is True:
        st.write(f"Die Modulo-Bedingungen sehen wie folgt aus: \n"
                 f"1. x^2 + y^2 = n    (mod 60) wobei n % 60 in (1, 13, 17, 29, 37, 41, 49, 53) enthalten sein muss. \n"
                 f"2. x^2 + 3y^2 = n   (mod 60) wobei n % 60 is in (7, 19, 31, 43) enthalten sein muss. \n"
                 f"3. 3x^2 - y^2 = n   (mod 60) wobei n % 60 is in (11, 23, 47, 59) enthalten sein muss. \n")
    sieve = [False] * (number + 1)
    sqrt_limit = int(math.sqrt(number)) + 1

    for x in range(1, sqrt_limit):
        for y in range(1, sqrt_limit):
            n = 4 * x**2 + y**2
            if n <= number and n % 60 in {1, 13, 17, 29, 37, 41, 49, 53}:
                sieve[n] = not sieve[n]
            n = 3 * x**2 + y**2
            if n <= number and n % 60 in {7, 19, 31, 43}:
                sieve[n] = not sieve[n]
            n = 3 * x**2 - y**2
            if x > y and n <= number and n % 60 in {11, 23, 47, 59}:
                sieve[n] = not sieve[n]

    for n in range(5, sqrt_limit):
        if sieve[n]:
            for k in range(n**2, number + 1, n**2):
                sieve[k] = False

    primes = [2, 3] if number > 2 else []
    primes += [n for n in range(5, number + 1) if sieve[n]]
    if verbose is True:
        st.write(f"Alle Primzahlen bis {number} lauten: {primes}")
    if number in primes:
        if verbose is True:
            st.write(f"Die Zahl {number} kommt im Array vor.")
        return True
    else:
        if verbose is True:
            st.write(f"Die Zahl {number} kommt nicht im Array vor.")
        return False


def ggt(a, b):
    if b == 0:
        return a
    return ggt(b, a % b)


def fermat(number, verbose):
    if number == 1:
        return False
    for i in range(2, number):
        nggt = ggt(number, i)
        if verbose is True:
            st.write(f"Bestimmung von ggT von {number} und {i} = {nggt}")
        if nggt == 1:
            if verbose is True:
                latex = fr"{i}^{{{number - 1}}} mod {number}"
                st.write(f"Da der größte gemeinsame Teiler gleich 1 ist, wird ${latex}$ berechnet.")
            if (((i ** (number - 1)) % number) != 1):
                if verbose is True:
                    latex = fr"{i}^{{{number - 1}}} mod {number}"
                    st.write(f"Da ${latex}$ gleich 1 ist folgt draus:")
                    st.write(f"Die Zahl {number} ist zusammengesetzt.")
                return False
    if verbose is True:
        st.write(f"Es wurden alle Zahlen von 2 bis {number - 1} probiert und da kein Zerlegung gefunden wurde folgt:")
        st.write(f"Die Zahl {number} scheint eine Primzahl zu sein, aber es könnte sich auch um eine Carmichael-Zahl handeln.")
    return True


def legendre(a, n):
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a % 2 == 0:
        if n % 8 == 1 or n % 8 == 7:
            return legendre(a // 2, n)
        else:
            return -legendre(a // 2, n)
    if a % 4 == 3 and n % 4 == 3:
        return -legendre(n % a, a)
    else:
        return legendre(n % a, a)


def solovaystrassen(number, k, verbose):
    if number < 2:
        if verbose is True:
            st.write(f"Die Zahl {number} ist kleiner 2.")
        return False
    if number != 2 and number % 2 == 0:
        if verbose is True:
            st.write(f"Die Zahl {number} ist zusammengesetzt.")
            st.write(f"weil die Zahl {number} ist gerade ist.")
        return False
    for _ in range(k):
        a = random.randint(2, number - 1)
        if verbose is True:
            st.write(f"Es wurde eine Zufallszahl {a} zwischen 2 und {number - 1} generiert.")
        x = legendre(a, number)
        if verbose is True:
            st.write(f"Mit dieser Zufallszahl {a} wurde des Legendre-Symbol {x} berechnet.")
        if x == 0 or pow(a, (number - 1) // 2, number) != (x % number):
            if verbose is True:
                latex = fr"{a}^{{{((number - 1) / 2)}}} \equiv {x} mod {number}"
                st.write(f"Da ${latex}$, folgt daraus:")
                st.write(f"Die Zahl {number} ist zusammengesetzt.")
            return False
        else:
            if verbose is True:
                st.write(f"Keine Aussage ist möglich und daher wählen einer neuen Zufallszahl a.")
    if verbose is True:
        st.write(f"Es wurden alle {k} Runden probiert und da kein Zerlegung gefunden wurde folgt:")
        st.write(f"Die Zahl {number} ist vermutlich prim da für die {k} Durchläufe kein Beweis gefunden wurde.")
    return True


def millerrabin(number, runden, verbose):
    if number <= 1:
        if verbose is True:
            st.write(f"Die Zahl {number} ist kleiner oder gleich 1.")
        return False
    if number <= 3:
        if verbose is True:
            st.write(f"Die Zahl {number} ist kleiner oder gleich 3.")
        return True
    if number % 2 == 0:
        if verbose is True:
            st.write(f"Die Zahl {number} ist durch 2 teilbar also kein Primzahl.")
        return False
    r, d = 0, number - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    def millerrabinloop(a, verbose):
        x = pow(a, d, number)
        if verbose is True:
            latex = r"{a}^{d} mod {number}"
            st.write(f"Die Zahl {x} wird durch ${latex}$ berechnet.")
        if x == 1 or x == number - 1:
            if verbose is True:
                st.write(f"Da die Zahl {x} entweder 1 oder -1 entspricht, kann keine Aussage mit {a} getroffen werden.")
            return True
        for _ in range(r - 1):
            x = pow(x, 2, number)
            if x == number - 1:
                if verbose is True:
                    st.write(f"Da die Zahl {x} = {number - 1} folgt, dass keine Aussage mit {a} getroffen werden kann.")
                return True
        if verbose is True:
            st.write(f"Mit der Zahl {a} lässt sich beweisen, dass {number} keine Primzahl ist.")
        return False

    for _ in range(runden):
        a = random.randint(2, number - 2)
        if verbose is True:
            st.write(f"Es wird ein Zufallszahl {a} generiert zwischen 2 und {number -2}.")
            st.write(f"Es wird ein Schreife zum Testen mit der Zufallszahl {a} begonnen.")
        if not millerrabinloop(a, verbose):
            if verbose is True:
                st.write(f"Die Zahl {number} ist zusammengesetzt.")
            return False
    if verbose is True:
        st.write(f"Die Zahl {number} ist vermutlich prim, da in den {runden} Runden kein Beweis für eine Zerlegung gefunden wurde.")
    return True


def expand_x_1(number):
    c = 1
    for i in range(number // 2 + 1):
        c = c * (number - i) // (i + 1)
        yield c

def aks(number):
    if number == 1:
        return False
    if number == 2:
        return True
    for i in expand_x_1(number):
        if i % number:
            return False
    return True

#----------------------------------------PRIMZAHLZERLEGUNG----------------------------------------

#----------------------------------------STREAMLIT----------------------------------------

st.header('Primzahltests')

option = st.selectbox("Welche Primzahltest-Methode soll gemacht werden?", ["Bruteforce-Methode", "Sieb des Eratosthenes", "Sieb von Atkin", "Fermatscher Primzahltest", "Solovay-Strassen-Test", "Miller-Rabin-Test", "Agrawal-Kayal-Saxena-Primzahltest"], index=0)

verbose = st.checkbox("Ist eine detailierte Beschreibung gewünscht?")

number = st.number_input("Welche Zahl soll geprüft werden?", value=1, min_value=1)

#st.write(f"Die ausgewählte zu testende Zahl lautet: " + str(number))
#st.write(f"Der ausgewählte Primzahltest lautet: " + str(option))

if option == "Bruteforce-Methode":
    st.write("Die Bruteforce-Methode probiert alle Zahlen von 2 bis zur Wurfel aus " + str(number)+ " durch.")
    if bruteforce(number, verbose):
        st.write("Die Zahl " + str(number) + " ist eine Primzahl.")
    else:
        st.write("Die Zahl " + str(number) + " ist keine Primzahl.")

if option == "Sieb des Eratosthenes":
    st.write("Bei dem Sieb des Eratosthenes werden alle Primzahlen die kleiner als " + str(number) + " sind als Teiler durchprobiert.")
    if eratosthenes(number, verbose):
        st.write("Die Zahl " + str(number) + " ist eine Primzahl.")
    else:
        st.write("Die Zahl " + str(number) + " ist keine Primzahl.")

if option == "Sieb von Atkin":
    st.write(f"Der Sieb von Atkin ist ein Algorithmus zur Bestimmung von Primzahlen, der eine mathematische Transformation der Quadrate und Reste verwendet, um Kandidaten für Primzahlen zu identifizieren. "
             f"Er durchläuft ein Gitter von Zahlen und wendet bestimmte Modulo-Bedingungen an, um Zahlen zu markieren, die Primzahlen sein könnten. "
             f"Schließlich entfernt er Vielfache von gefundenen Primzahlen, um die endgültige Liste der Primzahlen zu erstellen.")
    if atkin(number, verbose):
        st.write("Die Zahl " + str(number) + " ist eine Primzahl.")
    else:
        st.write("Die Zahl " + str(number) + " ist keine Primzahl.")

if option == "Fermatscher Primzahltest":

    latex1 = r"a^{p-1} \equiv 1 (mod p)"
    latex2 = r"a^{n-1} \equiv 1 (mod n)"
    st.write(fr'''Der Fermat-Primzahltest basiert auf dem kleinen Fermatschen Satz, der besagt, dass für eine Primzahl p und eine Basis a gilt: ${latex1}$. Um zu prüfen, ob eine Zahl n prim ist, wählt man eine Basis a  und überprüft, ob ${latex2}$. Wenn diese Bedingung nicht erfüllt ist, ist n definitiv keine Primzahl, aber wenn sie erfüllt ist, ist n wahrscheinlich prim, aber nicht garantiert.''')
    if fermat(number, verbose):
        st.write("Die Zahl " + str(number) + " ist vermeintlich eine Primzahl, aber es könnte auch eine Carmichael-Zahl sein.")
    else:
        st.write("Die Zahl " + str(number) + " ist keine Primzahl.")

if option == "Solovay-Strassen-Test":

    latex1 = r"\left(\frac{a}{n} \right)"
    latex2 = r"a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \ (\text{mod} \ n)"
    st.write(fr'''Der Solovay-Strassen-Primzahltest basiert auf dem Euler-Kriterium und verwendet die Jacobi-Symbole zur Bestimmung der Primalität. Für eine gegebene Zahl n und eine zufällige Basis a, berechnet der Test das Jacobi-Symbol ${latex1}$ und überprüft, ob ${latex2}$. Wenn diese Bedingung nicht erfüllt ist, ist n keine Primzahl; wenn sie erfüllt ist, ist n wahrscheinlich prim, jedoch besteht immer ein kleines Risiko, dass n eine Pseudoprimzahl ist.''')
    runden = st.number_input("Wieviele Runden sollen durchlaufen bzw. getestet werden?", value=5, min_value=5, max_value=100)
    if solovaystrassen(number, runden, verbose):
        st.write("Die Zahl " + str(number) + " ist vermeintlich eine Primzahl, aber es könnte auch eine Pseudo-Primzahl sein.")
    else:
        st.write("Die Zahl " + str(number) + " ist keine Primzahl.")

if option == "Miller-Rabin-Test":

    latex1 = r"2^s \cdot d"
    latex2 = r"a^d mod n = 1"
    latex3 = r"a^{2^r \cdot d} \equiv -1"
    latex4 = r"0 \leq r < s"
    st.write(fr"Der Miller-Rabin-Primzahltest ist ein probabilistischer Algorithmus, der auf der Faktorisierung n-1 in die Form ${latex1}$ basiert, wobei n die zu testende Zahl ist. Eine zufällig gewählte Basis a wird verwendet, um zu prüfen, ob  ${latex2}$  oder ob eine der Bedingungen ${latex3}$ für ${latex4}$ erfüllt ist. Wenn keine dieser Bedingungen erfüllt ist, ist n zusammengesetzt; andernfalls ist n wahrscheinlich prim.")
    runden = st.number_input("Wieviele Runden sollen durchlaufen bzw. getestet werden?", value=5, min_value=5, max_value=100)
    if millerrabin(number, runden, verbose):
        st.write("Die Zahl " + str(number) + " ist vermeintlich eine Primzahl.")
    else:
        st.write("Die Zahl " + str(number) + " ist keine Primzahl.")

if option == "Agrawal-Kayal-Saxena-Primzahltest":
    latex1 = r"(x - a)^n \equiv (x^n - a)"
    latex2 = r"a \in \Z"
    latex3 = r"\left\lfloor \sqrt{\phi(r)} \log(n) \right\rfloor  "
    latex4 = r"ggt(a, n) \neq 1"
    latex5 = r"(x + a)^n \equiv x^n + a \ (\text{mod} \ n, x^r - 1)"
    st.write(f"Der AKS-Primzahltest (benannt nach seinen Erfindern Agrawal, Kayal und Saxena) ist ein deterministischer Algorithmus zur Bestimmung der Primalität einer Zahl. "
             f"Der Test basiert auf der Eigenschaft, dass eine Zahl n genau dann prim ist, wenn ${latex1}$ für alle ${latex2}$ gilt. "
             f"Der AKS-Test überprüft diese Eigenschaft unter eingeschränkten Bedingungen, um die Komplexität zu reduzieren. Zuerst wird festgestellt, ob n eine perfekte Potenz ist. "
             f"Wenn ja, ist n keine Primzahl. Andernfalls wird eine geeignete Grenze r bestimmt, sodass n für die Mehrheit der Basen a keine nichttrivialen r-Wurzeln besitzt. "
             f"Dies wird durch iteratives Finden des kleinsten r erreicht, für das die Ordnung von n modulo r groß genug ist. "
             f"Der Algorithmus überprüft dann für jedes a von 1 bis ${latex3}$, ob ${latex4}$. Falls ein solches 𝑎 a gefunden wird, ist n keine Primzahl. "
             f"Schließlich wird getestet, ob ${latex5}$ für jedes a in diesem Bereich gilt. Wenn alle diese Tests bestanden werden, ist n prim, andernfalls nicht. "
             f"Der AKS-Primzahltest ist der erste bekannte deterministische Algorithmus mit polynomieller Laufzeit, der die Primalität jeder beliebigen Zahl ohne Annahmen über unbewiesene Hypothesen überprüft.")
    if aks(number):
        st.write(f"{number} ist eine Primzahl.")
    else:
        st.write(f"{number} ist keine Primzahl.")





    # True  --> vermutlich prim
    # False --> zusammengesetzt
    # Primzahltest
#bruteforce(number, True)
    # eratosthenes(number, True)
    # atkin(number, True)
    # fermat(number, True)
    # solovaystrassen(number, runden, True)
    # millerrabin(number, runden, True)
    # aks(number, True)
    # Primzahlzerlegung
    # pollard(number, True)
    # williams(number, True)
