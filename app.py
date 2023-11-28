import io
import sys
import sqlite3
import random
import datetime
# import asyncio
from ui.uiProj import temp

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem, QFileDialog


class TestingSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(temp)
        uic.loadUi(f, self)
        self.initUi()

    def initUi(self) -> None:
        self.params()
        self.connectionMenu()
        self.startMenu()

    def params(self):
        self.lastClkClass = 0
        self.lastClkProgram = ''
        self.lastIdTest = 0
        self.sessionPage = 1
        self.lastAnswer = ''
        self.lastInsertFile = ''
        self.points = 0
        self.acceptBtn.setEnabled(False)
        self.ownVersion = False
        self.authorization = False
        self.dict_programs_mini_versions = {'Mathematics': 'Math',
                                            'Russian language': 'Rus',
                                            'Surrounding world': 'SurWrd',
                                            'English language': 'Eng',
                                            'Literature': 'Lit',
                                            'Logical thinking': 'Logical'
                                            }

    def connectionMenu(self) -> None:
        self.saveBtn.clicked.connect(self.profileSave)

        self.profile.clicked.connect(self.gotoProfile)
        self.taskDetails.clicked.connect(self.gotoTaskDetails)
        self.stats.clicked.connect(self.gotoStats)

        rec_buttons = [self.recBtn1, self.recBtn2, self.recBtn3, self.recBtn4]
        for item in rec_buttons:
            item.clicked.connect(
                lambda: self.stackedWidget.setCurrentWidget(self.recPage))

        self.insertFileBtn.clicked.connect(self.insertFile)
        self.acceptBtn.clicked.connect(self.acceptFile)

        self.selectRBtn.clicked.connect(self.selectR)
        self.mainSelectRBtn.clicked.connect(self.mainSelectR)

        self.dailyTestBtn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.dailyTestPage))

        self.class1Btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.class1TestPage))
        self.class2Btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.class2TestPage))
        self.class3Btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.class3TestPage))
        self.class4Btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.class4TestPage))

        buttons = [self.enBtn4, self.lBtn4,
                   self.lthBtn4, self.mathBtn4, self.rlBtn4, self.swBtn4,
                   self.enBtn3, self.lBtn3,
                   self.lthBtn3, self.mathBtn3, self.rlBtn3, self.swBtn3,
                   self.enBtn2,
                   self.lthBtn2, self.mathBtn2, self.rlBtn2, self.swBtn2,
                   self.lthBtn1, self.mathBtn1, self.rlBtn1, self.swBtn1
                   ]
        for item in buttons:
            item.clicked.connect(
                lambda: self.stackedWidget.setCurrentWidget(self.testingPage))

        self.testFinishBtn.clicked.connect(self.testResult)

        self.class1Btn.clicked.connect(self.lastClkClass1)
        self.class2Btn.clicked.connect(self.lastClkClass2)
        self.class3Btn.clicked.connect(self.lastClkClass3)
        self.class4Btn.clicked.connect(self.lastClkClass4)

        self.testABtn_2.clicked.connect(self.btnAClicked)
        self.testBBtn_2.clicked.connect(self.btnBClicked)
        self.testCBtn_2.clicked.connect(self.btnCClicked)
        self.testDBtn_2.clicked.connect(self.btnDClicked)

        math = [self.mathBtn1, self.mathBtn2, self.mathBtn3, self.mathBtn4]
        for item in math:
            item.clicked.connect(self.lastClkMathematics)
        rl = [self.rlBtn1, self.rlBtn2, self.rlBtn3, self.rlBtn4]
        for item in rl:
            item.clicked.connect(self.lastClkRussianlanguage)
        sw = [self.swBtn1, self.swBtn2, self.swBtn3, self.swBtn4]
        for item in sw:
            item.clicked.connect(self.lastClkSurroundingworld)
        en = [self.enBtn2, self.enBtn3, self.enBtn4]
        for item in en:
            item.clicked.connect(self.lastClkEnglishlanguage)
        l = [self.lBtn3, self.lBtn4]
        for item in l:
            item.clicked.connect(self.lastClkLiterature)
        lth = [self.lthBtn1, self.lthBtn2, self.lthBtn3, self.lthBtn4]
        for item in lth:
            item.clicked.connect(self.lastClkLogicalthinking)

    def startMenu(self) -> None:
        self.taskDetails.setEnabled(False)
        self.stats.setEnabled(False)

    def profileSave(self) -> None:
        try:
            name = self.nameEdit.text()
            about = self.aboutEdit.toPlainText()
            number = self.numberEdit.text()
            email = self.emailEdit.text()
            password = self.passwordEdit.text()
            if name != 'InputName':
                con = sqlite3.connect(r'databases\app.db')
                cur = con.cursor()
                registration = cur.execute(
                    f'SELECT * FROM users WHERE id_name = "{name}"').fetchone()
                if registration is None:
                    cur.execute(f'''INSERT INTO users (id_name, PASSWORD, about, number, email, points, iq, completed, daily_test, decided_now, level_points)
                                    VALUES ("{name}", "{password}", "{about}", "{number}", "{email}", 0, 0, 0 ,0, 0, 0)''')
                    self.authorization = True
                    self.nameEdit.setEnabled(False)
                    self.passwordEdit.setEnabled(False)
                    self.taskDetails.setEnabled(True)
                    self.stats.setEnabled(True)
                else:
                    password_true = cur.execute(
                        f'''SELECT PASSWORD FROM users WHERE id_name = "{name}"''').fetchone()[0]
                    if password_true == password:
                        cur.execute(f'''UPDATE users SET decided_now = 0 WHERE id_name = "{name}"'''
                                    )
                        if not self.authorization:
                            self.authorization = True
                            info = cur.execute(
                                f'''SELECT about, number, email, level_points FROM users WHERE id_name = "{name}"''').fetchone()
                            self.aboutEdit.setText(info[0])
                            self.numberEdit.setText(info[1])
                            self.emailEdit.setText(info[2])
                            self.lvlLbl.setText(f'{info[3] // 100} lvl.')
                            self.lvlBar.setValue(info[3] % 100)
                        else:
                            cur.execute(f'''UPDATE users SET about = "{about}",
                                                            number = "{number}",
                                                            email = "{email}"
                                                            WHERE id_name = "{name}"'''
                                        )
                        self.nameEdit.setEnabled(False)
                        self.passwordEdit.setEnabled(False)
                        self.taskDetails.setEnabled(True)
                        self.stats.setEnabled(True)
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Incorrect password!")
                        msg.setWindowTitle("Error password")
                        msg.exec_()
                con.commit()
                con.close()
        except Exception as ex:
            print(ex)

    def runTest(self):
        try:
            con = sqlite3.connect(r'databases\app.db')
            cur = con.cursor()
            self.sessionPage = 1
            self.testFinishBtn.setVisible(False)
            lastClass = self.lastClkClass
            lastProgram = self.lastClkProgram
            tests_correct = [i[0] for i in cur.execute(
                f'''SELECT id FROM tests_class_{lastClass} WHERE item = "{lastProgram}"''').fetchall()]
            self.lastIdTest = random.choice(tests_correct)
            text = cur.execute(
                f'''SELECT "1" FROM tests_questions WHERE item_id = {self.lastIdTest}''').fetchone()[0].replace('\\n', "\n")
            self.questionTestLbl_2.setText(text)
            self.completedTestBar_2.setValue(0)
            self.completedTestLbl_2.setText(
                f'Completed {10 * (self.sessionPage - 1)}%')
            self.completedTestBar_3.setValue(10 * self.points)
            self.completedTestLbl_3.setText(
                f'Correctly {10 * self.points}%')
            self.sessionPage += 1
        except Exception as e:
            self.questionTestLbl_2.setText(
                'Sorry, this test has not been added to the database yet :(\nTry something else')
            self.testABtn_2.setEnabled(False)
            self.testBBtn_2.setEnabled(False)
            self.testCBtn_2.setEnabled(False)
            self.testDBtn_2.setEnabled(False)
            self.testFinishBtn.setVisible(True)
        finally:
            self.taskDetails.setEnabled(False)
            self.stats.setEnabled(False)
            self.profile.setEnabled(False)
            con.close()

    def question_next(self):
        try:
            con = sqlite3.connect(r'databases\app.db')
            cur = con.cursor()
            text = cur.execute(
                f'''SELECT "{self.sessionPage}" FROM tests_questions WHERE item_id = {self.lastIdTest}''').fetchone()[0].replace('\\n', "\n")
            self.questionTestLbl_2.setText(text)
            self.completedTestBar_2.setValue(10 * (self.sessionPage - 1))
            self.completedTestLbl_2.setText(
                f'Completed {10 * (self.sessionPage - 1)}%')

            true_answer = cur.execute(
                f'''SELECT "{self.sessionPage - 1}" FROM tests_answers WHERE item_id = {self.lastIdTest}''').fetchone()[0]
            if self.lastAnswer == true_answer:
                self.points += 1
            self.completedTestBar_3.setValue(10 * self.points)
            self.completedTestLbl_3.setText(
                f'Correctly {10 * self.points}%')
            if self.sessionPage > 10:
                itemHistory = QListWidgetItem(
                    f'{self.dict_programs_mini_versions[self.lastClkProgram]}({self.lastClkClass}): {self.points} p.')
                itemHistory.setToolTip(
                    f'Program: {self.lastClkProgram}\nClass: {self.lastClkClass}\nPoints: {self.points}\nTime: {datetime.datetime.now().strftime("%c")}')
                self.historyList.insertItem(0, itemHistory)
                name = self.nameEdit.text()
                cur.execute(
                    f'''UPDATE users SET points = points + {self.points} WHERE id_name = "{name}"''')
                cur.execute(
                    f'''UPDATE users SET level_points = level_points + {self.points // 2} WHERE id_name = "{name}" ''')
                cur.execute(
                    f'''UPDATE users SET decided_now = decided_now + 1 WHERE id_name = "{name}" ''')
                cur.execute(
                    f'''UPDATE users SET completed = completed + 1 WHERE id_name = "{name}" ''')
                con.commit()
                message = "Good work! You're the best" if self.points >= 7 else "Not bad, there is much to strive for :)" if self.points >= 5 else "It is necessary to tighten the knowledge on this topic:("
                self.questionTestLbl_2.setText(
                    f"According to the results of this test,\nyou scored {self.points} points.\n\n{message}")
                self.points = 0
                self.completedTestBar_3.setValue(0)
                self.completedTestLbl_3.setText(
                    f'Correctly 0%')
                self.completedTestBar_2.setValue(0)
                self.completedTestLbl_2.setText(
                    f'Completed 0%')
                self.testABtn_2.setEnabled(False)
                self.testBBtn_2.setEnabled(False)
                self.testCBtn_2.setEnabled(False)
                self.testDBtn_2.setEnabled(False)
                self.testFinishBtn.setVisible(True)
            self.sessionPage += 1
        except Exception as e:
            print(e)
        finally:
            con.close()

    def selectR(self, selected):
        if selected:
            self.ownVersion = False

    def mainSelectR(self, selected):
        if selected:
            self.ownVersion = True

    def acceptFile(self):
        if self.ownVersion:
            select_program = self.ownVersionEdit.text()
        else:
            select_program = self.selectProgramBox.currentText()
        select_class = self.selectClassBox.currentText()
        select_file = self.lastInsertFile
        try:
            con = sqlite3.connect(r'databases\app.db')
            cur = con.cursor()
            name = self.nameEdit.text()
            id_tests = [i[0] for i in cur.execute(
                f'''SELECT id FROM rec_tests''').fetchall()]
            while True:
                id_correct = random.randint(1, 10000)
                if id_correct not in id_tests:
                    break
            cur.execute(
                f'''INSERT INTO rec_tests (item, id, class, created_by, content) VALUES ("{select_program}", {id_correct}, "{select_class}", "{name}", "{select_file}")''')
            con.commit()
            self.stackedWidget.setCurrentWidget(self.taskPage)
            self.lastInsertFile = ''
            self.acceptBtn.setEnabled(False)
        except Exception as ex:
            print(ex)
        finally:
            con.close()

    def insertFile(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', 'C:\\', '*.txt')
        if fname[0]:
            with open(fname[0], 'r') as file:
                data = file.read()
                self.lastInsertFile = data
                self.acceptBtn.setEnabled(True)

    def testResult(self):
        self.taskDetails.setEnabled(True)
        self.stats.setEnabled(True)
        self.profile.setEnabled(True)
        self.testABtn_2.setEnabled(True)
        self.testBBtn_2.setEnabled(True)
        self.testCBtn_2.setEnabled(True)
        self.testDBtn_2.setEnabled(True)
        self.stackedWidget.setCurrentWidget(self.taskPage)
        self.updateTaskDetails()

    def gotoTaskDetails(self):
        self.stackedWidget.setCurrentWidget(self.taskPage)
        self.updateTaskDetails()

    def gotoStats(self):
        self.stackedWidget.setCurrentWidget(self.statsPage)
        self.updateStats()

    def gotoProfile(self):
        self.stackedWidget.setCurrentWidget(self.profilePage)
        self.updateProfile()

    def updateStats(self):
        try:
            con = sqlite3.connect(r'databases\app.db')
            cur = con.cursor()

            self.ratingList.clear()
            usersRating = cur.execute(
                f'''SELECT id_name, points, iq, completed, level_points FROM users ORDER BY points DESC''').fetchall()
            for index, user in enumerate(usersRating, start=1):
                name = user[0]
                points = user[1]
                iq = user[2]
                completed = user[3]
                lvl = user[4]
                item = QListWidgetItem(f'{index}) {name} - {points} points.')
                item.setToolTip(
                    f'Rating: {index}\nName: {name}\nLevel: {lvl // 100}\nPoints: {points}\nIq(the highest): {iq}\nCompleted tests : {completed}')
                self.ratingList.addItem(item)
            name = self.nameEdit.text()
            statsInfo = cur.execute(
                f'''SELECT points, iq, completed, daily_test FROM users WHERE id_name = "{name}"''').fetchone()
            self.pointsLcd.display(statsInfo[0])
            self.completedLcd.display(statsInfo[2])
            self.iqLcd.display(statsInfo[1])
            self.compTestTodayLbl.setText(f'{statsInfo[3]}/1')
        except Exception as ex:
            print(ex)
        finally:
            con.close()

    def updateProfile(self):
        try:
            con = sqlite3.connect(r'databases\app.db')
            cur = con.cursor()
            name = self.nameEdit.text()
            info = cur.execute(
                f'''SELECT level_points FROM users WHERE id_name = "{name}"''').fetchone()[0]
            self.lvlLbl.setText(f'{info // 100} lvl.')
            self.lvlBar.setValue(info % 100)
        except Exception as ex:
            print(ex)
        finally:
            con.close()

    def updateTaskDetails(self):
        try:
            con = sqlite3.connect(r'databases\app.db')
            cur = con.cursor()
            name = self.nameEdit.text()
            decidedToday = cur.execute(
                f'''SELECT decided_now FROM users WHERE id_name = "{name}"''').fetchone()[0]
            self.comletedTodayLcd.display(decidedToday)
        except Exception as ex:
            print(ex)
        finally:
            con.close()

    def btnAClicked(self):
        self.lastAnswer = 'A'
        self.question_next()

    def btnBClicked(self):
        self.lastAnswer = 'B'
        self.question_next()

    def btnCClicked(self):
        self.lastAnswer = 'C'
        self.question_next()

    def btnDClicked(self):
        self.lastAnswer = 'D'
        self.question_next()

    def lastClkMathematics(self):
        self.lastClkProgram = 'Mathematics'
        self.runTest()

    def lastClkRussianlanguage(self):
        self.lastClkProgram = 'Russian language'
        self.runTest()

    def lastClkSurroundingworld(self):
        self.lastClkProgram = 'Surrounding world'
        self.runTest()

    def lastClkEnglishlanguage(self):
        self.lastClkProgram = 'English language'
        self.runTest()

    def lastClkLiterature(self):
        self.lastClkProgram = 'Literature'
        self.runTest()

    def lastClkLogicalthinking(self):
        self.lastClkProgram = 'Logical thinking'
        self.runTest()

    def lastClkClass1(self):
        self.lastClkClass = 1

    def lastClkClass2(self):
        self.lastClkClass = 2

    def lastClkClass3(self):
        self.lastClkClass = 3

    def lastClkClass4(self):
        self.lastClkClass = 4


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TestingSystem()
    ex.show()
    sys.exit(app.exec())
