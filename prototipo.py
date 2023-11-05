import cv2 as cv
import numpy as np
from tkinter import *
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfile
from PIL import Image, ImageTk


def cvToImg(cvImg):
    color_coverted = cv.cvtColor(cvImg, cv.COLOR_BGR2RGB) 
    pil_image = Image.fromarray(color_coverted) 
    imgtk = ImageTk.PhotoImage(image=pil_image) 
    return imgtk

def atualizaImagemPanel(imgRes):
    global imgCopy
    newImg = cvToImg(imgRes)
    imagePanel.configure(image=newImg)
    imagePanel.image = newImg
    imgCopy = newImg

def filtVerm():
    imgCopy = img.copy()
    imgRes = img.copy()
    corModificadora = [0, 0, 255]
    
    for i in range(imgCopy.shape[0]): #percorre linhas
        for j in range(imgCopy.shape[1]): #percorre colunas
            B = imgCopy.item(i,j,0) | corModificadora[0]
            G = imgCopy.item(i,j,1) | corModificadora[1]
            R = imgCopy.item(i,j,2) | corModificadora[2]
            imgRes.itemset((i,j,0),B) # canal B
            imgRes.itemset((i,j,1),G) # canal G
            imgRes.itemset((i,j,2),R) # canal R

    # grayImg = cv.cvtColor(imgRes, cv.COLOR_Luv2RGB) 
    atualizaImagemPanel(imgRes)

def filtPond():
    imgCopy = img.copy()
    imgRes = img.copy()
    
    for i in range(imgCopy.shape[0]): #percorre linhas
        for j in range(imgCopy.shape[1]): #percorre colunas
            mediaPond = imgCopy.item(i,j,0) * 0.07 + imgCopy.item(i,j,1) * 0.71 + imgCopy.item(i,j,2) * 0.21
            imgRes.itemset((i,j,0),mediaPond) # canal B
            imgRes.itemset((i,j,1),mediaPond) # canal G
            imgRes.itemset((i,j,2),mediaPond) # canal R

    atualizaImagemPanel(imgRes)

def filtCol():
    imgCopy = img.copy()
    imgRes = img.copy()
    
    color_code = colorchooser.askcolor(title ="Color Picker")[0]
    corModificadora = list(color_code)
    
    for i in range(imgCopy.shape[0]): #percorre linhas
        for j in range(imgCopy.shape[1]): #percorre colunas
            B = imgCopy.item(i,j,0) | corModificadora[0]
            G = imgCopy.item(i,j,1) | corModificadora[1]
            R = imgCopy.item(i,j,2) | corModificadora[2]
            imgRes.itemset((i,j,0),B) # canal B
            imgRes.itemset((i,j,1),G) # canal G
            imgRes.itemset((i,j,2),R) # canal R

    atualizaImagemPanel(imgRes)

def filtInv():
    imgCopy = img.copy()
    imgRes = img.copy()
    
    for i in range(imgCopy.shape[0]): #percorre linhas
        for j in range(imgCopy.shape[1]): #percorre colunas
            imgRes.itemset((i,j,0),imgCopy.item(i,j,0)^255) # canal B
            imgRes.itemset((i,j,1),imgCopy.item(i,j,1)^255) # canal G
            imgRes.itemset((i,j,2),imgCopy.item(i,j,2)^255) # canal R

    atualizaImagemPanel(imgRes)

def filtBin():
    imgCopy = img.copy()
    imgGray = cv.cvtColor(imgCopy, cv.COLOR_BGR2GRAY)
    imgRes = imgGray.copy()
    k = spinVar.get()
    print(k)
    for i in range(imgGray.shape[0]): #percorre linhas
        for j in range(imgGray.shape[1]): #percorre colunas
            if imgGray.item(i,j) < k:
                imgRes.itemset((i,j),0)
            else:
                imgRes.itemset((i,j),255)

    atualizaImagemPanel(imgRes)

def filtVig():
    imgCopy = img.copy()
    imgRes = img.copy()
    rows, cols = imgCopy.shape[:2]
    X_resultant_kernel = cv.getGaussianKernel(cols, 150)
    Y_resultant_kernel = cv.getGaussianKernel(rows, 150)
    resultant_kernel = Y_resultant_kernel * X_resultant_kernel.T
    mask = 255 * resultant_kernel / np.linalg.norm(resultant_kernel)   
    for i in range(3):
        imgRes[:,:,i] = imgRes[:,:,i] * mask
    atualizaImagemPanel(imgRes)

def filtLUV():
    imgCopy = img.copy()
    grayImg = cv.cvtColor(imgCopy, cv.COLOR_Luv2RGB) 
    newImg = cvToImg(grayImg)
    imagePanel.configure(image=newImg)
    imagePanel.image = newImg

def filtPix():
    imgCopy = imgRes = img.copy()
    height, width = imgCopy.shape[:2]
    temp = cv.resize(imgCopy, (16, 16))
    imgRes = cv.resize(temp, (height, width), interpolation=cv.INTER_NEAREST)
    atualizaImagemPanel(imgRes)

def abrirArquivo():
    global img, imgCopy
    file_path = askopenfilename(filetypes=[('*jpeg', '*png')])
    if file_path is not None:
        img = cv.imread(file_path)
        imgCopy = img.copy()
        atualizaImagemPanel(img)
    return

def salvarArquivo():
    img = ImageTk.getimage(imagePanel.image)
    filename = asksaveasfile(mode='wb', defaultextension='.png')
    if filename is None:
        return
    img.save(filename)
        
root = Tk()  # create parent window

topFrame = Frame(root)
topFrame.pack(side=TOP, fill=X)

frame = Frame(root)
frame.pack()

bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

mb = Menubutton(topFrame, text="Arquivo", relief=GROOVE)
mb.menu = Menu(mb, tearoff=0)
mb["menu"] = mb.menu
mb.menu.add_checkbutton(label="Abrir", command=abrirArquivo)
mb.menu.add_checkbutton(label="Salvar", command=salvarArquivo)
mb.pack(anchor="w")


# Button(bottomFrame, text="Gray", command=filtro1).pack(side="left", padx=5)
# Button(bottomFrame, text="LUV", command=filtro2).pack(side="left", padx=5)
Button(bottomFrame, text="Verm", command=filtVerm).pack(side="left", padx=5)
Button(bottomFrame, text="Pond", command=filtPond).pack(side="left", padx=5)
Button(bottomFrame, text="Col Pic", command=filtCol).pack(side="left", padx=5)
Button(bottomFrame, text="Inv", command=filtInv).pack(side="left", padx=5)
Label(bottomFrame, text="Bin").pack(side="left")
spinVar = IntVar()
spin = Spinbox(bottomFrame, from_=0, to=255, command=filtBin, textvariable=spinVar, width=5).pack(side="left", padx=5)
Button(bottomFrame, text="Vig", command=filtVig).pack(side="left", padx=5)
Button(bottomFrame, text="LUV", command=filtLUV).pack(side="left", padx=5)
Button(bottomFrame, text="Pix", command=filtPix).pack(side="left", padx=5)

img = cv.imread('baboon.png') #original
imgCopy = img.copy()

imgtk = cvToImg(imgCopy)
imagePanel = Label(root, image=imgtk, bg="white", relief=SUNKEN)
imagePanel.pack(side="top")

root.mainloop()