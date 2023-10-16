import sys
from MainWindow import MainWidget
from PySide2.QtWidgets import QApplication

if __name__=="__main__":
    app = QApplication(sys.argv)
    main_window = MainWidget()
    main_window.show()
    sys.exit(app.exec_())