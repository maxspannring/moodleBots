#-------AUFGEGEBEN, WEIL ZU UNNÖTIG UND SCHWIERIG----------------------------
#-------MAN MÜSSTE BEI JEDER DER 4 FRAGEN EINE EIGENE FUNKTION ANWENDEN------
#-------+ HERAUSFINDEN WELCHE FRAGE WELCHER TYP IST--------------------------
#-------MIT HAND AUSRECHNEN IST VIEL SCHNELLER UND EFFEKTIVER----------------

from selenium import webdriver
import re as regex
from time import sleep


class moodleBot2():
    url = "https://www.eduvidual.org/mod/quiz/view.php?id=47463"
    creds = ["maximilian.spannring@akadgym.at", "Nope"]
    driver = webdriver.Chrome(r'chromedriver.exe')
    q_list = {}

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

    def enum_q(self):           #findet status/Typ der Fragen heraus
        q = []
        open_q = []
        sleep(2)
        q.append(self.driver.find_element_by_id("quiznavbutton1"))
        q.append(self.driver.find_element_by_id("quiznavbutton2"))
        q.append(self.driver.find_element_by_id("quiznavbutton3"))
        q.append(self.driver.find_element_by_id("quiznavbutton4"))
        for i in q:                                                     #findet heraus welche Fragen schon beamtwortet wurden
            status = i.get_attribute("title")
            if status == "Antwort gespeichert":
                pass  # wenn die Frage beantwortet wurde passiert nichts
            elif status == "Bisher nicht beantwortet":
                open_q.append(i)  # falls doch, wird sie zu den unbeantworteten Fragen hinzugefügt
        for o in open_q:                                                #bestimmt typen der Fragen
            u = o.get_attribute("href")
            for n in self.q_list:                               #schon ein eintrag?
                if o.get_attribute("id") == n:
                    entry = True
                    print("Eintrag")
                else:
                    entry = False
                    print("kein Eintrag")
            if u == '#' and not entry:
                type = self.define_type(self)
                self.q_list[o.get_attribute("id")] = type
            else:
                for w in open_q:
                    print(w)
                    sleep(2)
                    print(w.get_attribute("id"))
                    btn = self.driver.find_element_by_id(w.get_attribute("id"))
                    btn.click()
                    for n in self.q_list:
                        if o.get_attribute("id") == n:
                            entry = True
                            print("Eintrag")
                        else:
                            entry = False
                            print("kein Eintrag")
                            type = self.define_type(self)
                            self.q_list[w.get_attribute("id")] = type
                    q = []
                    open_q = []
                    q.append(self.driver.find_element_by_id("quiznavbutton1"))
                    q.append(self.driver.find_element_by_id("quiznavbutton2"))
                    q.append(self.driver.find_element_by_id("quiznavbutton3"))
                    q.append(self.driver.find_element_by_id("quiznavbutton4"))
                    for i in q:  # findet heraus welche Fragen schon beamtwortet wurden
                        status = i.get_attribute("title")
                        if status == "Antwort gespeichert":
                            pass  # wenn die Frage beantwortet wurde passiert nichts
                        elif status == "Bisher nicht beantwortet":
                            open_q.append(i)  # falls doch, wird sie zu den unbeantworteten Fragen hinzugefügt

    def define_type(self):
        print("der typ ist vlaah ballah")
        return "protoTYPE"

    def parse_LaTex(self):
        pass

    def integrate(self):        #bildet Satmmfunktion
        pass

    def integrate_plus_C(self): #integriert und findet C heraus
        pass

    def answer_checkboxes(self):#beantwortet ankreuzaufgaben
        pass

    def wahrfalsch(self):       #beantrwortet Wahr oder Falsch fragen
        pass

    def fill_in(self):          #füllt richtige Fragen ein
        pass

    def finish(self):       #geht noch einmal alle fragen durch
        pass

    def walkthrough(self):
        try:
            self.login(self)
        except:
            print("\n[!]\tFehler beim Login, neuer Versuch...")
            self.login(self)
        self.start_course(self)
        self.enum_q(self)
        print(self.q_list)


moodleBot2.walkthrough(moodleBot2)
