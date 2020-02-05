import re as regex  # RegEx für Filter
from time import sleep
from pylatexenc.latex2text import LatexNodes2Text
from selenium import webdriver                          #um den browser zu steuern
from sympy import integrate, Symbol                     #für math. Berechnungen
from mpmath import e

class moodleBotv3():
    url = "https://www.eduvidual.org/mod/quiz/view.php?id=51985"
    creds = ["maximilian.spannring@akadgym.at", "Nope"]
    driver = webdriver.Chrome(r'chromedriver.exe')

    def start(self):            #intro
        print("[i]\Moodle Bot gestartet")

    def login(self):            #logt user ein
        self.driver.get(self.url)
        print("[i]\tMicrosoft-Konto login\n")
        btn = self.driver.find_element_by_id("eduvidual-btn-sso-microsoft")
        btn.click()  # clickt den "Microsoft Button"
        sleep(1)
        emailinput = self.driver.find_element_by_id("i0116")  # findet Feld zum emailadresse eingeben
        emailinput.send_keys(self.creds[0])
        submitbutton = self.driver.find_element_by_id("idSIButton9")
        submitbutton.click()  # clickt "weiter"
        sleep(2)
        pwdinput = self.driver.find_element_by_id("i0118")
        sleep(3)
        pwdinput.send_keys(self.creds[1])  # gibt passwort ein
        submitbutton = self.driver.find_element_by_id("idSIButton9")
        sleep(1)
        submitbutton.click()  # meldet benutzer an
        sleep(2)
        nobtn = self.driver.find_element_by_id("idBtn_Back")  # Benutzernamen nicht merken
        sleep(1)
        nobtn.click()
        print("[i]\tMicrosoft-Konto login abgeschlossen\n")

    def start_course(self):     #startet kurs
        startbtns = self.driver.find_elements_by_class_name("btn-secondary")
        startbtn = startbtns[1]  # wählt aus mehreren btn möglichkeiten den richtigen aus
        if startbtn.text == "Letzten Versuch fortsetzen":
            print("[i]\tLetzter Versuch wird Fortgesetzt...\n")
        else:
            print("[i]\tStarte neuen Kurs...\n")
        startbtn.click()

    def parse_LaTEX(self, t):  # übersetzt f von LaTEX in 'normalen' text
        t = LatexNodes2Text().latex_to_text(t)
        t = t.replace("∫", "")  # ändert noch ein paar Zeichen
        t = t.replace("=", "")
        t = t.replace("ds", "")
        t = t.replace("dx", "")
        t = regex.sub("f\([a-z]\)", "", t)  # RegEx
        t = regex.sub("d[a-z]", "", t)
        print("t:", t)
        return t

    def get_funtion(self, url):  # sucht die zu integrierende Funkton
        self.driver.get(url)
        sleep(1)
        mathjax = self.driver.find_element_by_id("MathJax-Element-1")
        f = (mathjax.get_attribute("innerHTML"))
        print("f", f)
        return f

    def calculate(self, f):
        f = f.replace("√", "sqrt")  # noch mehr formatierungen
        f = f.replace("( ", "(")
        f = f.replace(" )", ")")
        f = f.replace(" ", "*")
        f = f.replace("e", str(e))
        var = regex.search("(?<![a-z])[a-z](?![a-z])", f)  # Variable nach der abgeleitet werden muss
        var = var.group()
        if f[-1] == "*":
            f = f.replace(f[-1], "")
        f = f.replace(u'\xa0', u"")
        print("Var:\t", var)
        print("F:\t", f)
        var = Symbol(str(var))
        i = integrate(f, var)  # eigentliche berechnung des integrals
        i = str(i)
        if str(2.71828182845905) in i:
            i = i.replace("2.71828182845905", "e")
            i = regex.sub("(.00|.0)", "", i)
        print("Integral:\t", i)
        return i

    def enum_q(self):
        q = []
        open_q = []
        urls = []
        sleep(2)
        q.append(self.driver.find_element_by_id("quiznavbutton1"))
        q.append(self.driver.find_element_by_id("quiznavbutton2"))
        q.append(self.driver.find_element_by_id("quiznavbutton3"))
        q.append(self.driver.find_element_by_id("quiznavbutton4"))
        for i in q:
            status = i.get_attribute("title")
            if status == "Antwort gespeichert":
                pass  # wenn die Frage beantwortet wurde passiert nichts
            elif status == "Bisher nicht beantwortet":
                open_q.append(i)  # falls doch, wird sie zu den unbeantworteten Fragen hinzugefügt
        url = self.driver.current_url
        for i in open_q:  # generiert urls zu den offenen Fragen
            c = int(i.text[-1]) - 1 if i.text[-1] != "e" else ""
            if c is not "":
                urls.append(str(url) + "&page=" + str(c))
            else:
                urls.append(url)
        for u in urls:
            print("URl-7", u[-7:])
            if u[-7:] == "&page=0":
                u = u.replace("&page=0", "")
                print("Url wurde ausgebessert")
            print("[i]\t", u)
        return urls

    def fill_in(self, dict):
        print("[i]\tFüllt Lösungen ein")
        for url in dict:
            btn = None
            q = []
            q.append(self.driver.find_element_by_id("quiznavbutton1"))
            q.append(self.driver.find_element_by_id("quiznavbutton2"))
            q.append(self.driver.find_element_by_id("quiznavbutton3"))
            q.append(self.driver.find_element_by_id("quiznavbutton4"))
            for i in q:
                href = i.get_attribute("href")
                href = href.replace("#", "")
                if href[-3:] == url[-3:]:
                    print("[i]\t'Weiter-button gefunden")
                    btn = i
                else:
                    pass
            sleep(2)
            if btn != None:
                btn.click()
            else:
                print("\n[!]\tkein Button wurde gefunden!\n[!]\tTSarte den Versuch neu und setze die pos auf die 1.Frage!\n")
            ids = ["q74555:2_ans1", "q74555:3_ans1", "q74555:4_ans1", "q74555:1_ans1"]
            for i in ids:
                try:
                    inputfield = self.driver.find_element_by_id(i)
                except:
                    pass
            inputs = self.driver.find_elements_by_tag_name("input")
            for i in inputs:
                if i.size == {'height': 28, 'width': 204}:
                    print("[i]\tInputfield gefunden")
                    inputfield = i
            ls = dict[url]
            ls = str(ls[1])
            inputfield.send_keys(ls)
            sleep(0.5)

    def walkthrough(self):
        #self.driver.get(self.url)
        Lösungsbuch = {}
        self.start(self)
        self.login(self)
        print("\n[!]\tAnmelden gescheiter, versuche es nochmal")
        self.start_course(self)
        urls = self.enum_q(self)
        for u in urls:
            f = self.get_funtion(self, u)
            parsedF = self.parse_LaTEX(self, f)
            lösung = self.calculate(self, parsedF)
            Lösungsbuch[u] = [[f, parsedF], lösung]  # füllt LöBuch
        print(Lösungsbuch)
        self.fill_in(self, Lösungsbuch)

moodleBotv3.walkthrough(moodleBotv3)