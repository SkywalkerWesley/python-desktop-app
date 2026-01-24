import os
import traceback

import numpy as np
import pyqtgraph
from PyQt5 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg
from openpyxl.styles.builtins import calculation
from sympy import sympify
from numpy.ma.core import equal

from Code.Module_Main_1_3.Application.calculations.Calculations import Calculations
from Code.Module_Main_1_3.Application.mainUI.ExportWorker import ExportWorker
from Code.Module_Main_1_3.Application.mainUI.SamplePlotCalcWorker import SamplePlotCalcWorker
from Code.Module_Main_1_3.Application.uiElements.graph import Graph
from Code.Module_Main_1_3.Application.uiElements.button import Button
from Code.Module_Main_1_3.Application.uiElements.LineEdit import LineEdit

class SamplePlotsWidget(QtWidgets.QWidget):
    # Emitted for non-fatal issues the UI should surface
    softError = QtCore.pyqtSignal((str, str))

    def __init__(self, DefaultXAxisEquation, DefaultYAxisEquation, getVarsDict, parent=None):
        # # Sample Plot axises
        # self.DefaultXAxisEquation = "ln(Mass44 - CO2Zero44)"
        # self.DefaultYAxisEquation = "ln(Mass45 - CO2Zero45)"
        super().__init__(parent)
        
        pg.setConfigOptions(useOpenGL=False, antialias=True)
        self.xAxisEquation = sympify(DefaultXAxisEquation)
        self.yAxisEquation = sympify(DefaultYAxisEquation)
        self.sampleEquationXPlotData = []
        self.sampleEquationYPlotData = []
        self.lineEditList = []
        self.getVarsDict = getVarsDict
        self.lastData = dict()

        self.currentPlotData = dict()
        # UI Setup
        #  ______________________________________________________________
        #  | Top Bar                                      |             |
        #  |                                              |Sample Name  |
        #  |----------------------------------------------|-------------|
        #  |  graph                                       | Table       |
        #  |                                              |             |
        #  |                                              |             |
        #  |                                              |             |
        #  |                                              |             |
        #  |                                              |             |
        #  |----------------------------------------------|-------------|
        #  | Get Data Buttons                             | T Buttons   |
        #  |______________________________________________|_____________|

        ################################### Top Bar layout #############################################
        self.xAxisLabel = QtWidgets.QLabel("X Axis:")
        self.yAxisLabel = QtWidgets.QLabel("Y Axis:")
        self.emptyLabel = QtWidgets.QLabel("")

        self.xAxisLineEdit = LineEdit()
        self.yAxisLineEdit = LineEdit()

        self.xAxisLineEdit.setReadOnly(False)
        self.yAxisLineEdit.setReadOnly(False)

        self.xAxisLineEdit.setText(str(DefaultXAxisEquation))
        self.yAxisLineEdit.setText(str(DefaultYAxisEquation))

        self.OnEditedXAxis()
        self.OnEditedYAxis()

        self.lineEditList.extend([self.xAxisLineEdit, self.yAxisLineEdit])

        self.topBarGridLayout = QtWidgets.QFormLayout()
        self.topBarGridLayout.addRow(self.xAxisLabel, self.xAxisLineEdit)
        self.topBarGridLayout.addRow(self.yAxisLabel, self.yAxisLineEdit)

        ################################## Graph #####################################################
        self.calculationPlotGraph = Graph(100, 100)

        self.samplePlotGraphLayout = QtWidgets.QHBoxLayout()
        self.samplePlotGraphLayout.addWidget(self.calculationPlotGraph)
        self.setContentsMargins(0, 10, 0, 0)

        self.calculationPlotGraph2 = Graph(100, 100)
        self.calculationPlotGraph2.setLabel(axis='bottom', text='Time')
        self.calculationPlotGraph2.setLabel(axis='left', text='d²/dt² Mass44')

        # Curve
        self.calculationPlotGraph2Curve = pg.PlotDataItem(skipFiniteCheck=True, clipToView=True)
        self.calculationPlotGraph2Curve.setPen(color='#4363d8', width=4)

        self.calculationPlotGraph2.addItem(self.calculationPlotGraph2Curve)

        self.samplePlotGraphLayout.addWidget(self.calculationPlotGraph2)

        ################################## bottomBarLayout #####################################################
        self.calculationPlotAddDataButton = Button("Add Data", 120, 26)
        tempLable = QtWidgets.QLabel("Delta Part:")

        self.samplePlotDeltaPartLineEdit = LineEdit()
        self.samplePlotDeltaPartLineEdit.setReadOnly(False)

        bottomBarLayout = QtWidgets.QGridLayout()
        bottomBarLayout.addWidget(self.calculationPlotAddDataButton, 1, 1)
        bottomBarLayout.addWidget(tempLable, 1, 2)
        bottomBarLayout.addWidget(self.samplePlotDeltaPartLineEdit, 1, 3)

        ################################## Table Sample Name #####################################################
        sampleNameLamble = QtWidgets.QLabel("Sample Name:")
        self.sampleNameLineEdit = LineEdit()
        self.sampleNameLineEdit.setReadOnly(False)

        tableSampleNameLayout = QtWidgets.QFormLayout()
        tableSampleNameLayout.addRow(sampleNameLamble, self.sampleNameLineEdit)

        ################################## Table #####################################################
        self.calculationPlotTable = QtWidgets.QTableWidget()
        self.calculationPlotTable.setColumnCount(1)
        self.calculationPlotTable.setHorizontalHeaderLabels(["Samples"])
        self.calculationPlotTable.setRowCount(0)
        # makes table read only
        self.calculationPlotTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        ################################## Table Buttons #####################################################
        outterCalculationTableWidgetButtons = QtWidgets.QGridLayout()

        self.calculationPlotExportTableButton = Button("Export Table", 120, 26)
        self.calculationPlotClearTableButton = Button("Clear Table", 120, 26)

        outterCalculationTableWidgetButtons.addWidget(self.calculationPlotExportTableButton, 0, 0)
        outterCalculationTableWidgetButtons.addWidget(self.calculationPlotClearTableButton, 0, 1)

        ################################## Final Layout ##################################

        # Graph
        self.calculationPlotButtonLayoutAxisGraph = QtWidgets.QGridLayout()
        self.calculationPlotButtonLayoutAxisGraph.addLayout(self.topBarGridLayout, 1, 1)
        self.calculationPlotButtonLayoutAxisGraph.addLayout(self.samplePlotGraphLayout, 2, 1)
        self.calculationPlotButtonLayoutAxisGraph.addLayout(bottomBarLayout, 3, 1)

        # Table
        tableHalfLayout = QtWidgets.QGridLayout()
        tableHalfLayout.addLayout(tableSampleNameLayout, 0, 0)
        tableHalfLayout.addWidget(self.calculationPlotTable, 1, 0)
        tableHalfLayout.addLayout(outterCalculationTableWidgetButtons, 2, 0)

        # final layout
        self.sampleCalculationPlotsLayout = QtWidgets.QGridLayout()
        self.sampleCalculationPlotsLayout.addLayout(self.calculationPlotButtonLayoutAxisGraph, 1, 1)
        self.sampleCalculationPlotsLayout.setColumnStretch(1, 3)
        self.sampleCalculationPlotsLayout.addLayout(tableHalfLayout, 1, 2)
        self.setLayout(self.sampleCalculationPlotsLayout)

        ################################## Coonecting UI to to Methouds ##################################
        self.calculationPlotAddDataButton.clicked.connect(self.addSampleToSampleData)
        # Adds Equation from lineedit to plot
        self.xAxisLineEdit.returnPressed.connect(lambda: self.OnEditedXAxis())
        self.yAxisLineEdit.returnPressed.connect(lambda: self.OnEditedYAxis())
        # updates the plot when equations our changed
        self.xAxisLineEdit.returnPressed.connect(lambda: self.updateCustomCalcPlots(self.lastData))
        self.yAxisLineEdit.returnPressed.connect(lambda: self.updateCustomCalcPlots(self.lastData))

        # adds export table buttons
        self.calculationPlotExportTableButton.clicked.connect(lambda: self.exportSampleTable())
        self.calculationPlotClearTableButton.clicked.connect(self.clearSampleData)



    def addSampleToSampleData(self):
        """
        Adds sample data to sample table
        sample Data: (sampleName, (header, list of data), (header, list of data)...)
        :return:
        """
        #################### Sample Name ####################

        sampleName = self.sampleNameLineEdit.text()
        # checks that sample name is valid
        if not sampleName:
            sampleName = "null sample"
        sampleData = list()
        sampleData.append(sampleName)

        #################### equations plot ####################

        equationXName = self.xAxisLineEdit.text()
        equationYName = self.yAxisLineEdit.text()

        try:
            equationXData = self.currentPlotData["sampleEquationXPlotData"]
            equatoinYData = self.currentPlotData["sampleEquationYPlotData"]
        except:
            pass

        sampleData.append((equationXName, equationXData))
        sampleData.append((equationYName, equatoinYData))

        #################### Raw Data ####################
        data = self.getAllMeanBarData()

        allVars = self.xAxisEquiation.free_symbols.union(self.yAxisEquiation.free_symbols)

        rawData = {k: [] for k in allVars}
        for d in data:
            vars = self.getVarsDict(d)
            for v in allVars:
                rawData[v].append(Calculations.roundIfFloat(vars[str(v)], 5))

        for k in rawData.keys():
            sampleData.append((k, rawData[k]))
        #################### Adds Blank slope ####################
        sampleData.append(("Blank Slope 44", [self.blankSlope44LineEdit.text()]))
        sampleData.append(("Blank Slope 45", [self.blankSlope45LineEdit.text()]))

        #################### Adds Extract slope ####################
        sampleData.append(("Extract Slope 44", [self.extractSlope44LineEdit.text()]))
        sampleData.append(("Extract Slope 45", [self.extractSlope45LineEdit.text()]))

        #################### Adds line of best fit ####################
        slope, intecept = Calculations.getLineOfBestFit(equationXData, equatoinYData)
        sampleData.append(("Line Of Best Fit",
                           ["" + Calculations.roundIfFloat(str(slope), 5) + "*x" + " + " + Calculations.roundIfFloat(
                               str(intecept), 5)]))

        #################### Adds R^2 ####################
        r2 = self.currentPlotData["rSquared"]
        sampleData.append(("R^2", [str(r2)]))

        #################### Adds b44OverSlope ####################
        b44OverSlope = self.currentPlotData["b44OverSlope"]
        sampleData.append(("blank slope 44 / slope", [str(b44OverSlope)]))

        #################### Adds Alpha/Delta/Rubisco metrics ####################
        delta_part_val = self.samplePlotDeltaPartLineEdit.text()
        try:
            # α_total (slope)
            sampleData.append(("α_total (slope)", [str(round(self.currentPlotData["α_total (slope)"], 6))]))
        except:
            pass
        try:
            # Δ_part (input)
            delta_part_str = f"{delta_part_val} ({self.currentPlotData["delta_part"] * 1000:.2f} ‰)"
            sampleData.append(("Δ_part (input)", [delta_part_str]))
        except:
            pass
        try:
            # Δ_Rubisco
            delta_r = self.currentPlotData["delta_rubisco"]
            delta_rubisco_str = f"{round(delta_r, 6)} ({delta_r * 1000:.2f} ‰)"
            sampleData.append(("Δ_Rubisco", [delta_rubisco_str]))
        except:
            pass

        #################### Adds Data to save ####################
        self.samplePlotData.append(sampleData)

        # Adds sample to table
        self.calculationPlotTable.insertRow(0)
        self.calculationPlotTable.setItem(0, 0, QtWidgets.QTableWidgetItem(sampleName))

    def updateCustomCalcPlots(self, data):
        """ Updates the custom calculation plots with data from the mean bar
            Calls Async threads
        """
        # guard against multiple concurrent threads
        t = getattr(self, "_calcThread", None)
        if t is not None:
            try:
                if t.isRunning():
                    return
            except RuntimeError:
                self._calcThread = None
        self.calculationPlotGraph.setBackground(QtGui.QBrush(QtGui.QColor(0, 255, 0)))

        # Snapshot equations on the main thread
        xexp = self.xAxisEquiation
        yexp = self.yAxisEquiation

        self._calcThread = QtCore.QThread(self)
        self._calcWorker = SamplePlotCalcWorker(
            data=data,
            xexp=xexp,
            yexp=yexp,
            getVars=self.getVarsDict,
            deltaPart=self.samplePlotDeltaPartLineEdit.text(),
        )

        self._calcWorker.moveToThread(self._calcThread)
        self._calcThread.started.connect(self._calcWorker.run)

        # update plots on the thread
        self._calcWorker.resultReady.connect(self.applyCustomCalcResults)

        # Clean up
        self._calcWorker.finished.connect(self._calcThread.quit)
        self._calcWorker.finished.connect(self._calcWorker.deleteLater)
        self._calcThread.finished.connect(self._calcThread.deleteLater)
        self._calcThread.finished.connect(lambda: setattr(self, "_calcThread", None))

        # show warning to user on the main thread
        self._calcWorker.userWarning.connect(
            lambda msg: self.softError.emit("Calculation Warning", str(msg))
        )

        # Errors
        self._calcWorker.error.connect(
            lambda msg: self.softError.emit("Calculation Error", str(msg))
        )
        self._calcThread.start()

        self.lastData = data

    @QtCore.pyqtSlot(dict)
    def applyCustomCalcResults(self, res):
        """
        Apply custom calculation results to Calculations tab
        :param res:
        :return:
        """
        self.calculationPlotGraph.setBackground(QtGui.QBrush(QtGui.QColor(0, 0, 255)))

        try:
            self.calculationPlotGraph.clear()

            # Equation graph
            self.calculationPlotGraph.plot(
                res["lbfX"], res["lbfY"],
                pen=pg.mkPen(color=(255, 0, 0), width=2, style=QtCore.Qt.DashLine)
            )

            self.calculationPlotGraph.plot(
                res["sampleEquationPlotX"], res["sampleEquationPlotY"],
                pen=None, symbol='o', symbolBrush='r'
            )
            self.calculationPlotGraph.plot()

            # # r^2 and delta graph labels
            # try:
            #     rSquared = round(res["rSquared"], 5)
            # except:
            #     rSquared = "N/A"
            # try:
            #     delta = round(res["delta_rubisco"], 5)
            # except:
            #     delta = "N/A"
            # try:
            #     blank44OverBestFit = round(float(self.blankSlope44LineEdit.text()) / float(res["slope44"]), 5)
            # except:
            #     blank44OverBestFit = "N/A"
            #
            # text = pg.TextItem(f"R²={rSquared}\nDelta={delta}\nb44/slope={blank44OverBestFit}", color=(100, 255, 100), anchor=(1, 0))
            # # self.autoRangeToData(res["sampleEquationPlotX"], res["sampleEquationPlotY"], self.calculationPlotGraph, 0.1)
            # view = self.calculationPlotGraph.getViewBox()
            # x_range, y_range = view.viewRange()
            #
            # text.setPos(x_range[1], y_range[1])
            # self.calculationPlotGraph.addItem(text)
            # self.calculationPlotGraph.setBackground('white')
            #
            # # Time vs d²/dt²(Mass44)
            # times = res["d2_Time"]
            # d2 = res["d2_m44"]
            # self.calculationPlotGraph2Curve.setData(x=times, y=d2)
            #
            # # Rescale view
            # self.calculationPlotGraph2.setXRange(float(times[0]), float(times[-1]))
            # y_min, y_max = float(np.min(d2)), float(np.max(d2))
            # if y_min == y_max:
            #     pad = 1.0 if y_min == 0 else abs(y_min) * 0.1
            #     y_min -= pad
            #     y_max += pad
            # self.calculationPlotGraph2.setYRange(min(-1, y_min), max(1, y_max))
            #
            #
            # try:
            #     deltaPart = float(self.samplePlotDeltaPartLineEdit.text())
            # except:
            #     deltaPart = None

            # self.currentPlotData = {
            #     "sampleEquationXPlotData": Calculations.roundIfFloat(res["sampleX"], 5),
            #     "sampleEquationYPlotData": Calculations.roundIfFloat(res["sampleY"], 5),
            #     "rSquared": rSquared,
            #     "delta": delta,
            #     "α_total (slope)": res["α_total (slope)"],
            #     "delta_rubisco": res["delta_rubisco"],
            #     "delta_part": deltaPart,
            #     "b44OverSlope": blank44OverBestFit,
            # }

        except Exception as e:
            self.softError.emit("Plot Update Error", str(e))

    def drawPlots(self):


        print("wad")
    def exportSampleTable(self):
        """
        Exports data from samle table to csv file
        :return:
        """
        path = f'C:\\Users\\{self.user}\\Documents\\TableData'
        if not os.path.exists(path):
            os.makedirs(path)

        path, ok = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save File', path, "Excel Files (*.xlsx)"
        )

        if ok:
            self.statusBar().showMessage("Exporting data... please wait")

            self.thread = QtCore.QThread()
            self.worker = ExportWorker(path, self.samplePlotData)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.onExportFinished)
            self.worker.error.connect(self.onExportError)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()

    def clearSampleData(self):
        """
        Clears sample data and sample data table
        :return:
        """
        self.samplePlotData = []
        self.calculationPlotTable.clear()
        self.calculationPlotTable.setRowCount(0)

    def OnEditedXAxis(self):
        try:
            equationString = self.xAxisLineEdit.text()
            equation = sympify(equationString)
            # self.xAxisLineEdit.setText(str(equation))
            self.xAxisEquiation = equation
        except:
            self.softError.emit("Invalid Equation", f"{self.xAxisLineEdit.text()} is not a valid equation")

    def OnEditedYAxis(self):
        try:
            equationString = self.yAxisLineEdit.text()
            equation = sympify(equationString)
            # self.yAxisLineEdit.setText(str(equation))
            self.yAxisEquiation = equation
        except:
            self.softError.emit("Invalid Equation", f"{self.yAxisLineEdit.text()} is not a valid equation")

    def clearLineEdits(self):
        for lineEdit in self.lineEditList:
            lineEdit.setText("")

    def autoRangeToData(self, xs, ys, plot, padding):
        """ rescales plot to show all points
                :param {xs : List of x values}
                :param {ys : List of y values}
                :param {plot : Graph}
                :return -> None
        """

        try:
            xMin, xMax = min(xs), max(xs)
            yMin, yMax = min(ys), max(ys)

            if xMin == xMax:
                xMin -= 1
                xMax += 1
            if yMin == yMax:
                yMin -= 1
                yMax += 1

            xPadding = (xMax - xMin) * padding
            yPadding = (yMax - yMin) * padding

            plot.setXRange(xMin - xPadding, xMax + xPadding)
            plot.setYRange(yMin - yPadding, yMax + yPadding)
        except Exception:
            traceback.print_exc()
