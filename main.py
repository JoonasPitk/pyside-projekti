import sys
from PySide6.QtWidgets import QApplication, QMainWindow

from quiz_ui import Ui_MainWindow

KYSYMYKSET_JA_VASTAUKSET = [
    (
        'Mistä Python-ohjelmointikieli on saanut nimensä?',
        'Käärmeestä',
        'Laulusta',
        '*TV-sarjasta',
        'Elokuvasta'
    ),
    (
        'Paljonko on 5*5?'
        '15'
        '10'
        '30'
        '*25'
    )
]

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.vaihda_kysymykset_ja_vastaukset(0)

    def vaihda_kysymykset_ja_vastaukset(self, indeksi):
        tekstit = KYSYMYKSET_JA_VASTAUKSET[indeksi]
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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())