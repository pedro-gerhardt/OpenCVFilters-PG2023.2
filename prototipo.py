import cv2 as cv
import numpy as np
from tkinter import ttk
from tkinter import *
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

def cvToImg(cvImg):
    color_coverted = cv.cvtColor(cvImg, cv.COLOR_BGR2RGB) 
    pil_image = Image.fromarray(color_coverted) 
    imgtk = ImageTk.PhotoImage(image=pil_image) 
    return imgtk

def atualizaImagemPanel(imgRes):
    global img, imgCopy, filterStacking
    imgCopy = imgRes

    if filterStacking == True:
        img = imgRes

    newImg = cvToImg(imgCopy)
    imagePanel.configure(image=newImg)
    imagePanel.image = newImg
    imagePanel.update()

def atualizaFiltro(imgRes):
    global imgCopy
    imgCopy = imgRes
    for sticker in stickers_pos:
        imgCopy = sobrepoeImagem(sticker[0], sticker[1], sticker[2])
    atualizaImagemPanel(imgCopy)

def filtVerm():
    global filtroAtivo
    filtroAtivo = 1
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
    atualizaFiltro(imgRes)

def filtPond():
    global filtroAtivo
    filtroAtivo = 2
    imgCopy = img.copy()
    imgD2 = np.zeros((imgCopy.shape[0], imgCopy.shape[1]), np.uint8)

    for i in range(imgCopy.shape[0]): #percorre linhas
        for j in range(imgCopy.shape[1]): #percorre colunas
            mediaPond = imgCopy.item(i,j,0) * 0.07 + imgCopy.item(i,j,1) * 0.71 + imgCopy.item(i,j,2) * 0.21
            imgD2[i,j] = int(mediaPond)

    atualizaFiltro(imgD2)

def filtCol():
    global filtroAtivo, corModificadora
    imgCopy = img.copy()
    imgRes = img.copy()

    if filtroAtivo != 3:
        color_code = colorchooser.askcolor(title ="Color Picker")[0]
        corModificadora = list(color_code)
    filtroAtivo = 3
    
    for i in range(imgCopy.shape[0]): #percorre linhas
        for j in range(imgCopy.shape[1]): #percorre colunas
            B = imgCopy.item(i,j,0) | corModificadora[0]
            G = imgCopy.item(i,j,1) | corModificadora[1]
            R = imgCopy.item(i,j,2) | corModificadora[2]
            imgRes.itemset((i,j,0),B) # canal B
            imgRes.itemset((i,j,1),G) # canal G
            imgRes.itemset((i,j,2),R) # canal R

    atualizaFiltro(imgRes)

def filtInv():
    global filtroAtivo
    filtroAtivo = 4
    imgCopy = img.copy()
    imgRes = img.copy()
    
    for i in range(imgCopy.shape[0]): #percorre linhas
        for j in range(imgCopy.shape[1]): #percorre colunas
            imgRes.itemset((i,j,0),imgCopy.item(i,j,0)^255) # canal B
            imgRes.itemset((i,j,1),imgCopy.item(i,j,1)^255) # canal G
            imgRes.itemset((i,j,2),imgCopy.item(i,j,2)^255) # canal R

    atualizaFiltro(imgRes)

def filtBin():
    global filtroAtivo
    filtroAtivo = 5
    imgCopy = img.copy()
    imgGray = cv.cvtColor(imgCopy, cv.COLOR_BGR2GRAY)
    imgRes = imgGray.copy()
    k = spinVar.get()
    for i in range(imgGray.shape[0]): #percorre linhas
        for j in range(imgGray.shape[1]): #percorre colunas
            if imgGray.item(i,j) < k:
                imgRes.itemset((i,j),0)
            else:
                imgRes.itemset((i,j),255)

    atualizaFiltro(imgRes)

def filtVig():
    global filtroAtivo
    filtroAtivo = 6
    imgCopy = img.copy()
    imgRes = img.copy()
    rows, cols = imgCopy.shape[:2]
    X_resultant_kernel = cv.getGaussianKernel(cols, 150)
    Y_resultant_kernel = cv.getGaussianKernel(rows, 150)
    resultant_kernel = Y_resultant_kernel * X_resultant_kernel.T
    mask = 255 * resultant_kernel / np.linalg.norm(resultant_kernel)   
    for i in range(3):
        imgRes[:,:,i] = imgRes[:,:,i] * mask
    atualizaFiltro(imgRes)

def filtLUV():
    global filtroAtivo
    filtroAtivo = 7
    imgCopy = img.copy()
    grayImg = cv.cvtColor(imgCopy, cv.COLOR_Luv2RGB) 
    atualizaFiltro(grayImg)

