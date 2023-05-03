# -*- coding: utf-8 -*-
#Author: Vodohleb04

# Form implementation generated from reading ui file 'addCreaturesDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from ecosystem import EcoSystem
import configs


class AddCreaturesSignal(QtCore.QObject):
    updateMapSignal = QtCore.pyqtSignal()


class SignalingAddCreaturesDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        self.addCreaturesSignal = AddCreaturesSignal()
        QtWidgets.QWidget.__init__(self, parent)


class Ui_addCreaturesDialog(object):
    def setupUi(self, addCreaturesDialog: SignalingAddCreaturesDialog, ecosystem: EcoSystem,
                vertical_hectare_number, horizontal_hectare_number):
        addCreaturesDialog.setObjectName("newCreatureDialog")
        addCreaturesDialog.resize(661, 284)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(255)
        sizePolicy.setVerticalStretch(255)
        sizePolicy.setHeightForWidth(addCreaturesDialog.sizePolicy().hasHeightForWidth())
        addCreaturesDialog.setSizePolicy(sizePolicy)
        addCreaturesDialog.setBaseSize(QtCore.QSize(0, 0))
        window_icon = QtGui.QIcon()
        window_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["gui_windows_icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        addCreaturesDialog.setWindowIcon(window_icon)
        addCreaturesDialog.setStyleSheet("background-color: rgb(255, 242, 254);")
        addCreaturesDialog.setStyleSheet("""QToolTip {background-color: white; 
                                                     color: black; 
                                                     border: black solid 1px}""")
        addCreaturesDialog.setSizeGripEnabled(False)
        addCreaturesDialog.setModal(False)
        self.gridLayout = QtWidgets.QGridLayout(addCreaturesDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.dialogDoneButtonBox = QtWidgets.QDialogButtonBox(addCreaturesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dialogDoneButtonBox.sizePolicy().hasHeightForWidth())
        self.dialogDoneButtonBox.setSizePolicy(sizePolicy)
        self.dialogDoneButtonBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dialogDoneButtonBox.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.dialogDoneButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.dialogDoneButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dialogDoneButtonBox.setObjectName("dialogDoneButtonBox")
        self.dialogDoneButtonBox.setFocus()
        self.gridLayout.addWidget(self.dialogDoneButtonBox, 5, 6, 1, 2)
        self.removeButton = QtWidgets.QPushButton(addCreaturesDialog)
        self.removeButton.setEnabled(False)
        self.removeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.removeButton.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.removeButton.setText("")
        minus_icon = QtGui.QIcon()
        minus_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["minus_icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeButton.setIcon(minus_icon)
        self.removeButton.setObjectName("removeButton")
        self.gridLayout.addWidget(self.removeButton, 4, 7, 1, 1)
        self.addedTable = QtWidgets.QTableWidget(addCreaturesDialog)
        self.addedTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.addedTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.addedTable.setObjectName("addedTable")
        self.addedTable.setColumnCount(2)
        for i in range(3):
            self.addedTable.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())
        self.addedTable.setRowCount(0)
        self.addedTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.addedTable.setCornerButtonEnabled(False)
        self.addedTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.gridLayout.addWidget(self.addedTable, 0, 0, 1, 8)
        self.addButton = QtWidgets.QPushButton(addCreaturesDialog)
        self.addButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy)
        self.addButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addButton.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.addButton.setText("")
        add_icon = QtGui.QIcon()
        add_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["add_icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(add_icon)
        self.addButton.setObjectName("addButton")
        self.gridLayout.addWidget(self.addButton, 4, 6, 1, 1)
        self.creatureTypeBox = QtWidgets.QComboBox(addCreaturesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.creatureTypeBox.sizePolicy().hasHeightForWidth())
        self.creatureTypeBox.setSizePolicy(sizePolicy)
        self.creatureTypeBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.creatureTypeBox.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.creatureTypeBox.setObjectName("creatureTypeBox")
        self.creatureTypeBox.addItem("")
        self.creatureTypeBox.addItem("")
        self.creatureTypeBox.addItem("")
        self.creatureTypeBox.addItem("")
        self.creatureTypeBox.addItem("")
        self.creatureTypeBox.addItem("")
        self.creatureTypeBox.addItem("")
        self.gridLayout.addWidget(self.creatureTypeBox, 4, 1, 1, 1)
        self.creatureAmountSpinBox = QtWidgets.QSpinBox(addCreaturesDialog)
        self.creatureAmountSpinBox.setEnabled(True)
        self.creatureAmountSpinBox.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.creatureAmountSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.creatureAmountSpinBox.setSpecialValueText("")
        self.creatureAmountSpinBox.setMinimum(1)
        self.creatureAmountSpinBox.setMaximum(10)
        self.creatureAmountSpinBox.setObjectName("creatureAmountSpinBox")
        self.gridLayout.addWidget(self.creatureAmountSpinBox, 4, 5, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 5)

        self.retranslateUi(addCreaturesDialog)
        self.dialogDoneButtonBox.accepted.connect(addCreaturesDialog.accept)  # type: ignore
        self.dialogDoneButtonBox.rejected.connect(addCreaturesDialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(addCreaturesDialog)
        self.creatureTypeBox.activated.connect(lambda: self._activate_parameters())
        self.addButton.clicked.connect(self._add_creature)
        self.addedTable.itemSelectionChanged.connect(self._activate_remove_button)
        self.removeButton.clicked.connect(self._remove_added_element)
        addCreaturesDialog.accepted.connect(
            lambda: self.add_creatures_to_ecosystem(ecosystem, addCreaturesDialog.addCreaturesSignal.updateMapSignal,
                                                    vertical_hectare_number, horizontal_hectare_number))

    def add_creatures_to_ecosystem(self, ecosystem: EcoSystem, update_ecosystem_signal,
                                   vertical_hectare_number, horizontal_hectare_number):
        for i in range(self.addedTable.rowCount()):
            ecosystem.fill_creatures(ecosystem.define_creature_kind_from_russian(self.addedTable.item(i, 0).text()),
                                     int(self.addedTable.item(i, 1).text()),
                                     (vertical_hectare_number, horizontal_hectare_number))
        update_ecosystem_signal.emit()

    def _activate_remove_button(self):
        if self.addedTable.currentItem():
            self.removeButton.setEnabled(True)
        else:
            self.removeButton.setEnabled(False)

    def _remove_added_element(self):
        current_row = self.addedTable.currentRow()
        self.addedTable.removeRow(self.addedTable.currentRow())
        current_row -= 0 if current_row == 0 else 1
        self.addedTable.setCurrentCell(current_row, 0)

    def _activate_parameters(self):
        self.creatureAmountSpinBox.setEnabled(True)
        self.addButton.setEnabled(True)

    def _make_item(self, brush, text_to_set=""):
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(brush)
        item.setText(text_to_set)
        return item

    def _element_row_index(self, creature_type: str) -> int:
        row_index = 0
        while row_index < self.addedTable.rowCount():
            if self.addedTable.item(row_index, 0).text() == creature_type:
                return row_index
            row_index += 1
        return row_index

    def _add_creature(self):
        brush = QtGui.QBrush(QtGui.QColor(224, 224, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        if self._element_row_index(self.creatureTypeBox.currentText()) < self.addedTable.rowCount():
            self.addedTable.setItem(self._element_row_index(self.creatureTypeBox.currentText()),
                                    1, self._make_item(brush, str(self.creatureAmountSpinBox.value())))
        else:
            self.addedTable.insertRow(self.addedTable.rowCount())
            self.addedTable.setItem(self.addedTable.rowCount() - 1, 0,
                                    self._make_item(brush, self.creatureTypeBox.currentText()))
            self.addedTable.setItem(self.addedTable.rowCount() - 1, 1,
                                    self._make_item(brush, str(self.creatureAmountSpinBox.value())))


    def retranslateUi(self, newCreatureDialog):
        _translate = QtCore.QCoreApplication.translate
        newCreatureDialog.setWindowTitle(_translate("newCreatureDialog", "Добавление существ"))
        item = self.addedTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Вид существа"))
        item = self.addedTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Количество"))
        self.creatureTypeBox.setItemText(0, _translate("newCreatureDialog",
                                                       configs.RussianCreaturesNames.BLUEBERRY.value))
        self.creatureTypeBox.setItemText(1, _translate("newCreatureDialog", configs.RussianCreaturesNames.HAZEL.value))
        self.creatureTypeBox.setItemText(2, _translate("newCreatureDialog", configs.RussianCreaturesNames.MAPLE.value))
        self.creatureTypeBox.setItemText(3, _translate("newCreatureDialog", configs.RussianCreaturesNames.BOAR.value))
        self.creatureTypeBox.setItemText(4, _translate("newCreatureDialog", configs.RussianCreaturesNames.ELK.value))
        self.creatureTypeBox.setItemText(5, _translate("newCreatureDialog", configs.RussianCreaturesNames.WOLF.value))
        self.creatureTypeBox.setItemText(6, _translate("newCreatureDialog", configs.RussianCreaturesNames.BEAR.value))
        self.creatureTypeBox.setPlaceholderText(_translate("newCreatureDialog", "Выберите тип существа..."))
        self.addButton.setToolTip(_translate("MainWindow", "Разместить в список на добавление, +"))
        self.addButton.setShortcut(_translate("MainWindow", "+"))
        self.removeButton.setToolTip(_translate("MainWindow", "Убрать из списка на добавление, -"))
        self.removeButton.setShortcut(_translate("MainWindow", "-"))

