#include <Python.h>
#include "mainwindow.h"
#include <QApplication>
#include <QDebug>
int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    Py_SetPythonHome((const wchar_t *)(L"C:/Users/D000016264/AppData/Local/Programs/Python/Python37"));
    Py_Initialize();
    if( !Py_IsInitialized() ){
        qDebug()<<QObject::tr("Py_IsInitialize failed\n");
    }

    MainWindow w;
    w.setWindowTitle("Step2");
    w.show();
    return a.exec();
}
