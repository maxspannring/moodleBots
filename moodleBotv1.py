import re as regex  # RegEx für Filter
from time import sleep
from pylatexenc.latex2text import LatexNodes2Text
from selenium import webdriver                          #um den browser zu steuern
from sympy import *                                     #für math. Berechnungen
from mpmath import e                                    #für e- Konstante

def login(creds):                                       #logt user automatisch bei Microsoft ein
    print("[i]\tMicrosoft-Konto login\n")
    btn = driver.find_element_by_id("eduvidual-btn-sso-microsoft")
    btn.click()                                         #clickt den "Microsoft Button"
    sleep(2)
    emailinput = driver.find_element_by_id("i0116")     #findet Feld zum emailadresse eingeben
    emailinput.send_keys(creds[0])
    submitbutton = driver.find_element_by_id("idSIButton9")
    submitbutton.click()                                #clickt "weiter"
    sleep(3)
    pwdinput = driver.find_element_by_id("i0118")
    sleep(5)
    pwdinput.send_keys(creds[1])                        #gibt passwort ein
    submitbutton = driver.find_element_by_id("idSIButton9")
    sleep(1)
    submitbutton.click()                                #meldet benutzer an
    sleep(4)
    nobtn = driver.find_element_by_id("idBtn_Back")     #Benutzernamen nicht merken
    sleep(1)
    nobtn.click()
    print("[i]\tMicrosoft-Konto login abgeschlossen\n")


def start_course():
    sleep(2)
    startbtns = driver.find_elements_by_class_name("btn-secondary")
    startbtn = startbtns[1]                         #wählt aus mehreren btn möglichkeiten den richtigen aus
    if startbtn.text == "Letzten Versuch fortsetzen":
        print("[i]\tLetzter Versuch wird Fortgesetzt...\n")
    else:
        print("[i]\tStarte neuen Kurs...\n")
    startbtn.click()


def enum_open_q():          #findet heraus wie viele Fragen schon beantwortet wurden
    q = []
    open_q = []
    urls = []
    sleep(2)
    q.append(driver.find_element_by_id("quiznavbutton1"))
    q.append(driver.find_element_by_id("quiznavbutton2"))
    q.append(driver.find_element_by_id("quiznavbutton3"))
    q.append(driver.find_element_by_id("quiznavbutton4"))
    #q.append(driver.find_element_by_id("quiznavbutton5"))
    #q.append(driver.find_element_by_id("quiznavbutton6"))
    for i in q:
        status = i.get_attribute("title")
        if status == "Antwort gespeichert":
            pass                                    #wenn die Frage beantwortet wurde passiert nichts
        elif status == "Bisher nicht beantwortet":
            open_q.append(i)                        #falls doch, wird sie zu den unbeantworteten Fragen hinzugefügt
    url = driver.current_url
    for i in open_q:                                #generiert urls zu den offenen Fragen
        c = int(i.text[-1]) -1 if i.text[-1] != "e" else ""
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


def parse_LaTEX(t):                 #übersetzt f von LaTEX in 'normalen' text
    t = LatexNodes2Text().latex_to_text(t)
    t = t.replace("∫", "")      #ändert noch ein paar Zeichen
    t = t.replace("=", "")
    t = t.replace("ds", "")
    t = t.replace("dx", "")
    t = regex.sub("f\([a-z]\)", "", t)     #RegEx
    t = regex.sub("d[a-z]", "", t)
    print("t:", t)
    return t


def get_funtion(url):           #sucht die zu integrierende Funkton
    driver.get(url)
    sleep(1)
    mathjax = driver.find_element_by_id("MathJax-Element-1")
    f = (mathjax.get_attribute("innerHTML"))
    print("f", f)
    return f


def calculate(f):                       #berechnet diue Lösung
    f = f.replace("√", "sqrt")      #noch mehr formatierungen
    f = f.replace("( ", "(")
    f = f.replace(" )", ")")
    f = f.replace(" ", "*")
    f = f.replace("e", str(e))
    var = regex.search("(?<![a-z])[a-z](?![a-z])", f)      #Variable nach der abgeleitet werden muss
    var = var.group()
    print("Var:\t", var)
    print("F:\t", f)
    var = Symbol(str(var))
    i = integrate(f, var)       #eigentliche berechnung des integrals
    i = str(i)
    if str(2.71828182845905) in i:
        i = i.replace("2.71828182845905", "e")
    return i


