import os
from PyQt5.QtWidgets import (QApplication,QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QLabel,QListWidget, QFileDialog)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from PIL import (Image,ImageFilter)

app = QApplication([])
mw = QWidget()
mw.resize(700,500)

main_hl = QHBoxLayout()

left_vl = QVBoxLayout()
folder_btn = QPushButton(text='Папка')
imgs_lw = QListWidget()
left_vl.addWidget(folder_btn)
left_vl.addWidget(imgs_lw)

right_vl = QVBoxLayout()
image_lb = QLabel(text='Тут будет картинка')

btns_hl = QHBoxLayout()
left_btn = QPushButton(text='Лево')
right_btn = QPushButton(text='Право')
mirror_btn = QPushButton(text='Зеркало')
sharpness_btn = QPushButton(text='Резкость')
bw_btn = QPushButton(text='Ч/Б')
btns_hl.addWidget(left_btn)
btns_hl.addWidget(right_btn)
btns_hl.addWidget(mirror_btn)
btns_hl.addWidget(sharpness_btn)
btns_hl.addWidget(bw_btn)

right_vl.addWidget(image_lb)
right_vl.addLayout(btns_hl)

main_hl.addLayout(left_vl,stretch=20)
main_hl.addLayout(right_vl,stretch=80)

mw.setLayout(main_hl)

workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files: list[str], extensions):
    result = []
    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                result.append(file)
    return result

def showFilenamesList():
    chooseWorkdir()
    extensions = ['.jpg','.jpeg','.png','.gif','.bmp']
    files = os.listdir(workdir)
    files = filter(files,extensions)
    imgs_lw.clear()
    imgs_lw.addItems(files)

class ImageProcessor():
    def __init__(self) -> None:
        self.image = None
        self.filename = None
        self.modify_dir = './Modify'
    
    def loadImage(self,filename) -> None:
        self.filename = filename
        image_path = os.path.join(workdir,filename)
        self.image = Image.open(image_path)

    def showImage(self,path) -> None:
        image_lb.hide()
        pixmap_image = QPixmap(path)
        w,h = image_lb.width(),image_lb.height()
        pixmap_image = pixmap_image.scaled(w,h,
                                           Qt.AspectRatioMode.KeepAspectRatio)
        image_lb.setPixmap(pixmap_image)
        image_lb.show()

    def saveImage(self) -> None:
        path = os.path.join(workdir,self.modify_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)

    def changeImage(self):
        self.saveImage()
        path = os.path.join(workdir,self.modify_dir,self.filename)
        self.showImage(path)

    def modeWBImage(self) -> None:
        self.image = self.image.convert('L')
        self.changeImage()

    def modeMirrorImage(self) -> None:
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.changeImage()

    def modeSharpnessImage(self) -> None:
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.changeImage()

    def modeTransposeImage(self,const):
        self.image = self.image.transpose(const)
        self.changeImage()

folder_btn.clicked.connect(showFilenamesList)
def showChosenImage():
    if imgs_lw.currentRow() >= 0:
        filename = imgs_lw.currentItem().text()
        work_image.loadImage(filename)
        image_path = os.path.join(workdir,work_image.filename)
        work_image.showImage(image_path)

imgs_lw.currentRowChanged.connect(showChosenImage)

work_image = ImageProcessor()
bw_btn.clicked.connect(work_image.modeWBImage)
mirror_btn.clicked.connect(lambda:work_image.modeTransposeImage(Image.FLIP_LEFT_RIGHT))
left_btn.clicked.connect(lambda:work_image.modeTransposeImage(Image.ROTATE_90))
right_btn.clicked.connect(lambda:work_image.modeTransposeImage(Image.ROTATE_270))
sharpness_btn.clicked.connect(work_image.modeSharpnessImage)
mw.show()
app.exec_()
