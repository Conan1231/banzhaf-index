import itertools

class Fraktion:
    def __init__(self,name,stimmen):
        self.name = name
        self.stimmen = stimmen
        self.banzhaf_macht = 0
        self.banzhaf_index = 0

    def get_name(self):
            return self.name

    def get_stimmen(self):
            return self.stimmen

    def get_banzhaf_macht(self):
            return self.banzhaf_macht

    def get_banzhaf_index(self):
            return self.banzhaf_index

    def ist_kritisch(self):
            self.banzhaf_macht += 1

    def berechne_banzhaf_index(self,n):
            self.banzhaf_index = self.banzhaf_macht/n

class Koalition:
    def __init__(self, fraktionen):
        self.fraktionen = fraktionen
        self.stimmen = 0
        for fraktion in self.fraktionen:
            self.stimmen += fraktion.get_stimmen()

    def get_stimmen(self):
            return self.stimmen

    def get_fraktionen(self):
            return self.fraktionen

    def kritische_fraktionen(self, quorum):
            for fraktion in self.fraktionen:
                if self.get_stimmen() - fraktion.get_stimmen() < quorum:
                    fraktion.ist_kritisch()

    def ist_gewinnend(self, quorum):
            return self.stimmen >= quorum

class Abstimmung:
    def __init__(self, quorum, *fraktionen):
        self.quorum = quorum
        self.fraktionen = fraktionen
        self.koalitionen = []
        self.gewinnend = []
        potenzmenge = [x for length in range(len(self.fraktionen) + 1)
                       for x in itertools.combinations(self.fraktionen, length)]
        for fraktion in potenzmenge:
            self.koalitionen.append(Koalition(list(fraktion)))
        self.gewinnende_koalitionen()

    def gewinnende_koalitionen(self):
            for koalition in self.koalitionen:
                if koalition.ist_gewinnend(self.quorum):
                    self.gewinnend.append(koalition)

    def kritische_fraktionen(self):
            for koalition in self.gewinnend:
                koalition.kritische_fraktionen(self.quorum)

    def berechne_banzhaf_indizes(self):
            n = 0
            for fraktion in self.fraktionen:
                n += fraktion.get_banzhaf_macht()
            for fraktion in self.fraktionen:
                fraktion.berechne_banzhaf_index(n)

    def simulieren(self):
            self.kritische_fraktionen()
            self.berechne_banzhaf_indizes()
            for fraktion in self.fraktionen:
                print(fraktion.get_name() + ' - ' + str(fraktion.get_banzhaf_index()))
            alles = 0
            for fraktion in self.fraktionen:
                alles += fraktion.get_banzhaf_index()
            print("Combined: " + str(alles))

cdu = Fraktion("CDU", 200)
spd = Fraktion("SPD", 153)
afd = Fraktion("AFD", 94)
fdp = Fraktion("FDP", 80)
linke = Fraktion("Die Linke", 69)
gruene = Fraktion("Grüne", 67)
csu = Fraktion("CSU", 46)

abstimmung = Abstimmung(355, cdu, spd, afd, fdp, linke, gruene, csu)
abstimmung.simulieren()
