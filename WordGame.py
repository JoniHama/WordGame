import math
import random
import os
import xml.etree.ElementTree as ET
from tkinter import *

class Userinterface():
    def __init__(self):
        self.__mainwindow = Tk()
        self.__mainwindow.call("tk", "scaling", 2)
        self.__mainwindow.title("WordGame")
        try:
            self.__mainwindow.iconbitmap(f"{os.getcwd()}/gameicon.ico")
        except Exception:
            print("Error: Peli-ikonin lataus epäonnistui!")

        self.finnish_keyboard_letters = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "Å",
                                    "A", "S", "C", "D", "E", "F", "G", "H", "J", "K", "L", "Ö", "Ä",
                                    "Z", "X", "C", "V", "B", "N", "M"]
        self.list_of_rowbreaks = [1, 6, 11, 16, 21, 26, 31]
        self.letter_buttons = {}
        self.letter_boxes = {}
        self.letter_boxes_thisround = []
        self.gamerow = 1
        self.current_box = 1
        self.this_round_word = ""
        self.finnish_wordlist = []
        self.english_wordlist = []
        self.current_wordlist = []
        self.gamelanguage = "English"
        self.finnish_texts = ["Suomi", "Englanti", "Oikea sana oli", "Jatka painamalla Enter.",
                              "Sanaa ei ole sanalistassa!", "Ei tarpeeksi kirjaimia!", "Voitit pelin!", "Kieli"]
        self.english_texts = ["Finnish", "English", "Word was", "To continue press Enter",
                              "Word not in dictionary!", "Not enough letters!", "You won the game!", "Language"]
        self.current_texts = self.finnish_texts.copy()
        self.__mainwindow.bind('<KeyPress>', self.onPressEvent)
        columncounter = 0
        self.rowfull = False

        # Luodaan silmukassa pelikentän 32 ruutua kuuteen riviin.
        for x in range(1, 31):
            columncounter += 1
            letter_box = Label(self.__mainwindow, text="-")
            # Kenttä alkakoot neljännestä sarakkeesta ja rivi vaihtuu viiden laatikon välein
            letter_box.grid(row=math.ceil(x/5), column=columncounter+3)
            # Säilötään laatikot sanakirjaan sopivilla nimillä myöhempää käyttöä varten
            self.letter_boxes.update({ f"letter_box{x}" : letter_box})

            if columncounter == 5:
                columncounter = 0
        # Luodaan silmukassa kirjainpanikkeet.
        for idx, letter in enumerate(self.finnish_keyboard_letters, 1):
            letter_button = Button(self.__mainwindow, text=letter,
                                   borderwidth=2, command=lambda letter=letter: self.set_letter(letter, self.letter_boxes))
            # Jaetaan napit kolmelle riville. Yksi per sarake indeksin avulla.
            if idx < 12:
                row = 10
                column = idx
            elif 12 <= idx <= 24:
                row = 11
                column = 1+(idx-13)
            elif idx > 24:
                row = 12
                column = 1+(idx-23)
            # Poistetaan tyhjät välit sticky-komennon avulla.
            letter_button.grid(row=row, column=column, sticky="nsew")

            self.letter_buttons.update({ f"self.__{letter}_button" : letter_button})

        self.window_menu = Menu(self.__mainwindow)
        self.__mainwindow.config(menu=self.window_menu)
        self.kielimenu = Menu(self.window_menu, tearoff=0)
        self.window_menu.add_cascade(label=self.current_texts[7], menu=self.kielimenu)

        self.__enter_button = Button(self.__mainwindow, text="ENTER", borderwidth=2, fg="green", command=self.enter_button)
        self.__delete_button = Button(self.__mainwindow, text="DEL", borderwidth=2, fg="red", command=lambda: self.delete_button(self.letter_boxes))

        self.__explanation_text = Label(self.__mainwindow, width=20, text="")
        self.__explanation_text2 = Label(self.__mainwindow, width=20, text="")

        self.__enter_button.grid(row=12, column=10, sticky="nsew")
        self.__delete_button.grid(row=12, column=2, rowspan=4)
        self.__explanation_text.grid(row=2, column=10, columnspan=4)
        self.__explanation_text2.grid(row=3, column=10, columnspan=4)

        self.kielimenu.add_command(label=self.current_texts[0], command=lambda: self.language_change("Finnish"))
        self.kielimenu.add_command(label=self.current_texts[1], command=lambda: self.language_change("English"))

    def start(self):
        """
        Ohjataan ohjelman aloitus kahden metodin kautta. Setup määrittää
        tiedostojen latauksen sekä sen sisällä pelisanan muodostamisen
        ja mainloop() aloittaa käyttöliittymän toiminnan.
        """
        self.setup_round()
        self.__mainwindow.mainloop()

    def language_change(self, language):
        """
        Käsittelee kielenvaihtamisen. Kielivalikon napit ohjaavat tänne. Täällä asetetaan
        self.current_texts ja self.current_wordlist arvot, jotka määräävät käyttöliittymän
        sekä pelin kielen. Samalla peli aloitetaaan myös alusta self.new_game() metodilla.
        :param language: annettu pelikieli kielivalikosta
        """

        self.gamelanguage = language
        if self.gamelanguage == "Finnish":
            self.current_texts = self.finnish_texts
            self.current_wordlist = self.finnish_wordlist
            self.gamelanguage = "Finnish"
        else:
            self.current_texts = self.english_texts
            self.current_wordlist = self.english_wordlist
            self.gamelanguage = "English"
        self.kielimenu.entryconfig(1, label=self.current_texts[0])
        self.kielimenu.entryconfig(2, label=self.current_texts[1])
        self.window_menu.entryconfig(1, label=self.current_texts[7])

        self.new_game()

    def set_letter(self, letter, letter_boxes):
        """
        Käyttöliittymän kirjainnapit ohjaavat tähän metodiin. Käsittelee pelikentän
        muokkaamisen pelaajan syötteen mukaisesti.
        :param letter: pelaajan valitsema kirjain käyttöliittymästä
        :param letter_boxes: sanakirja, jossa pelikenttä.
        """
        self.__explanation_text.configure(text="")
        if self.rowfull == False:
            letter_boxes[f"letter_box{self.current_box}"].configure(text=letter, bg="white", fg="black")
            self.current_box += 1
            if self.current_box in self.list_of_rowbreaks:
                self.rowfull = True
        else:
            pass

    def onPressEvent(self, event):
        letter = event.char.upper()
        if letter in self.finnish_keyboard_letters:
            self.set_letter(letter, self.letter_boxes)
        elif event.char == "\r":
            self.enter_button()
        elif event.char == "\x08":
            self.delete_button(self.letter_boxes)

    def enter_button(self):
        """
        Käsittelee Enter-napin painamisen logiikan. Muokkaa käyttöliittymän
        tekstejä erikoistapauksissa, kuten pelin päättyminen, kirjaimia
        ei ole syötetty oikeaa määrää tai sanaa ei ole sanakirjassa.
        Onko sana sanakirjassa tarkastelu tapahtuu metodissa get_guessed_word().
        """
        if self.rowfull == True:
            guessed_word = self.get_guessed_word()
            # Tarkastellaan toisessa metodissa, onko sana validi.
            if self.check_word(guessed_word):
                # Onko pelaaja viimeisellä rivillä, eli peli päättyy enterin jälkeen?
                if self.current_box >= 31:
                    self.__explanation_text.configure(text=f"{self.current_texts[2]} {self.this_round_word}!")
                    self.__explanation_text2.configure(text=self.current_texts[3])
                    self.rowfull = False
                else:
                    self.rowfull = False
                    self.gamerow += 1
                    self.letter_boxes_thisround = []
            else:
                self.__explanation_text.configure(text=self.current_texts[4])
        else:
            if self.game_over():
                self.new_game()
            else:
                self.__explanation_text.configure(text=self.current_texts[5])
    def delete_button(self, letter_boxes):
        """
        Käsittelee Delete-napin painamisen logiikan.
        Tarkastelee useita pelitilanteita, kuten onko sana mennyt oikein
        vai väärin rowfull-muuttujan avulla ja sen perusteella tarkastelee,
        antaako poistaa edellisiä kirjaimia yhdessä list_of_rowbreaks tiedon
        kanssa, josta saadaan kohdat, joissa pelirivi muuttuu.
        :param letter_boxes: sanakirja, jossa pelikenttä.
        """
        if self.game_over():
            self.new_game()
        else:
            self.__explanation_text.configure(text="")
            if self.current_box not in self.list_of_rowbreaks:
                self.current_box -= 1
            elif self.rowfull == True:
                self.current_box -= 1
            self.rowfull = False
            letter_boxes[f"letter_box{self.current_box}"].configure(text="-", bg="SystemButtonFace")
    def setup_round(self):
        """
        Setup_round käydään läpi heti alussa. Siitä saadaan sekä suomen- että
        englanninkieliset sanalistat, joita hyödynnetään pelissä.
        """
        try:
            tree = ET.parse(f"{os.getcwd()}\data\kotus-sanalista_v1.xml")
        except Exception:
            print("Error: Sanalistaa ei löydy!")
        allwords = tree.getroot()
        self.finnish_wordlist = []
        # Tämän XML-tiedoston formaatissa sanat löytyvät "s"-osiosta.
        for word in allwords.iter("s"):
            word = word.text
            # Pelaajan ei ole mahdollista syöttää merkkiä "-", joten sivuutetaan ne.
            if len(word) == 5 and "-" not in word:
                self.finnish_wordlist.append(word)
            else:
                continue

        with open(f"{os.getcwd()}\data\sgb-words.txt") as english_words:
            for word in english_words:
                self.english_wordlist.append(word.rstrip())
        self.language_change(self.gamelanguage)
        self.determine_roundword()

    def get_guessed_word(self):
        """
        Muodostaa pelaajan syöttämän sanan riviltä. Hyödyntää self.gamerow tietoa
        halutun rivin saamiseen.
        :return: guessed_word: pelaajan käyttöliittymällä syöttämä sana
        """
        # lista [1, 2, 3, 4, 5], joista jokainen arvo kerrotaan self.gamerow
        letter_box_indexes = [x+(5*(self.gamerow-1)) for x in range(1, 6)]
        guessed_word = []

        for letter_box_index in letter_box_indexes:
            self.letter_boxes_thisround.append(self.letter_boxes[f"letter_box{letter_box_index}"])
            guessed_word.append(self.letter_boxes[f"letter_box{letter_box_index}"].cget("text"))
        guessed_word = "".join(guessed_word).lower()
        return guessed_word
    def check_word(self, guessed_word):
        """
        Funktio tarkastaa pelaaman syöttämän sanan ja tarkastelee, miten
        se liittyy etsittyyn sanaan. Jos sanoissa on sama kirjain, se
        väritetään sekä pelikentällä, että näppäimistöllä keltaiseksi.
        Jos se on vielä samalla paikalla, väri on vihreä.
        Erikoistapaus on, että jos sana oikea. Tällöin ilmoitetaan se pelaajalle.

        :param guessed_word: pelaajan käyttöliittymällä syöttämä sana
        :return: False, jos pelaajan syöttämä sana ei ole sopiva
        True, jos sana on sopiva.
        """

        if guessed_word not in self.current_wordlist:
            return False
        # Käydään pelaajan sana kirjain kirjaimelta läpi ja verrataan
        # jokaista kirjainta pelisanaan.
        for idx, letter in enumerate(guessed_word):
            if letter in self.this_round_word:
                if guessed_word[idx] == self.this_round_word[idx]:
                    self.letter_boxes_thisround[idx].configure(bg="green")
                    self.letter_buttons[f"self.__{letter.upper()}_button"].configure(bg="green")
                else:
                    self.letter_boxes_thisround[idx].configure(bg="yellow")
                    if self.letter_buttons[f"self.__{letter.upper()}_button"].cget("bg") != "green":
                        self.letter_buttons[f"self.__{letter.upper()}_button"].configure(bg="yellow")
            else:
                self.letter_buttons[f"self.__{letter.upper()}_button"].configure(bg="grey")
        if guessed_word == self.this_round_word:
            self.__explanation_text.configure(text=self.current_texts[6])
            self.__explanation_text2.configure(text=self.current_texts[3])
        return True

    def determine_roundword(self):
        """
        Arpoo tämän kierroksen pelisanan.
        """
        random_word_index = random.randint(0, len(self.current_wordlist))
        self.this_round_word = self.current_wordlist[random_word_index]

    def reset_GUI(self):
        """
        Palauttaa käyttöliittymän ennen pelin alkua olevaan tilanteeseen.
        Eli voittotekstit lähtevät ja pelikenttä palautuu koskemattomaksi.
        """
        # letter_buttonsien avain on muotoa self.__kirjain_button, joten
        # niiden saamiseen käytetään for looppia, joka käy läpi aakkosia a:sta eteenpäin.
        # ä on ASCII-koodiltaan 196. Joten pidennetään looppi 197 asti.
        for index in list(map(chr, range(97, 197))):
            try:
                self.letter_buttons[f"self.__{index.upper()}_button"].configure(bg="SystemButtonFace")
            except Exception:
                continue
        for index in range(1, 31):
            self.letter_boxes[f"letter_box{index}"].configure(text="-", bg="SystemButtonFace")
        self.__explanation_text.configure(text="")
        self.__explanation_text2.configure(text="")

    def new_game(self):
        """
        Uuden pelin alkaessa palautetaan reset_GUI metodin avulla käyttöliittymä
        normaaliksi, arvotaan uusi pelisana determine_roundwordilla sekä
        muutetaan muutamat kierrosriippuvaiset muuttujat takaisin alkutilanteeseen.
        """
        self.reset_GUI()
        self.determine_roundword()
        self.gamerow = 1
        self.current_box = 1
        self.letter_boxes_thisround = []

    def game_over(self):
        """
        Pelin loppuminen tarkastetaan yksinkertaisesti sillä, että onko lopputekstit
        sillä hetkellä ruudussa. Tämä voi olla häviö- tai voittotila.
        :return: True jos peli on päättynyt.
        False jos peli ei ole päättynyt.
        """
        # self.current.texts[3] on "jatka" teksti, joka on sekä
        # häviössä että voitossa. Siksi se toimii kumpaankin.
        if self.__explanation_text2.cget("text") == self.current_texts[3]:
            return True
        else:
            return False

def main():
    ui = Userinterface()
    ui.start()

if __name__ == "__main__":
    main()