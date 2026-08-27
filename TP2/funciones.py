class gf:
    def __init__(self, m, poli):
        self.m = m
        self.size = 2**m
        self.policomp = self.size ^ poli
        self.antilog = [0] * self.size
        self.log = [0] * self.size
        valor = 1
        for i in range(self.size-1):
            self.antilog[i] = valor
            self.log[valor] =  i
            valor = valor<<1
            if valor >= self.size:
                valor = valor ^ self.policomp
            

    def suma(self, a, b):
        if a>= self.size or b >= self.size:
            print("Error: Los elementos no pertenecen al campo")
            return -1
        res = a ^ b
        return res

    def producto(self, a, b):
        if a>= self.size or b >= self.size:
            print("Error: Los elementos no pertenecen al campo")
            return -1
        if a==0 or b==0:
            return 0
        mult = self.log[a] + self.log[b]
        if mult >= self.size-1:
            mult = mult % (self.size-1)
        return self.antilog[mult] 

    def division(self, a, b):
        if a>= self.size or b >= self.size:
            print("Error: Los elementos no pertenecen al campo")
            return -1
        if a ==0:
            return 0
        if b ==0:
            print("Error: No se puede dividir por cero")
            return -1
        div = self.log[a] - self.log[b]
        if div < 0:
            div = div + (self.size-1)
        return self.antilog[div]

    def inverso(self, a):
        if a>= self.size:
            print("Error: Los elementos no pertenecen al campo")
            return -1
        if a==0:
            print("Error: No se puede calcular el inverso de cero")
            return -1
        inv = ((self.size-1) - self.log[a]) % (self.size-1)

        return self.antilog[inv]

    def pot(self, a, n):
        if a>= self.size:
            print("Error: Los elementos no pertenecen al campo")
            return -1
        pot = self.log[a] * n
        if pot >= self.size-1:
            pot = pot % (self.size-1)
        if a == 0:
            return 1 if n == 0 else 0
        return self.antilog[pot]

class GFPoly:
    def __init__(self, campo, coeficientes):
        self.campo = campo

        for c in coeficientes:
            if c >= campo.size:
                print("Error: Los elementos no pertenecen al campo")
                return -1

        coeficientesL = list(coeficientes)
        while len(coeficientesL) > 1 and coeficientesL[0] == 0:
            coeficientesL.pop(0)
    
        self.coeficientes = coeficientesL

    def sumaP(self, pol1):
        if self.campo != pol1.campo:
            print("Error: Los polinomios no pertenecen al mismo campo")
            return -1

        coef1 = list(self.coeficientes)
        coef2 = list(pol1.coeficientes)

        if len(coef1) < len(coef2):
            coef1 = [0] * (len(coef2) - len(coef1)) + coef1
        elif len(coef2) < len(coef1):
            coef2 = [0] * (len(coef1) - len(coef2)) + coef2

        coefRes = []
        for c in range(len(coef1)):
            coefRes.append(self.campo.suma(coef1[c], coef2[c]))

        return GFPoly(self.campo, coefRes)

    def multP(self, pol1):
        if self.campo != pol1.campo:
                print("Error: Los polinomios no pertenecen al mismo campo")
                return -1
        coef1 = list(self.coeficientes)
        coef2 = list(pol1.coeficientes)
        res = [0] * (len(coef1)+len(coef2)-1)
        for i in range(len(coef1)):
            for e in range(len(coef2)):
                mult = self.campo.producto(coef1[i], coef2[e])
                pos = i+e
                if res[pos] == 0:
                    res[pos] = mult
                else:
                    res[pos] = self.campo.suma(res[pos], mult)
        return GFPoly(self.campo, res)

    def divE(self, pol1):
        dividendo = list(self.coeficientes)
        divisor = list(pol1.coeficientes)

        if len(dividendo) < len(divisor):
            return GFPoly(self.campo, [0]), GFPoly(self.campo, dividendo)

        cociente = [0] * (len(dividendo) - len(divisor) + 1)

        while len(dividendo) >= len(divisor):
            valorCociente = self.campo.division(dividendo[0], divisor[0])
            gradoTermino = (len(dividendo) - 1) - (len(divisor) - 1)
            cociente[len(cociente) - 1 - gradoTermino] = valorCociente

            monomio = [valorCociente] + [0] * gradoTermino
            resMult = pol1.multP(GFPoly(self.campo, monomio))
            dividendo = GFPoly(self.campo, dividendo).sumaP(resMult).coeficientes

            if len(dividendo) == 1 and dividendo[0] == 0:
                break

        return GFPoly(self.campo, cociente), GFPoly(self.campo, dividendo)

    def escalado(self, a):
        polEscalar = GFPoly(self.campo, [a])
        return self.multP(polEscalar)

    def eval(self, a):
        if a >= self.campo.size:
            print("Error: Los elementos no pertenecen al campo")
            return -1
        lista_aux = [0] * len(self.coeficientes)
        suma = 0
        for i in range(len(self.coeficientes)):
            lista_aux[i] = self.campo.producto(self.coeficientes[i], self.campo.pot(a, (len(self.coeficientes)-1-i)))
        for i in range(len(self.coeficientes)):
            suma = self.campo.suma(suma, lista_aux[i])
        return suma


    def const(self, listaR):
        resultado = GFPoly(self.campo, [1])
        for i in range(len(listaR)):
            pol = GFPoly(self.campo, [1, listaR[i]])
            resultado = resultado.multP(pol)
        return resultado


