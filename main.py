import sys
import time

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox

from quiz_ui import Ui_MainWindow
from questions import lataa_kysymykset_netista


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.luo_status_widget()
        self.tiedot = lataa_kysymykset_netista()
        self.vaihda_kysymys_ja_vastaukset(0)
        self.kytke_napit()
        self.kierros = 1
        self.pisteet = 0
        self.indeksi = 0

    def luo_status_widget(self):
        self.kierros_label = QLabel()
        self.ui.statusbar.addPermanentWidget(self.kierros_label)

    def vaihda_kysymys_ja_vastaukset(self, indeksi):
        tekstit = self.tiedot[indeksi]
        uudet_tekstit = []
        for (numero, teksti) in enumerate(tekstit):
            if teksti.startswith('*'):
                teksti = teksti[1:]
                self.oikea_vastaus = numero
            uudet_tekstit.append(teksti)
        self.aseta_tekstit(uudet_tekstit)
        # Aseta kysymysnumero.
        self.ui.nro_label.setText(f'{indeksi+1}/{len(self.tiedot)}')

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

        painettu_nappi = self.sender()

        if nappi == self.oikea_vastaus:
            self.pisteet += 1
            napin_vari = 'rgb(0,255,0)'
        else:
            napin_vari = 'rgb(255,0,0)'

        painettu_nappi.setStyleSheet(
            'QPushButton {background: ' + napin_vari + ';}')
        QApplication.processEvents()
        time.sleep(0.25)
        painettu_nappi.setStyleSheet('')

        self.seuraava_kysymys()

    def seuraava_kysymys(self):
        self.indeksi += 1
        if self.indeksi >= len(self.tiedot):
            laatikko = QMessageBox(self)
            if self.pisteet >= len(self.tiedot):
                laatikko.setText(f'Sait kaikki oikein {self.kierros} kierroksella!')
                self.kierros = 0
                self.tiedot = lataa_kysymykset_netista()
            else:
                laatikko.setText(f'Pisteesi: {self.pisteet}. Yritä uudelleen.')
            laatikko.exec()
            self.kierros += 1
            self.indeksi = 0
            self.pisteet = 0

        self.vaihda_kysymys_ja_vastaukset(self.indeksi)

    @property
    def pisteet(self):
        return self._pisteet

    @pisteet.setter
    def pisteet(self, arvo):
        self._pisteet = arvo
        self.paivita_tilarivi()

    def paivita_tilarivi(self):
        self.ui.statusbar.showMessage(f'Pisteet: {self.pisteet}')
        self.kierros_label.setText(f'Kierros: {self.kierros}')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