def filtPix():
    global filtroAtivo
    filtroAtivo = 8
    imgCopy = imgRes = img.copy()
    height, width = imgCopy.shape[:2]
    temp = cv.resize(imgCopy, (16, 16))
    imgRes = cv.resize(temp, (height, width), interpolation=cv.INTER_NEAREST)
    atualizaFiltro(imgRes)

def filtCanny():
    global filtroAtivo
    filtroAtivo = 9
    imgCopy = img.copy()
    imgRes = cv.Canny(imgCopy, 200, 550)
    atualizaFiltro(imgRes)

def filtBlur(intBlur):
    global filtroAtivo, valorIntBlur
    filtroAtivo = 10
    valorIntBlur = intBlur
    if intBlur == 0: return
    imgCopy = imgRes = img.copy()
    imgRes = cv.blur(imgCopy, (int(intBlur), int(intBlur)))
    atualizaFiltro(imgRes)

def abreArquivo():
    global img, imgCopy, webcamAtivo
    webcamAtivo = False
    file_path = askopenfilename(filetypes=[('*jpeg', '*png')]).strip()
    if file_path is not None and file_path != "":
        img = cv.imread(file_path.strip())
        if img.shape[0] < 100 or img.shape[1] < 100:
            showinfo("Aviso", "A imagem carregada precisa ter largura e altura igual ou superior a 100 pixels."); return
        imgCopy = img.copy()
        habilitaBotoesEStickers()
        atualizaImagemPanel(img)
    return

def salvaArquivo():
    img = ImageTk.getimage(imagePanel.image)
    filename = asksaveasfile(mode='wb', defaultextension='.png')
    if filename is None:
        return
    img.save(filename)

def abreWebcam():
    global webcamAtivo, img, filtroAtivo, valorIntBlur
    webcamAtivo = True
    filtroAtivo = 0
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        print("Não foi possível abrir a webcam")
        exit(0)
    habilitaBotoesEStickers()
    while webcamAtivo:
        ret, img = capture.read()
        if img is None:
            print("Frame com problemas")
            break
        if not ret:
            print("Falhou para obter o frame")
            break
        validaFiltrosAtivos()
        if cv.waitKey(1) & 0xFF == ord('q'):
            webcamAtivo = False
            capture.release()
            break

def limpawebCam():
    global filtroAtivo, img, stickers_pos
    filtroAtivo = 0
    stickers_pos = []
    atualizaImagemPanel(img)

def validaFiltrosAtivos():
    global img, filtroAtivo
    match filtroAtivo:
        case 0:
            atualizaFiltro(img)
        case 1:
            filtVerm()
        case 2:
            filtPond()
        case 3:
            filtCol()
        case 4:
            filtInv()
        case 5:
            filtBin()
        case 6:
            filtVig()
        case 7:
            filtLUV()
        case 8:
            filtPix()
        case 9:
            filtCanny()
        case 10:
            filtBlur(valorIntBlur)

def restauraArquivo():
    global imgCopy, stickers_pos
    imgCopy = img
    stickers_pos = []
    atualizaImagemPanel(img)

def sobrepoeImagem(x_offset, y_offset, stcAtualParam = None):
    global imgCopy
    stcAtualParam = stcAtualParam or stcAtual

    if stcAtualParam < 0: return

    imgRes = imgCopy.copy()
    imgStc = stckCv[stcAtualParam].copy()

    y1, y2 = int(y_offset - imgStc.shape[0]/2), int(y_offset + imgStc.shape[0]/2)
    x1, x2 = int(x_offset - imgStc.shape[1]/2), int(x_offset + imgStc.shape[1]/2)

    if y1 < 0: y1 = 0; y2 = imgStc.shape[0]
    if x1 < 0: x1 = 0; x2 = imgStc.shape[1]
    if y2 > imgRes.shape[0]: y2 = imgRes.shape[0]; y1 = imgRes.shape[0] - imgStc.shape[0]
    if x2 > imgRes.shape[1]: x2 = imgRes.shape[1]; x1 = imgRes.shape[1] - imgStc.shape[1]

    alpha_s = imgStc[:, :, 3] / 255.0 if imgStc.shape[2] == 4 else 1.0
    alpha_l = 1.0 - alpha_s

    # se a img for colorida
    if len(imgRes.shape) > 2:
        for c in range(0, 3):
            imgRes[y1:y2, x1:x2, c] = (alpha_s * imgStc[:, :, c] + alpha_l * imgRes[y1:y2, x1:x2, c])
    else:
        gray = cv.cvtColor(imgStc, cv.COLOR_BGR2GRAY)
        imgRes[y1:y2, x1:x2] = (alpha_s * gray[:, :] + alpha_l * imgRes[y1:y2, x1:x2])

    return imgRes