def fill_in(dict):
    print("[i]\tFüllt Lösungen ein")
    for url in dict:
        btn = None
        q = []
        sleep(0.5)
        q.append(driver.find_element_by_id("quiznavbutton1"))
        q.append(driver.find_element_by_id("quiznavbutton2"))
        q.append(driver.find_element_by_id("quiznavbutton3"))
        q.append(driver.find_element_by_id("quiznavbutton4"))
        q.append(driver.find_element_by_id("quiznavbutton5"))
        q.append(driver.find_element_by_id("quiznavbutton6"))
        sleep(0.5)
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
            print("\n[!]\tkein Button wurde gefunden!\n[!]\tNeuer Versuch...\n")
            sleep(2)
            #nochmal der selbe code wie oben...
            btn = None
            q = []
            sleep(0.5)
            q.append(driver.find_element_by_id("quiznavbutton1"))
            q.append(driver.find_element_by_id("quiznavbutton2"))
            q.append(driver.find_element_by_id("quiznavbutton3"))
            q.append(driver.find_element_by_id("quiznavbutton4"))
            #q.append(driver.find_element_by_id("quiznavbutton5"))
            #q.append(driver.find_element_by_id("quiznavbutton6"))
            sleep(0.5)
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
                print("[!]\tfinden ds Buttons nochmal gescheitert...")

        ids = ["q74555:2_ans1", "q74555:3_ans1", "q74555:4_ans1", "q74555:1_ans1", "q74555:5_ans1", "q74555:6_ans1"]
        for i in ids:
            try:
                inputfield = driver.find_element_by_id(i)
            except:
                pass
        inputs = driver.find_elements_by_tag_name("input")
        for i in inputs:
            if i.size == {'height': 28, 'width': 204}:
                print("[i]\tInputfield gefunden")
                inputfield = i
        ls = dict[url]
        ls = str(ls[1])
        inputfield.send_keys(ls)
        sleep(0.5)


def finish(really):
    print("[i]\tGeht noch einmal alle Fragen durch")
    ids = ["quiznavbutton1", "quiznavbutton2", "quiznavbutton3", "quiznavbutton4"] #, "quiznavbutton5", "quiznavbutton6"]
    for i in ids:
        btn = driver.find_element_by_id(i)
        sleep(0.5)
        btn.click()
        sleep(1.0)
       #ids.remove(i)
    finishbtn = driver.find_element_by_xpath("//*[@id=\"mod_quiz_navblock\"]/div/div/div[2]/a")
    finishbtn.click()
    print("[i]\tVersuch wird beendet")


#----------------------------------
#Beginn des eigentlichen Programmes
#----------------------------------

email = input("gib deine email adresese ein")
pwd = input("gib dein Passwort ein")
creds = [str(email), str(pwd)]
driver = webdriver.Chrome(r'chromedriver.exe')
Lösungsbuch = {}        #alle Lösungen für die unteschiedlicehn aufgaben, noch leer

site = driver.get("https://www.eduvidual.org/mod/quiz/view.php?id=51985")
main_window = driver.current_window_handle

if driver.current_url == "https://www.eduvidual.org/login/index.php":        #wenn der Benutzer nicht angemeldet ist
    try:
        login(creds)                #versucht sich anzumelden
    except Exception:
        print("\n[!]\tAuto-login Fehlgeschlagen. Bitte versuche es nochmal!\tFehler:")
        print(Exception)
else:
    pass
start_course()              #startet Kurs
urls = enum_open_q()        #findet heraus welche Fragen noch beantwortet werden müssen
for u in urls:
    f = get_funtion(u)      #verschafft sich eine Übersicht welche Funktionen gelöst werden müssen
    parsedF = parse_LaTEX(f)
    lösung = calculate(parsedF)
    Lösungsbuch[u] = [[f, parsedF], lösung]  #füllt LöBuch
print(Lösungsbuch)
fill_in(Lösungsbuch)
finish(1)