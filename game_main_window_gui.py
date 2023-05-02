# -*- coding: utf-8 -*-
# Author: Vodohleb04
import datetime
import time

import PyQt5.QtBluetooth
# Form implementation generated from reading ui file 'mainGameWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import creature_stats_dialog
from ecosystem import EcoSystem
import configs
import time


AUTO_PERIOD_MUTEX = QtCore.QMutex()
STOP_AUTO_PERIOD_FLAG = False


def up_stop_auto_period_flag():
    global STOP_AUTO_PERIOD_FLAG
    STOP_AUTO_PERIOD_FLAG = True


class ToolBarSignals(QtCore.QObject):
    makeToolBar = QtCore.pyqtSignal()
    closeToolBar = QtCore.pyqtSignal()


class AutoPeriodThreadSignals(QtCore.QObject):
    next_period = QtCore.pyqtSignal()
    close_thread = QtCore.pyqtSignal()


class AutoPeriodRunnable(QtCore.QRunnable):
    def __init__(self, auto_period_thread_signal: AutoPeriodThreadSignals, auto_period_speed):
        self.auto_period_thread_signal = auto_period_thread_signal
        self._auto_period_speed = auto_period_speed
        super().__init__()
        self.auto_period_thread_signal.close_thread.connect(up_stop_auto_period_flag)

    @property
    def auto_period_speed(self) -> int:
        return self._auto_period_speed

    @auto_period_speed.setter
    def auto_period_speed(self, auto_period_speed):
        self._auto_period_speed = auto_period_speed

    def run(self):
        global STOP_AUTO_PERIOD_FLAG
        i = 0
        while True:
            AUTO_PERIOD_MUTEX.lock()
            if i >= 1000000 or STOP_AUTO_PERIOD_FLAG:
                STOP_AUTO_PERIOD_FLAG = False
                AUTO_PERIOD_MUTEX.unlock()
                break
            AUTO_PERIOD_MUTEX.unlock()
            self.auto_period_thread_signal.next_period.emit()
            time.sleep(configs.AutoPeriodParams.TIME.value / self._auto_period_speed)
            i += 1


class modExitMainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        self.tool_bar_signal = ToolBarSignals()
        self.tool_bar_active_flag = True
        self.auto_period_thread_signals = AutoPeriodThreadSignals()
        QtWidgets.QWidget.__init__(self, parent)
        window_icon = QtGui.QIcon()
        window_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["gui_windows_icon"]), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(window_icon)
        self.resize(300, 100)

    def closeEvent(self, event) -> None:
        result = QtWidgets.QMessageBox.question(
            self,
            "Подтверждение закрытия окна",
            "Вы действительно хотите закрыть окно?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Save,
            QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            AUTO_PERIOD_MUTEX.lock()
            self.auto_period_thread_signals.close_thread.emit()
            AUTO_PERIOD_MUTEX.unlock()
            event.accept()
            QtWidgets.QWidget.closeEvent(self, event)
        elif result == QtWidgets.QMessageBox.Save:
            # TODO Save
            event.accept()
            QtWidgets.QWidget.closeEvent(self, event)
        else:
            event.ignore()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key.Key_Escape:
            if self.tool_bar_active_flag:
                self.tool_bar_active_flag = False
                self.tool_bar_signal.closeToolBar.emit()
            else:
                self.tool_bar_active_flag = True
                self.tool_bar_signal.makeToolBar.emit()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, ecosystem: EcoSystem):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1158, 579)
        MainWindow.setMouseTracking(False)
        MainWindow.setTabletTracking(False)
        windowIcon = QtGui.QIcon()
        windowIcon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["gui_windows_icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(windowIcon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(255, 242, 254);")
        MainWindow.setStyleSheet("""QToolTip {background-color: white; 
                                              color: black; 
                                              border: black solid 1px}""")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setAnimated(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        MainWindow.setMinimumSize(1000, 579)

        self.auto_period_thread_signals = MainWindow.auto_period_thread_signals
        self.auto_period_thread_signals.next_period.connect(lambda: self.next_period(ecosystem))
        self.auto_period_thread = QtCore.QThreadPool()
        self.auto_period_runnable = None
        self.auto_period_speed = configs.AutoPeriodParams.MIN_SPEED.value
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(255, 250, 230);")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.wakeDeadlyWormButton = QtWidgets.QPushButton(self.centralwidget)
        self.wakeDeadlyWormButton.setBaseSize(QtCore.QSize(108, 32))
        self.wakeDeadlyWormButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.wakeDeadlyWormButton.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.wakeDeadlyWormButton.setObjectName("wakeDeadlyWordButton")
        self.gridLayout.addWidget(self.wakeDeadlyWormButton, 2, 6, 1, 1)

        self.addCreatureButton = QtWidgets.QPushButton(self.centralwidget)
        self.addCreatureButton.setBaseSize((QtCore.QSize(108, 32)))
        self.addCreatureButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addCreatureButton.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.addCreatureButton.setText("")
        add_creature_icon = QtGui.QIcon()
        add_creature_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["add_icon"]), QtGui.QIcon.Normal,
                                    QtGui.QIcon.Off)
        self.addCreatureButton.setIcon(add_creature_icon)
        self.addCreatureButton.setCheckable(False)
        self.addCreatureButton.setObjectName("addCreatureButton")
        self.gridLayout.addWidget(self.addCreatureButton, 2, 0, 1, 1)

        self.removeCreatureButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeCreatureButton.setBaseSize((QtCore.QSize(108, 32)))
        self.removeCreatureButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.removeCreatureButton.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.removeCreatureButton.setText("")
        add_creature_icon = QtGui.QIcon()
        add_creature_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["minus_icon"]), QtGui.QIcon.Normal,
                                    QtGui.QIcon.Off)
        self.removeCreatureButton.setIcon(add_creature_icon)
        self.removeCreatureButton.setCheckable(False)
        self.removeCreatureButton.setObjectName("removeCreatureButton")
        self.gridLayout.addWidget(self.removeCreatureButton, 2, 1, 1, 1)
        self.periodButton = QtWidgets.QPushButton(self.centralwidget)
        self.periodButton.setBaseSize(QtCore.QSize(108, 32))
        self.periodButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.periodButton.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.periodButton.setText("")
        period_icon = QtGui.QIcon()
        period_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["period_button_icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.periodButton.setIcon(period_icon)
        self.periodButton.setCheckable(False)
        self.periodButton.setObjectName("periodButton")
        self.gridLayout.addWidget(self.periodButton, 2, 2, 1, 1)
        self.reduceAutoSpeedButton = QtWidgets.QPushButton(self.centralwidget)
        self.reduceAutoSpeedButton.setEnabled(False)
        self.reduceAutoSpeedButton.setBaseSize(QtCore.QSize(108, 32))
        self.reduceAutoSpeedButton.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.reduceAutoSpeedButton.setObjectName("reduceAutoSpeedButton")
        self.gridLayout.addWidget(self.reduceAutoSpeedButton, 2, 3, 1, 1)
        self.autoPeriodButton = QtWidgets.QPushButton(self.centralwidget)
        self.autoPeriodButton.setBaseSize(QtCore.QSize(108, 32))
        self.autoPeriodButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.autoPeriodButton.setStatusTip("")
        self.autoPeriodButton.setWhatsThis("")
        self.autoPeriodButton.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.autoPeriodButton.setIconSize(QtCore.QSize(16, 16))
        self.autoPeriodButton.setCheckable(True)
        self.autoPeriodButton.setObjectName("autoPeriodButton")
        self.gridLayout.addWidget(self.autoPeriodButton, 2, 4, 1, 1)
        self.cellDataListWidget = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cellDataListWidget.sizePolicy().hasHeightForWidth())
        self.cellDataListWidget.setSizePolicy(sizePolicy)
        self.cellDataListWidget.setStyleSheet("background-color: rgb(247, 255, 238);")
        self.cellDataListWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.cellDataListWidget.setObjectName("cellDataListWidget")
        self.gridLayout.addWidget(self.cellDataListWidget, 0, 0, 2, 2)
        self.worldMapTable = QtWidgets.QTableWidget(self.centralwidget)
        self.worldMapTable.setStyleSheet("background-color: rgb(247, 255, 238);")
        self.worldMapTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.worldMapTable.setAutoScroll(False)
        self.worldMapTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.worldMapTable.setDragEnabled(False)
        self.worldMapTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.worldMapTable.setGridStyle(QtCore.Qt.SolidLine)
        self.worldMapTable.setCornerButtonEnabled(False)
        self.worldMapTable.setObjectName("worldMapTable")
        self.emplace_elements(ecosystem)
        self.gridLayout.addWidget(self.worldMapTable, 0, 2, 2, 6)
        self.increaseAutoSpeedButton = QtWidgets.QPushButton(self.centralwidget)
        self.increaseAutoSpeedButton.setEnabled(False)
        self.increaseAutoSpeedButton.setBaseSize(QtCore.QSize(108, 32))
        self.increaseAutoSpeedButton.setStatusTip("")
        self.increaseAutoSpeedButton.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.increaseAutoSpeedButton.setObjectName("increaseAutoSpeedButton")
        self.gridLayout.addWidget(self.increaseAutoSpeedButton, 2, 5, 1, 1)
        self.appocalipseButton = QtWidgets.QPushButton(self.centralwidget)
        self.appocalipseButton.setBaseSize(QtCore.QSize(108, 32))
        self.appocalipseButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.appocalipseButton.setStyleSheet("background-color: rgb(224, 224, 255);")
        self.appocalipseButton.setObjectName("appocalipseButton")
        self.gridLayout.addWidget(self.appocalipseButton, 2, 7, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setEnabled(True)
        self.toolBar.setMovable(False)
        self.toolBar.setAllowedAreas(QtCore.Qt.LeftToolBarArea)
        self.toolBar.setOrientation(QtCore.Qt.Vertical)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)

        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setEnabled(True)  # TODO (False)
        self.statusBar.setObjectName("statusBar")
        self.statusBar.show()
        MainWindow.setStatusBar(self.statusBar)

        self.newWorldAction = QtWidgets.QAction(MainWindow)
        add_icon = QtGui.QIcon()
        add_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["add_icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newWorldAction.setIcon(add_icon)
        self.newWorldAction.setIconVisibleInMenu(True)
        self.newWorldAction.setObjectName("newWorldAction")
        self.loadWorldAction = QtWidgets.QAction(MainWindow)
        load_icon = QtGui.QIcon()
        load_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["load_icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loadWorldAction.setIcon(load_icon)
        self.loadWorldAction.setObjectName("loadWorldAction")
        self.leaveWorldAction = QtWidgets.QAction(MainWindow)
        exit_icon = QtGui.QIcon()
        exit_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["exit_icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.leaveWorldAction.setIcon(exit_icon)
        self.leaveWorldAction.setObjectName("leaveWorldAction")
        self.exitGameAction = QtWidgets.QAction(MainWindow)
        linux_icon = QtGui.QIcon()
        linux_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["linux_icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitGameAction.setIcon(linux_icon)
        self.exitGameAction.setObjectName("exitGameAction")
        self.saveWorldAction = QtWidgets.QAction(MainWindow)
        save_icon = QtGui.QIcon()
        save_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["save_icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveWorldAction.setIcon(save_icon)
        self.saveWorldAction.setObjectName("saveWorldAction")
        self.helpAction = QtWidgets.QAction(MainWindow)
        question_icon = QtGui.QIcon()
        question_icon.addPixmap(QtGui.QPixmap(configs.SERVICE_ICONS["question_icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.helpAction.setIcon(question_icon)
        self.helpAction.setObjectName("helpAction")
        self.toolBar.addAction(self.newWorldAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.saveWorldAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.loadWorldAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.helpAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.leaveWorldAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.exitGameAction)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.saveWorldAction.triggered.connect(lambda: ecosystem.save())
        self.loadWorldAction.triggered.connect(lambda: self.showLoadFileDialog(MainWindow, ecosystem))
        self.exitGameAction.triggered.connect(MainWindow.close)
        MainWindow.tool_bar_signal.makeToolBar.connect(self.makeToolBarFunction)
        MainWindow.tool_bar_signal.closeToolBar.connect(self.closeToolBarFunction)

        self.worldMapTable.itemClicked.connect(lambda: self.show_creatures(ecosystem))
        self.cellDataListWidget.itemDoubleClicked.connect(lambda: self.show_creature_stats(MainWindow, ecosystem))
        self.periodButton.clicked.connect(lambda: self.next_period(ecosystem))
        self.wakeDeadlyWormButton.clicked.connect(lambda: self.wake_deadly_worm(ecosystem))
        self.appocalipseButton.clicked.connect(lambda: self.apocalypse(ecosystem))
        self.autoPeriodButton.clicked.connect(lambda: self.auto_period(ecosystem))
        self.increaseAutoSpeedButton.clicked.connect(self.increase_auto_speed)
        self.reduceAutoSpeedButton.clicked.connect(self.reduce_auto_speed)
        #self.removeCreatureButton.clicked.connect(lambda: ecosystem.remove_creature())

    def show_creature_stats(self, MainWindow: QtWidgets.QMainWindow, ecosystem: EcoSystem):
        creature_removed_signal = creature_stats_dialog.CreatureRemovedSignal()
        creature_removed_signal.creatureRemoved.connect(
            lambda: self.remove_creature(ecosystem,
                                         ecosystem.find_creture(self.cellDataListWidget.currentItem().text())))
        creature_stat_dialog_window = creature_stats_dialog.SignalingCreatureStatsDialog(creature_removed_signal,
                                                                                         parent=MainWindow)
        ui = creature_stats_dialog.Ui_creatureStatsDialog()

        try:
            ui.setupUi(creature_stat_dialog_window,
                       ecosystem,
                       ecosystem.find_creture(self.cellDataListWidget.currentItem().text()))
            creature_stat_dialog_window.show()
            creature_stat_dialog_window.exec()
        except ValueError as ex:
            error_msg_box = QtWidgets.QMessageBox()
            error_msg_box.setWindowTitle("Ошибка")
            error_msg_box.setText("Неизвестный тип существа")
            error_msg_box.setInformativeText(ex.args[0])
            error_msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            error_msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            error_msg_box.setDefaultButton(QtWidgets.QMessageBox.Ok)
            error_msg_box.adjustSize()
            error_msg_box.exec()
            return ex.args[0]

    def next_period(self, ecosystem: EcoSystem):
        ecosystem.cycle()
        self.update(ecosystem)
        self.statusBar.showMessage(configs.GuiMessages.PERIOD_SPEND.value, msecs=configs.MESSAGE_DURATION)

    def enabled_support_auto_period_buttons(self):
        if self.auto_period_speed <= configs.AutoPeriodParams.MIN_SPEED.value:
            self.reduceAutoSpeedButton.setEnabled(False)
            self.increaseAutoSpeedButton.setEnabled(True)
        elif self.auto_period_speed >= configs.AutoPeriodParams.MAX_SPEED.value:
            self.reduceAutoSpeedButton.setEnabled(True)
            self.increaseAutoSpeedButton.setEnabled(False)
        else:
            self.reduceAutoSpeedButton.setEnabled(True)
            self.increaseAutoSpeedButton.setEnabled(True)

    def cancel_auto_period_thread(self):
        if self.auto_period_runnable:
            AUTO_PERIOD_MUTEX.lock()
            self.auto_period_thread_signals.close_thread.emit()
            AUTO_PERIOD_MUTEX.unlock()
            self.auto_period_runnable = None

    def auto_period(self, ecosystem: EcoSystem):
        if self.autoPeriodButton.isChecked():
            self.cancel_auto_period_thread()
            self.auto_period_runnable = AutoPeriodRunnable(self.auto_period_thread_signals, self.auto_period_speed)
            self.periodButton.setEnabled(False)
            self.enabled_support_auto_period_buttons()
            self.auto_period_thread.start(self.auto_period_runnable)
        else:
            self.cancel_auto_period_thread()
            self.periodButton.setEnabled(True)
            self.reduceAutoSpeedButton.setEnabled(False)
            self.increaseAutoSpeedButton.setEnabled(False)

    def increase_auto_speed(self):
        self.auto_period_speed += 1
        AUTO_PERIOD_MUTEX.lock()
        if self.auto_period_runnable:
            self.auto_period_runnable.auto_period_speed = self.auto_period_speed
        AUTO_PERIOD_MUTEX.unlock()
        self.enabled_support_auto_period_buttons()

    def reduce_auto_speed(self):
        self.auto_period_speed -= 1
        AUTO_PERIOD_MUTEX.lock()
        if self.auto_period_runnable:
            self.auto_period_runnable.auto_period_speed = self.auto_period_speed
        AUTO_PERIOD_MUTEX.unlock()
        self.enabled_support_auto_period_buttons()

    def wake_deadly_worm(self, ecosystem: EcoSystem):
        ecosystem.provoke_deadly_worm()
        self.update(ecosystem)
        self.statusBar.showMessage(configs.GuiMessages.MANUAL_DEADLY_WORM.value, msecs=configs.MESSAGE_DURATION)

    def apocalypse(self, ecosystem: EcoSystem):
        before_apocalypse_message_box = QtWidgets.QMessageBox()
        before_apocalypse_message_box.setWindowTitle(f"Печати апокалипсиса")
        before_apocalypse_message_box.setText("Вы уверены, что хотите снять 7 печатей апокалипсиса?")
        before_apocalypse_message_box.setInformativeText(configs.GuiMessages.APOCALYPSE_INFORMATIVE_TEXT.value)
        before_apocalypse_message_box.setIcon(QtWidgets.QMessageBox.Question)
        before_apocalypse_message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        before_apocalypse_message_box.setDefaultButton(QtWidgets.QMessageBox.No)
        before_apocalypse_message_box.adjustSize()
        before_apocalypse_message_box.accepted.connect(lambda: ecosystem.apocalypse())
        before_apocalypse_message_box.exec()
        self.update(ecosystem)
        self.statusBar.showMessage(configs.GuiMessages.APOCALYPSE.value, msecs=configs.MESSAGE_DURATION)

    def remove_creature(self, ecosystem, creature):
        ecosystem.remove_creature(creature.id)
        self.update(ecosystem)
        self.statusBar.showMessage(f"Существо {creature.id} уничтожено безвозвратно", msecs=configs.MESSAGE_DURATION)

    def update(self, ecosystem: EcoSystem):
        self.update_table(ecosystem)
        self.show_creatures(ecosystem)

    def show_creatures(self, ecosystem: EcoSystem):
        self.cellDataListWidget.clear()
        if ecosystem.is_wasteland():
            item = QtWidgets.QListWidgetItem()
            brush = QtGui.QBrush(QtGui.QColor(244, 224, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            item.setBackground(brush)
            item.setText(configs.GuiMessages.WASTELAND_CREATURES_INFO.value)
            self.cellDataListWidget.addItem(item)
        else:
            for creature in ecosystem.forest.hectares[self.worldMapTable.currentRow()][self.worldMapTable.currentColumn()].creations:
                item = QtWidgets.QListWidgetItem()
                brush = QtGui.QBrush(QtGui.QColor(244, 224, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                item.setBackground(brush)
                item.setText(creature.id)
                self.cellDataListWidget.addItem(item)

    def update_table(self, ecosystem: EcoSystem):
        if ecosystem.is_wasteland():
            for i in range(len(ecosystem.forest.hectares)):
                for j in range(len(ecosystem.forest.hectares[i])):
                    cell_text = configs.GuiMessages.WASTELAND_MAP_INFO.value
                    self.worldMapTable.item(i, j).setText(cell_text)
        else:
            for i in range(len(ecosystem.forest.hectares)):
                for j in range(len(ecosystem.forest.hectares[i])):
                    cell_text = f"Существ в гектаре: {len(ecosystem.forest.hectares[i][j].creations)}"
                    self.worldMapTable.item(i, j).setText(cell_text)

    def table_elements_size_policy(self):
        self.worldMapTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.worldMapTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def emplace_elements(self, ecosystem: EcoSystem):
        self.worldMapTable.setColumnCount(ecosystem.forest.vertical_length)
        self.worldMapTable.setRowCount(ecosystem.forest.horizontal_length)
        self.worldMapTable.setHorizontalHeaderLabels([str(index) for index in range(1, ecosystem.forest.horizontal_length + 1)])
        self.worldMapTable.setVerticalHeaderLabels([str(index) for index in range(1, ecosystem.forest.vertical_length + 1)])
        self.table_elements_size_policy()
        row = 0
        for hectares_line in ecosystem.forest.hectares:
            column = 0
            for _ in hectares_line:
                item = QtWidgets.QTableWidgetItem()
                brush = QtGui.QBrush(QtGui.QColor(224, 224, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                item.setBackground(brush)
                self.worldMapTable.setItem(row, column, item)
                column += 1
            row += 1
        self.update_table(ecosystem)
        if not (ecosystem.forest.vertical_length == 0 or ecosystem.forest.horizontal_length == 0):
            self.worldMapTable.setCurrentCell(0, 0)
            self.show_creatures(ecosystem)

    def showLoadFileDialog(self, MainWindow: QtWidgets.QMainWindow, ecosystem: EcoSystem):
        import os
        fname = QFileDialog.getOpenFileName(MainWindow, 'Загрузить файл', '/home')[0]
        if not fname:
            self.filenameError(configs.GuiMessages.FILE_NOT_CHOSEN.value)
            return
        try:
            ecosystem.load(fname)
            self.update(ecosystem)
            _, file = os.path.split(fname)
            self.statusBar.showMessage(configs.GuiMessages.FILE_LOADED.value.format(file), msecs=configs.MESSAGE_DURATION)
        except ValueError as ve:
            self.filenameError(ve.args[0])

    def makeToolBarFunction(self):
        # TODO stop game
        self.toolBar.setEnabled(True)
        self.toolBar.setVisible(True)
        self.autoPeriodButton.setEnabled(False)

    def closeToolBarFunction(self):
        # TODO continue game
        self.toolBar.setEnabled(False)
        self.toolBar.setVisible(False)
        self.autoPeriodButton.setEnabled(True)

    def showSaveFileDialog(self, MainWindow: QtWidgets.QMainWindow, ecosystem: EcoSystem) -> None:
        fname = QFileDialog.getOpenFileName(MainWindow, 'Open file', '/home')[0]
        if not fname:
            self.filenameError(configs.GuiMessages.FILE_NOT_CHOSEN.value)
            return
        try:
            ecosystem.save(fname)
        except ValueError as ve:
            self.filenameError(ve.args[0])

    def filenameError(self, msg):
        error_msg_box = QMessageBox()
        error_msg_box.setWindowTitle("Файл не был выбран")
        error_msg_box.setText("Вы отменили выбор файла либо что-то пошло не так.")
        error_msg_box.setInformativeText(msg)
        error_msg_box.setIcon(QMessageBox.Information)
        error_msg_box.setStandardButtons(QMessageBox.Ok)
        error_msg_box.setDefaultButton(QMessageBox.Ok)
        error_msg_box.adjustSize()
        error_msg_box.exec()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", f"Forest EcoSystem {configs.VERSION}"))
        self.wakeDeadlyWormButton.setToolTip(_translate("MainWindow", "Пробудить смерточервя"))
        self.wakeDeadlyWormButton.setText(_translate("MainWindow", "Смерточервь"))
        self.wakeDeadlyWormButton.setShortcut(_translate("MainWindow", "W"))
        self.periodButton.setToolTip(_translate("MainWindow", "Сменить временной период"))
        self.periodButton.setShortcut(_translate("MainWindow", "N"))
        self.reduceAutoSpeedButton.setToolTip(_translate("MainWindow", "Замедлить течение времени (работает при при включенном автоматическом режиме)"))
        self.reduceAutoSpeedButton.setText(_translate("MainWindow", "Замедлить"))
        self.reduceAutoSpeedButton.setShortcut(_translate("MainWindow", "<"))
        self.autoPeriodButton.setToolTip(_translate("MainWindow", "Режим автоматической смены времени"))
        self.autoPeriodButton.setText(_translate("MainWindow", "Авто"))
        self.autoPeriodButton.setShortcut(_translate("MainWindow", "A"))
        __sortingEnabled = self.worldMapTable.isSortingEnabled()
        self.worldMapTable.setSortingEnabled(False)
        self.worldMapTable.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.cellDataListWidget.isSortingEnabled()
        self.cellDataListWidget.setSortingEnabled(False)
        self.cellDataListWidget.setSortingEnabled(__sortingEnabled)
        self.increaseAutoSpeedButton.setToolTip(_translate("MainWindow", "Ускорить течение времени (работает при при включенном автоматическом режиме)"))
        self.increaseAutoSpeedButton.setText(_translate("MainWindow", "Ускорить"))
        self.increaseAutoSpeedButton.setShortcut(_translate("MainWindow", ">"))
        self.appocalipseButton.setToolTip(_translate("MainWindow", "Вызвать апокалипсис"))
        self.appocalipseButton.setText(_translate("MainWindow", "Апокалипсис"))
        self.appocalipseButton.setShortcut(_translate("MainWindow", "Del"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.newWorldAction.setText(_translate("MainWindow", "Создать новый мир"))
        self.loadWorldAction.setText(_translate("MainWindow", "Загрузить мир"))
        self.loadWorldAction.setToolTip(_translate("MainWindow", "Загрузить мир F9"))
        self.loadWorldAction.setShortcut(_translate("MainWindow", "F9"))
        self.leaveWorldAction.setText(_translate("MainWindow", "Покинуть мир"))
        self.exitGameAction.setText(_translate("MainWindow", "Выйти на рабочий стол"))
        self.saveWorldAction.setText(_translate("MainWindow", "Сохранить мир"))
        self.saveWorldAction.setToolTip(_translate("MainWindow", "Сохранить мир F5"))
        self.saveWorldAction.setShortcut(_translate("MainWindow", "F5"))
        self.helpAction.setText(_translate("MainWindow", "Помощь"))
        self.helpAction.setToolTip(_translate("MainWindow", "Помощь F11"))
        self.helpAction.setShortcut(_translate("MainWindow", "F11"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = modExitMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, EcoSystem())
    MainWindow.show()
    sys.exit(app.exec_())