def clicaImagem(event):
    if stcAtual == -1: return
    global stickers_pos
    stickers_pos.append((event.x, event.y, stcAtual))
    imgRes = sobrepoeImagem(event.x, event.y)
    atualizaImagemPanel(imgRes)

def habilitaBotoesEStickers():
    btnVerm["state"] = NORMAL
    btnPond["state"] = NORMAL
    btnColPic["state"] = NORMAL
    btnInv["state"] = NORMAL
    spBin["state"] = NORMAL
    btnVig["state"] = NORMAL
    btnLuv["state"] = NORMAL
    btnPix["state"] = NORMAL
    btnCan["state"] = NORMAL
    btnBlu["state"] = NORMAL
    for s in butStck:
        s["state"] = NORMAL

def toggle():
    global filterStacking

    if toggle_btn.config('relief')[-1] == 'sunken':
        toggle_btn.config(relief="raised")
        filterStacking = False
    else:
        toggle_btn.config(relief="sunken")
        filterStacking = True

stickers_pos = []
root = Tk()  # create parent window

topFrame = Frame(root)
topFrame.pack(side=TOP, fill=X)

bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

rightFrame = Frame(root)
rightFrame.pack(side=RIGHT)

arquivo = Menubutton(topFrame, text="Arquivo", relief=GROOVE)
arquivo.menu = Menu(arquivo, tearoff=0)
arquivo["menu"] = arquivo.menu
arquivo.menu.add_command(label="Abrir", command=abreArquivo)
arquivo.menu.add_command(label="Salvar", command=salvaArquivo)
arquivo.menu.add_command(label="Restaurar", command=restauraArquivo)
arquivo.grid(row=0, column=0)

video = Menubutton(topFrame, text="Video", relief=GROOVE)
video.menu = Menu(video, tearoff=0)
video["menu"] = video.menu
video.menu.add_command(label="Webcam", command=abreWebcam)
video.menu.add_command(label="Limpar Filtros", command=limpawebCam)
video.grid(row=0, column=1)

btnVerm = Button(bottomFrame, text="Verm", command=filtVerm, state=DISABLED)
btnVerm.pack(side="left", padx=5)

btnPond = Button(bottomFrame, text="Pond", command=filtPond, state=DISABLED)
btnPond.pack(side="left", padx=5)

btnColPic = Button(bottomFrame, text="Col Pic", command=filtCol, state=DISABLED)
btnColPic.pack(side="left", padx=5)

btnInv = Button(bottomFrame, text="Inv", command=filtInv, state=DISABLED)
btnInv.pack(side="left", padx=5)

Label(bottomFrame, text="Bin").pack(side="left")
spinVar = IntVar()
spBin = Spinbox(bottomFrame, from_=0, to=255, command=filtBin, textvariable=spinVar, width=5, state=DISABLED)
spBin.pack(side="left", padx=5)

btnVig = Button(bottomFrame, text="Vig", command=filtVig, state=DISABLED)
btnVig.pack(side="left", padx=5)

btnLuv = Button(bottomFrame, text="LUV", command=filtLUV, state=DISABLED)
btnLuv.pack(side="left", padx=5)

btnPix = Button(bottomFrame, text="Pix", command=filtPix, state=DISABLED)
btnPix.pack(side="left", padx=5)

btnCan = Button(bottomFrame, text="Canny", command=filtCanny, state=DISABLED)
btnCan.pack(side="left", padx=5)

Label(bottomFrame, text="Blur").pack(side="left")
btnBlu = Scale(bottomFrame, from_=1, to=100, command=filtBlur, state=DISABLED)
btnBlu.pack(side="left")

global filterStacking
filterStacking = False
toggle_btn = Button(text="Filter Stacking", width=12, relief="raised", command=toggle)
toggle_btn.pack(side="left", padx=5)

def btnStickerSelecionado(numStc):
    global stcAtual 
    stcAtual = numStc
    for i in range(len(butStck)):
        butStck[i].configure(relief=SUNKEN) if i == numStc else butStck[i].configure(relief=RAISED) 

stcAtual = -1
stckCv = []; stckImg = []; butStck = []
for i in range(5):
    stckCv.append(cv.imread('sticker' + str(i) + '.png', cv.IMREAD_UNCHANGED))
    stckImg.append(cvToImg(stckCv[i]))
    butStck.append(Button(rightFrame, image=stckImg[i], state=DISABLED, command=lambda itemp=i: btnStickerSelecionado(itemp)))
    butStck[i].pack()

imagePanel = Label(root, relief="sunken", image=PhotoImage())
imagePanel.pack(side="top")
imagePanel.bind("<Button-1>", clicaImagem)

root.mainloop()
