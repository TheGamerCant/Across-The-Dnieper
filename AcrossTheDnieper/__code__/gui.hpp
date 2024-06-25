#ifndef GUI_HPP
#define GUI_HPP

#include "load_map.hpp"
#include <string>

#include <QMainWindow>
#include <QGraphicsScene>
#include <QGraphicsItem>
#include <QGraphicsView>
#include <QGraphicsRectItem>
#include <QBrush>
#include <QGraphicsSceneHoverEvent>
#include <Qtcore>
#include <QPainter>
#include <QtGui>

using namespace std;

void loadProvinceMap(const string& filenameStr, vector<provinceClass>& provincesArray, int& localWidth, int& height);
void createWindowGUI(int argc, char *argv[], int& width, int& height, vector<provinceClass>& provincesArray);

class scenePixelItem: public QGraphicsRectItem {
public:
    scenePixelItem(int x, int y, int width, int height, const QColor& color);
protected:
    void hoverEnterEvent(QGraphicsSceneHoverEvent *event) override {
        Q_UNUSED(event);
        setBrush(QBrush(Qt::yellow)); // Change color on hover
    }

    void hoverLeaveEvent(QGraphicsSceneHoverEvent *event) override {
        Q_UNUSED(event);
        setBrush(QBrush(originalColor)); // Restore original color
    }
private:
    QColor originalColor;
};


class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    MainWindow(int& width, int& height, vector<provinceClass>& provincesArray, QWidget *parent = nullptr);
    ~MainWindow();

private:
    QGraphicsScene *scene;
    QGraphicsView *view;
};
#endif // GUI_HPP
