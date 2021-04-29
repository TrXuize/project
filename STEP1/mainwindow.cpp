#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "qmessagebox.h"
#include <math.h>
#include <Python.h>
#include <QDebug>
#include <QApplication>
#include <QWidget>
#include <QLabel>
#include <QFileDialog>
MainWindow::MainWindow(QWidget *parent):
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    Py_Finalize();
    delete ui;
}




void MainWindow::on_pushButton_clicked()
{
   //執行單句Python語句，用於調用模塊的路徑，否則將無法找到相應的調用模塊
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");

    PyObject* pModule = PyImport_ImportModule("QTpic_function");
    if (! pModule){
       qDebug()<<QObject::tr("Can't open python file\n");
    }

    QString pic_path = ui->P_path->text();
    QDir path;

    if(ui->rotate->isChecked()){
        QString save_path = pic_path + "rotate" + "\\";
        QString tLow = ui->low->text();
        QString tHigh = ui->high->text();
        int low = tLow.toInt();
        int high = tHigh.toInt();
        PyObject *args = PyTuple_New(4);
        PyTuple_SetItem(args,0,Py_BuildValue("s",pic_path.toStdString().c_str()));
        PyTuple_SetItem(args,1,Py_BuildValue("s",save_path.toStdString().c_str()));
        PyTuple_SetItem(args,2,Py_BuildValue("i",low));
        PyTuple_SetItem(args,3,Py_BuildValue("i",high));
        path.setCurrent(pic_path);
        path.mkdir("rotate");

        PyObject* pFunHandler = PyObject_GetAttrString(pModule,"rotate");
        if (!pFunHandler){
           qDebug()<<QObject::tr("Get function failed\n");
        }
        PyEval_CallObject(pFunHandler,args);

    }

    if(ui->bright->isChecked()){
        QString save_path = pic_path + "bright" + "\\";
        QString tmin_bright = ui->min_brightness->text();
        QString tmax_bright = ui->max_brightness->text();
        QString tmin_contrast = ui->min_contrast->text();
        QString tmax_contrast = ui->max_contrast->text();
        int min_bright = tmin_bright.toInt();
        int max_bright = tmax_bright.toInt();
        float min_contrast = tmin_contrast.toFloat();
        float max_contrast = tmax_contrast.toFloat();
        PyObject *args = PyTuple_New(6);
        PyTuple_SetItem(args,0,Py_BuildValue("s",pic_path.toStdString().c_str()));
        PyTuple_SetItem(args,1,Py_BuildValue("s",save_path.toStdString().c_str()));
        PyTuple_SetItem(args,2,Py_BuildValue("i",min_bright));
        PyTuple_SetItem(args,3,Py_BuildValue("i",max_bright));
        PyTuple_SetItem(args,4,Py_BuildValue("f",min_contrast));
        PyTuple_SetItem(args,5,Py_BuildValue("f",max_contrast));
        path.setCurrent(pic_path);
        path.mkdir("bright");

        PyObject* pFunHandler = PyObject_GetAttrString(pModule,"bright");
        if (!pFunHandler){
           qDebug()<<QObject::tr("Get function failed\n");
        }
        PyEval_CallObject(pFunHandler,args);
    }

    if(ui->resize->isChecked()){
        QString save_path = pic_path + "resize" + "\\";
        QString tmin_width = ui->min_width->text();
        QString tmax_width = ui->max_width->text();
        QString tmin_height = ui->min_height->text();
        QString tmax_height = ui->max_height->text();

        int min_width = tmin_width.toInt();
        int max_width = tmax_width.toInt();
        int min_height = tmin_height.toInt();
        int max_height = tmax_height.toInt();

        PyObject *args = PyTuple_New(6);
        PyTuple_SetItem(args,0,Py_BuildValue("s",pic_path.toStdString().c_str()));
        PyTuple_SetItem(args,1,Py_BuildValue("s",save_path.toStdString().c_str()));
        PyTuple_SetItem(args,2,Py_BuildValue("i",min_width));
        PyTuple_SetItem(args,3,Py_BuildValue("i",max_width));
        PyTuple_SetItem(args,4,Py_BuildValue("i",min_height));
        PyTuple_SetItem(args,5,Py_BuildValue("i",max_height));

        path.setCurrent(pic_path);
        path.mkdir("resize");

        PyObject* pFunHandler = PyObject_GetAttrString(pModule,"resize");
        if (!pFunHandler){
           qDebug()<<QObject::tr("Get function failed\n");
        }
        PyEval_CallObject(pFunHandler,args);
    }

    if(ui->shift->isChecked()){
        QString save_path = pic_path + "shift" + "\\";
        QString tmin_shift_right = ui->min_shift_right->text();
        QString tmax_shift_right = ui->max_shift_right->text();
        QString tmin_shift_down = ui->min_shift_down->text();
        QString tmax_shift_down = ui->max_shift_down->text();
        int min_shift_right = tmin_shift_right.toInt();
        int max_shift_right = tmax_shift_right.toInt();
        int min_shift_down = tmin_shift_down.toInt();
        int max_shift_down = tmax_shift_down.toInt();

        PyObject *args = PyTuple_New(6);
        PyTuple_SetItem(args,0,Py_BuildValue("s",pic_path.toStdString().c_str()));
        PyTuple_SetItem(args,1,Py_BuildValue("s",save_path.toStdString().c_str()));
        PyTuple_SetItem(args,2,Py_BuildValue("i",min_shift_right));
        PyTuple_SetItem(args,3,Py_BuildValue("i",max_shift_right));
        PyTuple_SetItem(args,4,Py_BuildValue("i",min_shift_down));
        PyTuple_SetItem(args,5,Py_BuildValue("i",max_shift_down));

        path.setCurrent(pic_path);
        path.mkdir("shift");

        PyObject* pFunHandler = PyObject_GetAttrString(pModule,"shift");
        if (!pFunHandler){
           qDebug()<<QObject::tr("Get function failed\n");
        }
        PyEval_CallObject(pFunHandler,args);
    }

    if(ui->flip->isChecked()){
        QString save_path = pic_path + "flip" + "\\";
        QString tmin_flipValue = ui->min_flipValue->text();
        QString tmax_flipValue = ui->max_flipValue->text();
        int min_flipValue = tmin_flipValue.toInt();
        int max_flipValue = tmax_flipValue.toInt();

        PyObject *args = PyTuple_New(4);
        PyTuple_SetItem(args,0,Py_BuildValue("s",pic_path.toStdString().c_str()));
        PyTuple_SetItem(args,1,Py_BuildValue("s",save_path.toStdString().c_str()));
        PyTuple_SetItem(args,2,Py_BuildValue("i",min_flipValue));
        PyTuple_SetItem(args,3,Py_BuildValue("i",max_flipValue));

        path.setCurrent(pic_path);
        path.mkdir("flip");

        PyObject* pFunHandler = PyObject_GetAttrString(pModule,"flip");
        if (!pFunHandler){
           qDebug()<<QObject::tr("Get function failed\n");
        }
        PyEval_CallObject(pFunHandler,args);
    }

    if(ui->hue->isChecked()){
        QString save_path = pic_path + "hue" + "\\";

        QString tpic_count = ui->pic_count->text();
        QString thue_low = ui->hue_low->text();
        QString thue_high = ui->hue_high->text();

        int pic_count = tpic_count.toInt();
        float hue_low = thue_low.toFloat();
        float hue_high = thue_high.toFloat();

        PyObject *args = PyTuple_New(5);
        PyTuple_SetItem(args,0,Py_BuildValue("s",pic_path.toStdString().c_str()));
        PyTuple_SetItem(args,1,Py_BuildValue("s",save_path.toStdString().c_str()));
        PyTuple_SetItem(args,2,Py_BuildValue("i",pic_count));
        PyTuple_SetItem(args,3,Py_BuildValue("f",hue_low));
        PyTuple_SetItem(args,4,Py_BuildValue("f",hue_high));

        path.setCurrent(pic_path);
        path.mkdir("hue");

        PyObject* pFunHandler = PyObject_GetAttrString(pModule,"hue");
        if (!pFunHandler){
           qDebug()<<QObject::tr("Get function failed\n");
        }
        PyEval_CallObject(pFunHandler,args);
    }
}

void MainWindow::on_browse_clicked()
{
    QFileDialog myFileDialog (this);

    QString fileName = myFileDialog.getExistingDirectory (this, tr ("Select Folder"), QDir::currentPath ());
    fileName = QDir::toNativeSeparators((fileName));

    fileName += "\\";
    if(fileName != NULL) {
        ui->P_path->setText(fileName);
    }
}

void MainWindow::on_browseImg_clicked()
{

    QFileDialog myFileDialog (this);

    QString filename = myFileDialog.getOpenFileName(this,"Select pic","/home","image(*.jpg *.png)");
    filename = QDir::toNativeSeparators((filename));

    QPixmap pix(filename);
    QPixmap dest=pix.scaled(ui->Img->size(),Qt::KeepAspectRatio);
    ui->Img->setPixmap(dest);
}

void MainWindow::on_browseResult_clicked()
{
    QFileDialog myFileDialog (this);

    QString filename = myFileDialog.getOpenFileName(this,"Select pic","/home","image(*.jpg *.png)");
    filename = QDir::toNativeSeparators((filename));


    QPixmap pix(filename);
    QPixmap dest=pix.scaled(ui->resultImg->size(),Qt::KeepAspectRatio);
    ui->resultImg->setPixmap(dest);
}
