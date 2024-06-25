#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include "load_map.hpp"
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#include "gui.hpp"
#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>


using namespace std;

void loadProvinceMap(const string& filenameStr, vector<provinceClass>& provincesArray, int& localWidth, int& localHeight){

    const char *filename = filenameStr.c_str();
    int width, height, channels;
    unsigned char *data = stbi_load(filename, &width, &height, &channels, 0);

    localWidth = width;
    localHeight = height;

    unordered_map<string, int> provinceMap;
    for (const auto &prov : provincesArray) {
        provinceMap[prov.hexadecimal] = prov.id;
    }

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            int currentPixel = (i * width + j) * channels;
            unsigned char r = data[currentPixel];
            unsigned char g = data[currentPixel + 1];
            unsigned char b = data[currentPixel + 2];

            int red = r;
            int green = g;
            int blue = b;

            string hexadecimal;
            stringstream redHex; stringstream greenHex; stringstream blueHex;
            redHex << hex << red; greenHex << hex << green; blueHex << hex << blue;
            
            if((redHex.str()).size()==1){hexadecimal+="0";}
            hexadecimal+=redHex.str();
            if((greenHex.str()).size()==1){hexadecimal+="0";}
            hexadecimal+=greenHex.str();
            if((blueHex.str()).size()==1){hexadecimal+="0";}
            hexadecimal+=blueHex.str();

            auto it = provinceMap.find(hexadecimal);
            if (it != provinceMap.end()) {
                provincesArray[it->second].coordinates.insert(make_pair(j,i));
            }
        }
    }


}

scenePixelItem::scenePixelItem(int x, int y, int width, int height, const QColor& color)
    : QGraphicsRectItem(x, y, width, height), originalColor(color) {
    setBrush(QBrush(originalColor));
    setAcceptHoverEvents(true);
    setPen(Qt::NoPen);
}


MainWindow::MainWindow(int& width, int& height, vector<provinceClass>& provincesArray,QWidget *parent)
    : QMainWindow(parent) {
    // Create a central widget to hold the layout
    QWidget *centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);

    // Create a scene with a predefined size
    QGraphicsScene *scene = new QGraphicsScene(0, 0, width, height);

    //for (const auto& prov : provincesArray) {
    //    QString hex = QString::fromStdString(prov.hexadecimal);
    //    auto coordinatesCopy = prov.coordinates;
    //    for (const auto& [key, value] : coordinatesCopy){
    //        scenePixelItem *item = new scenePixelItem(key, value, 1, 1, QColor("#"+hex));
    //        scene->addItem(item);
    //    }
    //}

    string hexadecimal = "FF10A0";
    QString hex = QString::fromStdString(hexadecimal);
    scenePixelItem *item = new scenePixelItem(0, 0, 100, 100, QColor("#"+hex));
    scene->addItem(item);

    // Create a view to display the scene
    QGraphicsView *view = new QGraphicsView(scene);
    view->setRenderHint(QPainter::Antialiasing);
    view->setViewportUpdateMode(QGraphicsView::BoundingRectViewportUpdate);
    view->setDragMode(QGraphicsView::ScrollHandDrag);

    view->setFixedSize(1000, 680);

    // Create a layout to position the view in the top-left corner
    QVBoxLayout *layout = new QVBoxLayout();
    layout->setContentsMargins(0, 0, 0, 0); // No margins
    layout->setSpacing(0); // No spacing between elements
    layout->addWidget(view);
    layout->addStretch(); // Push the view to the top-left corner
    centralWidget->setLayout(layout);
    resize(1920, 1080); // Set main window size
}

MainWindow::~MainWindow() {
    delete scene;
    delete view;
}

void createWindowGUI(int argc, char *argv[], int& width, int& height, vector<provinceClass>& provincesArray){
    QApplication app(argc, argv);


    MainWindow mainWindow(width, height, provincesArray);
    mainWindow.show();


    app.exec();
}