if __name__ == "__main__":
    c = gf(4, 3)

    def check(nombre, obtenido, esperado):
        ok = "OK  " if obtenido == esperado else "FALLA"
        print(f"[{ok}] {nombre}: obtenido={obtenido}  esperado={esperado}")

    print("========== CAMPO GF(2^4) ==========")
    check("suma(3,5)", c.suma(3, 5), 6)
    check("suma(5,5)", c.suma(5, 5), 0)
    check("producto(3,5)", c.producto(3, 5), 15)
    check("producto(a,0)", c.producto(7, 0), 0)
    check("division(a,a)", c.division(9, 9), 1)
    check("division(a,1)", c.division(9, 1), 9)
    check("inverso(1)", c.inverso(1), 1)
    malos_inv = [a for a in range(1, c.size) if c.producto(a, c.inverso(a)) != 1]
    check("a*inverso(a)==1 para todo a!=0", malos_inv, [])
    check("pot(a,0)", c.pot(5, 0), 1)
    check("pot(0,3)", c.pot(0, 3), 0)
    check("pot(2,4) == 2*2*2*2", c.pot(2, 4), c.producto(c.producto(2, 2), c.producto(2, 2)))

    print("\n========== POLINOMIOS ==========")
    p = GFPoly(c, [13, 12, 5])
    q = GFPoly(c, [7, 2])

    print("sumaP(p,q):", p.sumaP(q).coeficientes)
    print("multP(p,q):", p.multP(q).coeficientes)
    print("escalado(p, 3):", p.escalado(3).coeficientes)

    cociente, resto = p.divE(q)
    reconstruido = q.multP(cociente).sumaP(resto)
    print("cociente:", cociente.coeficientes, " resto:", resto.coeficientes)
    check("d*coc + resto == dividendo", reconstruido.coeficientes, p.coeficientes)

    r = GFPoly(c, [1, 1, 0])
    check("eval(x^2+x, 0)", r.eval(0), 0)
    check("eval(x^2+x, 1)", r.eval(1), 0)

    raices = [2, 4, 8]
    poli = p.const(raices)
    print("const(raices):", poli.coeficientes)
    fallan = [rz for rz in raices if poli.eval(rz) != 0]
    check("todas las raices evaluan a 0", fallan, [])

    print("\nFINALIZO")