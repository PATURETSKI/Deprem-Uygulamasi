# Çağırılan Kütüphaneler
import tkinter as tk
from tkinter import ttk
import sqlite3
import requests
from bs4 import BeautifulSoup
import threading
import time
from tkinter import ttk
from tkinter import StringVar
import re
import matplotlib.pyplot as plt
import datetime

# Veritabanı
Veritabanı = "depremler_Ödev1.db"


# Veritabanı Oluşturma fonksiyonu
def veritabani_olustur():
    baglantı = sqlite3.connect(Veritabanı)
    cur = baglantı.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Depremler(id INTEGER PRIMARY KEY AUTOINCREMENT,tarih, enlem, boylam,derinlik,buyukluk,yer,UNIQUE(tarih,enlem,boylam,derinlik,buyukluk,yer))""")
    baglantı.commit()
    baglantı.close()

# Verileri BeautifulSoup ile Kandilli Rasathanesinden veri çekme
def verileri_cekme():
    url = "http://www.koeri.boun.edu.tr/scripts/lst8.asp"
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    pre = soup.find('pre')
    if not pre:
        return
    
    satirlar = pre.text.strip().split('\n')[6:]

    baglantı = sqlite3.connect(Veritabanı)
    cur = baglantı.cursor()

    for satir in satirlar:
        try:
            # Burda liste içindeki sayılar Kandilli Rasathanesinin web sitesindeki işimize yarayan yerlerin nokta atışı kordinatları.
            # Elle tek tek ayarlandı...
            tarih = satir[:20].strip()
            enlem = satir[21:29].strip()
            boylam = satir[32:39].strip()
            derinlik = satir[46:50].strip()
            buyukluk = satir[60:65].strip()
            yer = satir[70:115].strip()

            # Tek satırda önce kontrol edip sonra ekleme kısmı.
            cur.execute("INSERT OR IGNORE INTO Depremler(tarih, enlem, boylam, derinlik, buyukluk, yer)VALUES (?, ?, ?, ?, ?, ?)",(tarih, enlem, boylam, derinlik, buyukluk, yer))
        except Exception as e:
            print("Hata oluştu veriyi çekemiyoruz", e)
       
    baglantı.commit()
    baglantı.close()

# Şehir seçerken kullanacağımız fonksiyon.
# Şehirlerin hepsini görmek istersek Tüm Zamanlar adı altında görebilmemiz için.
# Limit olarak 500 yazmamın sebebi Kandilli Rasathanesi verileri 1 Haftalık max 500 deprem olacak şekilde paylaşıyor.
# Yani 1 haftada tam 500 deprem verisi geldiğinden bütün verileri çekecek.
def Sehirler(sehir):
    baglantı = sqlite3.connect(Veritabanı)
    cur = baglantı.cursor()
    if sehir == "TÜM ZAMANLAR":
        cur.execute("SELECT * FROM Depremler ORDER BY tarih DESC LIMIT 500")
    else:
        cur.execute("SELECT * FROM Depremler WHERE yer LIKE ? ORDER BY tarih DESC LIMIT 500", (f"%{sehir}%",))
    veriler = cur.fetchall()
    baglantı.close()
    return veriler

# Şehir listesi fonksiyonu (Bu fonksiyonu bütün şehirleri bir araya getirip 'TÜM ZAMANLAR' adı altında bütün şehirleri göstersin amacıyla yaptım
def sehir_listesi():
    baglantı = sqlite3.connect(Veritabanı)
    cur = baglantı.cursor()
    cur.execute("SELECT DISTINCT yer FROM Depremler")
    verilerim = cur.fetchall()
    baglantı.close()
    sehir_seti = set()
    for i in verilerim:
        yer = i[0].strip()
        if "(" in yer and ")" in yer:
         match = re.search(r'\((.*?)\)', yer)
         if match:
             sehir = match.group(1).strip().upper()
             sehir_seti.add(sehir)
        elif len(yer.split()) <= 3:
            sehir_seti.add(yer.strip().upper())
    sehirler = sorted(list(sehir_seti))
    return ["TÜM ZAMANLAR"] + sehirler

# Grafik fonksiyonu matplotlib ile çalışıyor.
def Grafik():
    sehir = sehir_var.get()
    if sehir == "":
        return
    veriler = Sehirler(sehir)
    if not veriler:
        return
    tarih_listesi = []
    buyukluk_listesi = []
    for v in veriler:
        try:
            tarih_str = v[1].strip()
            tarih_obj = datetime.datetime.strptime(tarih_str, "%Y.%m.%d %H:%M:%S")
            buyukluk = float(v[5].replace(",", "."))
            tarih_listesi.append(tarih_obj)
            buyukluk_listesi.append(buyukluk)
        except Exception as e:
            print("Grafik verisi hatası:", e)
    plt.figure(figsize=(10, 5))
    plt.plot(tarih_listesi, buyukluk_listesi, marker="o", linestyle="-", color="blue")
    plt.title(f"{sehir} Deprem Büyüklükleri(Son 1 Hafta)")
    plt.xlabel("Tarih(Saatleri görmek için yakınlaştırın)")
    plt.ylabel("Büyüklük (Mw)")
    plt.gcf().autofmt_xdate()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Tkinter arayüzü kısmı
def tkinter_arayuz():
    verileri_cekme()
    # Her 60 saniyede bir otomatik şekilde Kandilli Rasathanesinden verileri çekip veritabanına atan fonksiyon
    # Bu fonksiyon uygulamamın bel kemiği 60 saniyede bir verileri veritabanına yazıyor otomatik
    # Güncelle butonuna basınca da o veriler önümüze geliyor(Güncel veriler)
    def arka_plan_guncelleme():
        while True:
            verileri_cekme()
            time.sleep(60)

    threading.Thread(target=arka_plan_guncelleme, daemon=True).start()
    # Güncelle butonuna basınca veritabanından güncel veriler getirir.(Yukarıda bahsettiğim kısım burası)
    def Guncelle():
        sehir = sehir_var.get()
        veriler = Sehirler(sehir)
        for row in tree.get_children():
            tree.delete(row)
        for v in veriler:
         try:
            buyukluk = float(v[5].replace(",", "."))
            # Depremin büyüklüğü 3 den küçükse Yeşil görünecek
            if buyukluk < 3:
              tag = "yesil"
            # Depremin büyüklüğü 3 den büyük fakat 5 den küçükse Turuncu görünecek
            elif buyukluk < 5:
              tag = "turuncu"
            # Depremin büyüklüğü 5 den büyükse Kırmızı görünecek
            else:
              tag = "kirmizi"
         except:
              tag = ""

         tree.insert("", "end", values=(v[1], v[2], v[3], v[4], v[5], v[6]), tags=(tag,))
    
    # Buradan itibaren pencere kısmına giriş yapıyoruz
    pencere = tk.Tk()
    pencere.title("Anlık Deprem Verisi")
    pencere.geometry("800x400")

    tk.Label(pencere, text="Veriler anlık olarak Kandilli Rasathanesinden gelmektedir.(Son 1 Haftadaki Depremler)").pack()
    tk.Label(pencere, text="Son 1 haftada depremlerin olduğu Şehirler,Ülkeler,Bölgeler:").pack()

    # Şehir_var değişkenini global yapmak zorunda kaldım sürekli hata alıyordum Guncelle fonksiyonu çalışmıyordu yoksa.
    global sehir_var

    sehir_var = StringVar()
    sehir_combobox = ttk.Combobox(pencere, textvariable=sehir_var,state="readonly")
    sehir_combobox['values'] = sehir_listesi()
    sehir_combobox.pack()

    buton_frame = tk.Frame(pencere)
    buton_frame.pack(pady=10)

    ttk.Button(buton_frame, text="Güncelle", command=Guncelle).pack(side="left", padx=7)
    ttk.Button(buton_frame, text="Grafik", command=Grafik).pack(side="left", padx=7)

    tree = ttk.Treeview(pencere, columns=("Tarih", "Enlem", "Boylam", "Derinlik","Büyüklük", "Yer"), show="headings")
    tree.tag_configure("yesil", background="#76f536")      # Yeşil
    tree.tag_configure("turuncu", background="#cf9b18")    # Turuncu
    tree.tag_configure("kirmizi", background="#d41414")    # Kırmızı

    # Kandilli Rasathanesinden verileri düzgün yerleştirebilmek içindeki bölümlerin boyutları(Yanlamasına)
    sutun_genişlikleri = {
        "Tarih": 120,
        "Enlem": 50,
        "Boylam": 50,
        "Derinlik": 50,
        "Büyüklük": 50,
        "Yer": 250,}

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col,width=sutun_genişlikleri[col],anchor="center")
    #Scrollbar ekleme kısmı
    scrollbar_y = ttk.Scrollbar(pencere, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    
    pencere.mainloop()

# Ana akış kısmı
veritabani_olustur()
tkinter_arayuz()