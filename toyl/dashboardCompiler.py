#!/usr/bin/python
import os

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox,
                             QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QPushButton, QRadioButton, QSizePolicy,
                             QStyleFactory, QTableWidget, QTabWidget,
                             QVBoxLayout, QWidget, QPlainTextEdit)

import sys
from toyl.lexer import ToyLexer
from toyl.parser import ToyParser
from toyl.ast import BaseASTNode


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        self.showMaximized()
        self.textEditprocessedSourceCode = None
        self.textEditSourceCode = None

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("E&stilo:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Usar estilos predeterminados")
        self.useStylePaletteCheckBox.setChecked(True)

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0, 2, 1)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomRightTabWidget, 2, 1)

        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)

        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 2)

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
        self.topLeftGroupBox = QGroupBox("Source Code")
        self.topLeftGroupBox.setCheckable(True)
        self.topLeftGroupBox.setChecked(True)

        self.textEditSourceCode = QPlainTextEdit()
        self.textEditSourceCode.setFont(QFont("Arial", 12))

        content = self.read_file()
        self.textEditSourceCode.setPlainText(content)

        layout = QGridLayout()
        layout.addWidget(self.textEditSourceCode, 0, 0, 1, 2)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):

        self.bottomRightTabWidget = QTabWidget()
        self.bottomRightTabWidget.setSizePolicy(QSizePolicy.Preferred,
                                                QSizePolicy.Ignored)

        tab1 = QWidget()
        self.textEditprocessedSourceCode = QPlainTextEdit()

        self.textEditprocessedSourceCode.setPlainText("")
        self.textEditprocessedSourceCode.setFont(QFont("Arial", 12))

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(self.textEditprocessedSourceCode)

        tab1.setLayout(tab1hbox)

        self.bottomRightTabWidget.addTab(tab1, "Source Code Procesado.")

        self.topRightGroupBox = QGroupBox("Opciones", self)

        tokenizarPushButton = QPushButton("Tokenizar Source Code (Generar lexemas)", self)
        tokenizarPushButton.setToolTip('Tokenizar Source Code')
        tokenizarPushButton.setDefault(True)
        tokenizarPushButton.clicked.connect(self.on_clickTokenizar)

        interpreterPushButton = QPushButton("Ejecutar programa fuente (Interpretar)")
        interpreterPushButton.setToolTip('Ejecutar programa fuente (Interpretar)')
        interpreterPushButton.setChecked(True)
        interpreterPushButton.clicked.connect(self.on_clickInterpreter)

        cleanerPushButton = QPushButton("Clean TextBox")
        cleanerPushButton.setToolTip('Limpiar TextBox resultados')
        cleanerPushButton.setChecked(True)
        cleanerPushButton.clicked.connect(self.on_clickCleanResults)

        layout = QVBoxLayout()
        layout.addWidget(tokenizarPushButton)
        layout.addWidget(interpreterPushButton)
        layout.addWidget(cleanerPushButton)

        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    @pyqtSlot()
    def on_clickCleanResults(self):
        print('Limpiar resultados')
        self.textEditprocessedSourceCode.clear()
        BaseASTNode.clean_result()

    @pyqtSlot()
    def on_clickTokenizar(self):
        print('Tokenizer button click')
        self.textEditprocessedSourceCode.clear()
        BaseASTNode.clean_result()
        # Create lexer
        print("Tokenizando...")
        lexer = ToyLexer()
        try:
            for tok in lexer.tokenize(self.textEditSourceCode.toPlainText()):
                BaseASTNode.add_result(
                    'TOKEN: {token:' '<15} {val:' '>15}'.format(token=tok.type, val=tok.value))
        except (ValueError, RuntimeError, TypeError, NameError):
            print('Error tokenizando entrada')

        for op in BaseASTNode.get_result():
            self.textEditprocessedSourceCode.appendPlainText(op)

    @pyqtSlot()
    def on_clickInterpreter(self):
        self.textEditprocessedSourceCode.clear()
        BaseASTNode.clean_result()
        # Limpio la variable resultado, ya que de tener un valor es de la ejecucion anterior
        BaseASTNode.clean_result()
        # Create lexer
        print("Tokenizando...")
        lexer = ToyLexer()
        # print(self.textEditSourceCode.toPlainText())
        # Create parser
        print("Parseando...")
        parser = ToyParser()
        # ast es el arbol AST expresado a traves de un objeto principal Statements
        ast = parser.parse(lexer.tokenize(self.textEditSourceCode.toPlainText()))
        try:
            ast.eval()
        except ValueError as valueError:
            print("Error Semantico; {0}".format(valueError))
        except AttributeError as attributeError:
            # ValueError, TypeError, NameError,
            print("Error Sintactico; {0}".format(attributeError))
        except:
            print("Error inesperado:", sys.exc_info()[0])

        # Imprimiendo el resultado de la lista de resultados del programa
        for op in BaseASTNode.get_result():
            self.textEditprocessedSourceCode.appendPlainText(str(op))

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
