import cv2 as cv
import numpy as np
from tkinter import ttk
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
    imgCopy = imgRes
    newImg = cvToImg(imgRes)
    imagePanel.configure(image=newImg)
    imagePanel.image = newImg

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

def filtCanny():
    imgCopy = img.copy()
    imgRes = cv.Canny(imgCopy, 200, 550)
    atualizaImagemPanel(imgRes)

def abreArquivo():
    global img, imgCopy
    file_path = askopenfilename(filetypes=[('*jpeg', '*png')]).strip()
    if file_path is not None and file_path != "":
        img = cv.imread(file_path.strip())
        imgCopy = img.copy()
        atualizaImagemPanel(img)
    return

def salvaArquivo():
    img = ImageTk.getimage(imagePanel.image)
    filename = asksaveasfile(mode='wb', defaultextension='.png')
    if filename is None:
        return
    img.save(filename)

def restauraArquivo():
    global imgCopy
    imgCopy = img
    atualizaImagemPanel(img)

def sobrepoeImagem(x_offset, y_offset):
    if stcAtual < 0:
        return
    imgRes = imgCopy.copy()
    imgStc = stckCv[stcAtual].copy()

    y1, y2 = int(y_offset - imgStc.shape[0]/2), int(y_offset + imgStc.shape[0]/2)
    x1, x2 = int(x_offset - imgStc.shape[1]/2), int(x_offset + imgStc.shape[1]/2)

    if y1 < 0: y1 = 0; y2 = imgStc.shape[0]
    if x1 < 0: x1 = 0; x2 = imgStc.shape[1]
    if y2 > imgRes.shape[0]: y2 = imgRes.shape[0]; y1 = imgRes.shape[0] - imgStc.shape[0]
    if x2 > imgRes.shape[1]: x2 = imgRes.shape[1]; x1 = imgRes.shape[1] - imgStc.shape[1]

    alpha_s = imgStc[:, :, 3] / 255.0 if imgStc.shape[2] == 4 else 1.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        imgRes[y1:y2, x1:x2, c] = (alpha_s * imgStc[:, :, c] + alpha_l * imgRes[y1:y2, x1:x2, c])
    
    atualizaImagemPanel(imgRes)

def clicaImagem(event):
    sobrepoeImagem(event.x, event.y)


root = Tk()  # create parent window

topFrame = Frame(root)
topFrame.pack(side=TOP, fill=X)

bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

rightFrame = Frame(root)
rightFrame.pack(side=RIGHT)

mb = Menubutton(topFrame, text="Arquivo", relief=GROOVE)
mb.menu = Menu(mb, tearoff=0)
mb["menu"] = mb.menu
mb.menu.add_checkbutton(label="Abrir", command=abreArquivo)
mb.menu.add_checkbutton(label="Salvar", command=salvaArquivo)
mb.menu.add_checkbutton(label="Restaurar", command=restauraArquivo)
mb.pack(anchor="w")


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
Button(bottomFrame, text="Canny", command=filtCanny).pack(side="left", padx=5)


def btnStickerSelecionado(numStc):
    global stcAtual 
    print(numStc)
    stcAtual = numStc
    for i in range(len(butStck)):
        butStck[i].configure(relief=SUNKEN) if i == numStc else butStck[i].configure(relief=RAISED) 

# stc = cv.imread('circle.png')
stckCv = []; stckImg = []; butStck = []
for i in range(5):
    stckCv.append(cv.imread('alien' + str(i) + '.png'))
    stckImg.append(cvToImg(stckCv[i]))
    butStck.append(Button(rightFrame, image=stckImg[i], command=lambda itemp=i: btnStickerSelecionado(itemp)))
    butStck[i].pack()

img = cv.imread('baboon.png') 
imgCopy = img.copy()
stcAtual = -1


imgtk = cvToImg(imgCopy)
imagePanel = Label(root, image=imgtk, bg="white", relief=SUNKEN)
imagePanel.pack(side="top")
imagePanel.bind("<Button-1>", clicaImagem)

root.mainloop()
