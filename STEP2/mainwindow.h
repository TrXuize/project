#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_browse_clicked();

    void on_csv_browse_clicked();

    void on_pushButton_clicked();

    void on_browseImg_clicked();

    void on_browseResult_clicked();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
