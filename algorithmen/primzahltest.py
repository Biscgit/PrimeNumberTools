import math
import random
import streamlit as st

st.write(""" Test """)

st.header('Primzahltest')

option = st.selectbox("Welche Primzahltest-Methode soll gemacht werden?", ["Bruteforce-Methode", "Sieb des Eratosthenes", "Sieb von Atkin", "Fermatscher Primzahltest", "Solovay-Strassen-Test", "Miller-Rabin-Test", "Agrawal-Kayal-Saxena-Primzahltest"], index=1)

st.header("Der ausgwewählte Primzahltest lautet: ", option)

def bruteforce(number, verbose):
    for i in range(2, number):
        if number % i == 0:
            if verbose is True:
                st.text(f"{i} ist ein echter Teiler von {number}")
                st.text(f"Die Zahl {number} ist zusammengesetzt")
                st.text(f"{number} = {i} * {number // i}")
            return False
        else:
            if verbose is True:
                st.text(f"{i} ist kein Teiler von {number}")
    return True


def eratosthenes(number, verbose):
    primes = []
    for i in range(2, number):
        if bruteforce(i, 0) == 1:
            primes.append(i)
            if verbose is True:
                print(f"{i} ist die nächte Primzahl")
            if number % i == 0:
                if verbose is True:
                    print(f"Die Primzahl {i} ist ein echter Teiler von {number}")
                    print(f"Die Zahl {number} ist zusammengesetzt")
                    print(f"{number} = {i} * {number // i}")
                return False
                break
            else:
                if verbose is True:
                    print(f"aber {i} ist kein Teiler von {number}")
    if verbose is True:
        print(f"Alle Primzahlen bis {number} lauten: {primes}")
        print(f"Die Zahl {number} ist vermutlich prim")
    return True


def atkin(number, verbose):
    sieve = [False] * (number + 1)
    sqrt_limit = int(math.sqrt(number)) + 1
    # 1. x^2 + y^2 = n    (mod 60) where n % 60 is in {1, 13, 17, 29, 37, 41, 49, 53}
    # 2. x^2 + 3y^2 = n   (mod 60) where n % 60 is in {7, 19, 31, 43}
    # 3. 3x^2 - y^2 = n   (mod 60) where n % 60 is in {11, 23, 47, 59}
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
    # Eliminate composites by sieving
    for n in range(5, sqrt_limit):
        if sieve[n]:
            for k in range(n**2, number + 1, n**2):
                sieve[k] = False
    # Collect primes
    primes = [2, 3] if number > 2 else []
    primes += [n for n in range(5, number + 1) if sieve[n]]
    if verbose is True:
        print(f"Alle Primzahlen bis {number} lauten: {primes}")
    if number in primes:
        if verbose is True:
            print(f"Die Zahl {number} kommt im Array vor und ist eine Primzahl")
        return True
    else:
        if verbose is True:
            print(f"Die Zahl {number} kommt nicht im Array vor und ist keine Primzahl")
        return False


def ggt(a, b):
    if b == 0:
        return a
    return ggt(b, a % b)


def fermat(number, verbose):
    for i in range(2, number):
        if verbose is True:
            print(f"Bestimmung von ggT von {number} und {i} = {ggt(number, i)}")
        if ggt(number, i) == 1:
            if verbose is True:
                print(
                    "Da der größte gemeinsame Teiler  gleich 1 ist, wird {i} hoch {number - 1} berechnet"
                )
            if (i ** (number - 1) % number) != 1:
                if verbose is True:
                    print("Da {i} hoch {number - 1} gleich 1 ist folgt draus:")
                print(f"Die Zahl {number} ist zusammengesetzt")
                return 1
    if verbose is True:
        print(
            f"Es wurden alle Zahlen von 2 bis {number - 1} probiert und kein Zeregung gefunden wurde keine Zerlegung gefunden und daher:"
        )
        print(
            f"Die Zahl {number} scheint eine Primzahl zu sein, aber es könnte sich auch um eine Carmichael-Zahl handeln"
        )
    return 0


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
            print(f"Die Zahl {number} ist kleiner 2")
        return False
    if number != 2 and number % 2 == 0:
        if verbose is True:
            print(f"Die Zahl {number} ist zusammengesetzt")
            print(f"weil die Zahl {number} ist gerade ist")
        return False
    for _ in range(k):
        a = random.randint(2, number - 1)
        if verbose is True:
            print(f"Es wurde eine Zufallszahl ({a}) generiert")
        x = legendre(a, number)
        if verbose is True:
            print(f"Mit dieser Zufallszahl wurde des Legendre-Symbol {x} berechnet")
        if x == 0 or pow(a, (number - 1) // 2, number) != (x % number):
            if verbose is True:
                print(
                    "Da die Zufallszahl^(Nummer - 1)/2 nicht dem Legendre-Symbol modulo der Nummer entspricht, folgt daraus:"
                )
                print(f"Die Zahl {number} ist zusammengesetzt")
            return False
    if verbose is True:
        print(
            f"Die Zahl {number} ist vermutlich prim da für die "
            + k
            + " Durchläufe kein Beweis gefunden wurde"
        )
    return True


def millerrabin(number, runden, verbose):
    if number <= 1:
        if verbose is True:
            print(f"Die Zahl {number} ist kleiner 2")
        return False
    if number <= 3:
        if verbose is True:
            print(f"Die Zahl {number} ist großer oder gleich 3")
        return True
    if number % 2 == 0:
        return False
    r, d = 0, number - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    def millerrabinloop(a, verbose):
        x = pow(a, d, number)
        if x == 1 or x == number - 1:
            return True
        for _ in range(r - 1):
            x = pow(x, 2, number)
            if x == number - 1:
                return True
        return False

    for _ in range(runden):
        a = random.randint(2, number - 2)
        if not millerrabinloop(a, False):
            if verbose is True:
                print(f"Die Zahl {number} ist zusammengesetzt")
            return False
    if verbose is True:
        print(
            f"Die Zahl {number} ist vermutlich prim da kein Beweis für eine Zerlegung gefunden wurde."
        )
    return True


def aks(number, verbose):
    # hier findet AKS stat
    return 0

number = 37
runden = 100
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
