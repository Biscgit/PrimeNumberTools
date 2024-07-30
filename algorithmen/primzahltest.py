import random


def bruteforce(number, verbose):
    for i in range(2, number):
        if number % i == 0:
            if verbose is True:
                print(f"{i} ist ein echter Teiler von {number}")
                print(f"Die Zahl {number} ist zusammengesetzt")
                print(f"{number} = {i} * {int(number / i)}")
            return False
        else:
            if verbose is True:
                print(f"{i} ist kein Teiler von {number}")
    return True


def eratosthenes(number, verbose):
    for i in range(2, number):
        if bruteforce(i, 0) == 1:
            if verbose is True:
                print(f"{i} ist die nächte Primzahl")
            if number % i == 0:
                if verbose is True:
                    print(f"Die Primzahl {i} ist ein echter Teiler von {number}")
                    print(f"Die Zahl {number} ist zusammengesetzt")
                    print(f"{number} = {i} * {int(number / i)}")
                return False
                break
            else:
                print(f"aber {i} ist kein Teiler von {number}")
    print(f"Die Zahl {number} ist vermutlich prim")
    return True


def atkin(number, verbose):
    # hier findet Atkin stat
    return 0


def ggt(a, b):
    if b == 0:
        return a
    return ggt(b, a % b)


def fermat(number, verbose):
    for i in range(2, number):
        if verbose is True:
            print(f"Estimmung von ggT von {number} und {i} = {ggt(number, i)}")
        if ggt(number, i) == 1:
            if verbose is True:
                print(
                    "Da der größte gemeinsame Teiler  gleich 1 ist, wird {i} hoch "
                    + str(number - 1)
                    + " berechnet"
                )
            if (i ** (number - 1) % number) != 1:
                if verbose is True:
                    print("Da {i} hoch {number - 1}" + " gleich 1 ist folgt draus:")
                print(f"Die Zahl {number} ist zusammengesetzt")
                return 1
    if verbose is True:
        print(
            f"Es wurden alle Zahlen von 2 bis {str(number - 1)} probiert und kein Zeregung gefunden wurde keine Zerlegung gefunden und daher:"
        )
        print(
            f"Starker verdacht auf eine Primzahl, aber die die Zahl {number} könnte eine Carmichael-Zahl sein"
        )
    else:
        print(
            "Die Zahl {number} ist vielleicht prim aber es besteht die Gefahr einer Carmichael-Zahl"
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
        print(f"Die Zahl {number} ist kleiner 2")
        return False
    if number != 2 and number % 2 == 0:
        print(f"Die Zahl {number} ist zusammengesetzt")
        if verbose is True:
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
    print(
        f"Die Zahl {number} ist vermutlich prim da für die {k} Durchläufe kein Beweis gefunden wurde"
    )
    return True


def millerrabin(number, runden, verbose):
    if number <= 1:
        print(f"Die Zahl {number} ist kleiner 2")
        return False
    if number <= 3:
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
            print(f"Die Zahl {number} ist zusammengesetzt")
            return False
    print(
        f"Die Zahl {number} ist vermutlich prim da kein Beweis für eine Zerlegung gefunden wurde."
    )
    return True


def aks(number, verbose):
    # hier findet AKS stat
    return 0


# if __name__ == "__main__":
# number = 561
# runden = 100

# True  --> vermutlich prim
# False --> zusammengesetzt

# Primzahltest
# bruteforce(number, True)
# eratosthenes(number, True)
# atkin(number, True)
# fermat(number, True)
# solovaystrassen(number, runden, True)
# millerrabin(number, runden, True)
# aks(number, True)

# Primzahlzerlegung
# pollard(number, True)
# williams(number, True)williams(number, True)
