#!/usr/bin/python
import os

from PyQt5.QtCore import QDateTime, Qt, QTimer, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget)

import sys
from builtins import print
from lexer import Lexer
from parser import Parser


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.textEditprocessedSourceCode = None
        self.textEditSourceCode = None

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("E&stilo:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Usar estilos predeterminados")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Deshabilitar widgets")

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        # self.createbottomRightTabWidget()
        self.createbottomLeftGroupBox()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomRightTabWidget.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomLeftGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftGroupBox, 2, 0)
        mainLayout.addWidget(self.bottomRightTabWidget, 2, 1)
        # mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Proyecto X")
        self.changeStyle('fusion')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if self.useStylePaletteCheckBox.isChecked():
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Input")

        radioButton1 = QRadioButton("Radio button 1")
        radioButton2 = QRadioButton("Radio button 2")
        radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):

        # def createbottomRightTabWidget(self):
        self.bottomRightTabWidget = QTabWidget()
        self.bottomRightTabWidget.setSizePolicy(QSizePolicy.Preferred,
                                                QSizePolicy.Ignored)

        tab1 = QWidget()
        self.textEditprocessedSourceCode = QTextEdit()

        self.textEditprocessedSourceCode.setPlainText("")

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(self.textEditprocessedSourceCode)
        tab1.setLayout(tab1hbox)

        self.bottomRightTabWidget.addTab(tab1, "Source Code Procesado.")

        self.topRightGroupBox = QGroupBox("Opciones", self)

        tokenizarPushButton = QPushButton("Tokenizar Source Code", self)
        tokenizarPushButton.setToolTip('This is an example button')
        tokenizarPushButton.setDefault(True)
        tokenizarPushButton.clicked.connect(self.on_clickTokenizar)

        parsearPushButton = QPushButton("Parsear Source Code", self)
        parsearPushButton.setToolTip('This is an example button')
        parsearPushButton.setChecked(True)
        parsearPushButton.clicked.connect(self.on_clickParser)

        interpreterPushButton = QPushButton("Interpretar Source Code")
        interpreterPushButton.setToolTip('This is an example button')
        interpreterPushButton.setChecked(True)
        interpreterPushButton.clicked.connect(self.on_clickInterpreter)

        layout = QVBoxLayout()
        layout.addWidget(tokenizarPushButton)
        layout.addWidget(parsearPushButton)
        layout.addWidget(interpreterPushButton)

        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createbottomLeftGroupBox(self):

        # -----------------------------------------------------------------------------------
        self.bottomLeftGroupBox = QGroupBox("Source Code")
        self.bottomLeftGroupBox.setCheckable(True)
        self.bottomLeftGroupBox.setChecked(True)

        self.textEditSourceCode = QTextEdit()

        content = self.read_file()

        self.textEditSourceCode.setPlainText(content)

        # lineEdit = QLineEdit('s3cRe7')
        # lineEdit.setEchoMode(QLineEdit.Password)

        # spinBox = QSpinBox(self.bottomLeftGroupBox)
        # spinBox.setValue(50)

        # dateTimeEdit = QDateTimeEdit(self.bottomLeftGroupBox)
        # dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        # slider = QSlider(Qt.Horizontal, self.bottomLeftGroupBox)
        # slider.setValue(40)

        # scrollBar = QScrollBar(Qt.Horizontal, self.bottomLeftGroupBox)
        # scrollBar.setValue(60)

        # dial = QDial(self.bottomLeftGroupBox)
        # dial.setValue(30)
        # dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(self.textEditSourceCode, 0, 0, 1, 2)
        # layout.addWidget(lineEdit, 0, 0, 1, 2)
        # layout.addWidget(spinBox, 1, 0, 1, 2)
        # layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        # layout.addWidget(slider, 3, 0)
        # layout.addWidget(scrollBar, 4, 0)
        # layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottomLeftGroupBox.setLayout(layout)

    @pyqtSlot()
    def on_clickTokenizar(self):
        print('Tokenizer button click')
        # Create lexer
        lexer = Lexer().get_lexer()
        tokens = lexer.lex(self.read_file())

        text = None
        for tok in tokens:
            print('type=%r, value=%r' % (tok.gettokentype(), tok.getstr()))
            # text += (str(tok.gettokentype()) + str(tok.getstr()))
            self.textEditprocessedSourceCode.append(tok.gettokentype() + '---' + tok.getstr())

    @pyqtSlot()
    def on_clickParser(self):
        print('Parser button click')
        # Create lexer
        lexer = Lexer().get_lexer()
        tokens = lexer.lex(self.textEditSourceCode)
        # Create parser
        pg = Parser()
        pg.parse()
        parser = pg.get_parser()

        self.textEditprocessedSourceCode.setPlainText("")

    @pyqtSlot()
    def on_clickInterpreter(self):
        print('Interpreter button click')
        # Create lexer
        lexer = Lexer().get_lexer()
        tokens = lexer.lex(self.textEditSourceCode)
        # Create parser
        pg = Parser()
        pg.parse()
        parser = pg.get_parser()

        self.textEditprocessedSourceCode.setPlainText("text")
        parser.parse(tokens).eval()
        names = pg.get_names().get_all_symbols()
        print('Imprimiendo tabla de simbolos')
        for sym in names.keys():
            print('Simbolo : ' + str(sym) + ' = ' + str(pg.get_names().get_symbol(sym).get_value()) + ' - '
                  + pg.get_names().get_symbol(sym).get_type())


    def read_file(self):
        # Leo el archivo que se indique ...y lo muestro del lado izquierdo de la pantalla
        content = ""  # Esta variable mandendra el contenido del archivo de entrada leido
        path = os.getcwd()

        print('|-|-|-|-|-|-|-|-|-|-|-|-|-|-  Starting Interpreter  |-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|- \n')
        print("Leyendo archivo...")

        # Verifico que el usuario haya ingresado el nombre del archivo como parametro
        try:
            fileName = sys.argv[1]
        except:
            print(
                "[ERROR] Se esperaba el nombre de archivo, como parametro para iniciar procesamiento, por ejemplo: 'demo.x'")
            return

        # Chequeo si la extension del archivo es correcta
        if fileName[len(fileName) - 2:len(fileName)] != ".x":
            print("[ERROR] Extension de archivo no reconocida, asegurese que la extension del archivo sea '.x'")
            return

        # Abre el archivo de entrada (en modo lectura) y lo graba en la variable 'content'
        try:
            with open(path + "/" + fileName, "r") as sourceCodeFile:
                content = sourceCodeFile.read()
        except:
            print('[ERROR] No se puede encontrar el archivo "' + fileName + '"')

        return content


if __name__ == '__main__':
    app = QApplication([])
    gallery = WidgetGallery()
    gallery.show()
    app.exec_()
