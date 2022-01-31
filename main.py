import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from quiz_ui import Ui_MainWindow
from questions import lataa_kysymykset_netista


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tiedot = lataa_kysymykset_netista()
        self.vaihda_kysymys_ja_vastaukset(0)
        self.kytke_napit()
        self.pisteet = 0
        self.indeksi = 0

    def vaihda_kysymys_ja_vastaukset(self, indeksi):
        tekstit = self.tiedot[indeksi]
        uudet_tekstit = []
        for (numero, teksti) in enumerate(tekstit):
            if teksti.startswith('*'):
                teksti = teksti[1:]
                self.oikea_vastaus = numero
            uudet_tekstit.append(teksti)
        self.aseta_tekstit(uudet_tekstit)

    def aseta_tekstit(self, tekstit):
        self.aseta_kysymys(tekstit[0])
        self.aseta_nappien_tekstit(tekstit[1:])

    def aseta_nappien_tekstit(self, tekstit):
        (t1, t2, t3, t4) = tekstit
        self.ui.pushButton.setText(t1)
        self.ui.pushButton_2.setText(t2)
        self.ui.pushButton_3.setText(t3)
        self.ui.pushButton_4.setText(t4)

    def aseta_kysymys(self, kysymys):
        self.ui.label.setText(kysymys)

    def kytke_napit(self):
        self.ui.pushButton.clicked.connect(self.nappia_painettu)
        self.ui.pushButton_2.clicked.connect(self.nappia_painettu)
        self.ui.pushButton_3.clicked.connect(self.nappia_painettu)
        self.ui.pushButton_4.clicked.connect(self.nappia_painettu)

    def nappia_painettu(self):
        if self.sender() == self.ui.pushButton:
            nappi = 1
        elif self.sender() == self.ui.pushButton_2:
            nappi = 2
        elif self.sender() == self.ui.pushButton_3:
            nappi = 3
        elif self.sender() == self.ui.pushButton_4:
            nappi = 4
        else:
            return

        if nappi == self.oikea_vastaus:
            print('Oikein!')
            self.pisteet += 1

        self.indeksi += 1
        if self.indeksi >= len(self.tiedot):
            laatikko = QMessageBox(self)
            laatikko.setText(f'Peli päättyi. Pisteesi: {self.pisteet}')
            laatikko.exec()
            self.indeksi = 0
            self.pisteet = 0

        self.vaihda_kysymys_ja_vastaukset(self.indeksi)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
