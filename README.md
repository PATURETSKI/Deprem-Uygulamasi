# 🌍 Deprem Takip Uygulaması

Python kullanılarak geliştirilmiş, **Kandilli Rasathanesi'nden güncel deprem verilerini alan, SQLite veritabanında saklayan ve Tkinter arayüzü üzerinden görüntüleyen** masaüstü deprem takip uygulamasıdır.

Uygulama, verileri belirli aralıklarla otomatik olarak günceller. Kullanıcı şehir/bölge seçerek son depremleri görüntüleyebilir ve seçilen bölgeye ait deprem büyüklüklerini grafik üzerinde inceleyebilir.

---

## 📌 Projenin Amacı

Bu projenin amacı Python kullanarak;

* Web üzerinden veri çekme
* Web scraping
* SQLite veritabanı kullanımı
* Tkinter ile masaüstü arayüz geliştirme
* Thread kullanarak arka planda işlem yürütme
* Matplotlib ile veri görselleştirme

gibi konuları bir arada kullanarak gerçek zamanlıya yakın çalışan basit bir deprem takip sistemi geliştirmektir.

---

## 🚀 Özellikler

### 📡 Otomatik Deprem Verisi Güncelleme

Uygulama Kandilli Rasathanesi'nden deprem verilerini çeker.

Veriler uygulama çalıştığı sürece **60 saniyede bir otomatik olarak güncellenir** ve SQLite veritabanına kaydedilir.

Aynı deprem verisinin tekrar eklenmesini önlemek için SQLite tarafında `UNIQUE` kısıtlaması ve `INSERT OR IGNORE` kullanılmıştır.

### 🗄️ SQLite Veritabanı

Deprem verileri aşağıdaki bilgilerle birlikte SQLite veritabanında saklanır:

* Tarih
* Enlem
* Boylam
* Derinlik
* Büyüklük
* Yer

Veritabanı uygulama tarafından otomatik olarak oluşturulur.

### 🖥️ Grafiksel Kullanıcı Arayüzü

Arayüz **Tkinter** kullanılarak geliştirilmiştir.

Kullanıcı:

1. Bölge/şehir seçebilir.
2. Güncel verileri görüntüleyebilir.
3. Deprem büyüklüklerini renklerle ayırt edebilir.
4. Seçilen bölge için deprem büyüklüğü grafiğini açabilir.

### 🎨 Deprem Büyüklüğüne Göre Renklendirme

Tabloda depremler büyüklüklerine göre renklendirilir:

| Büyüklük    | Renk       |
| ----------- | ---------- |
| `< 3.0`     | 🟢 Yeşil   |
| `3.0 - 4.9` | 🟠 Turuncu |
| `>= 5.0`    | 🔴 Kırmızı |

### 📊 Deprem Grafiği

`Grafik` butonuna basıldığında seçilen şehir/bölgedeki son depremlerin büyüklükleri **Matplotlib** kullanılarak grafik halinde gösterilir.

---

## 🛠️ Kullanılan Teknolojiler

* **Python**
* **Tkinter** — Grafiksel kullanıcı arayüzü
* **SQLite3** — Veritabanı
* **Requests** — Web üzerinden HTTP isteği gönderme
* **BeautifulSoup4** — Web scraping
* **Threading** — Arka planda otomatik veri güncelleme
* **Matplotlib** — Grafik oluşturma
* **Datetime** — Tarih ve saat işlemleri
* **Regular Expressions (re)** — Bölge/şehir bilgilerinin ayrıştırılması

---

## 📂 Projenin Çalışma Mantığı

Uygulamanın genel çalışma akışı:

```text
Kandilli Rasathanesi
        │
        ▼
   HTTP Request
        │
        ▼
   BeautifulSoup
        │
        ▼
 Deprem Verilerinin
     Ayrıştırılması
        │
        ▼
 SQLite Veritabanı
        │
        ├───────────────┐
        ▼               ▼
   Tkinter           Matplotlib
   Arayüzü             Grafik
        │
        ▼
 Kullanıcıya
 Deprem Verileri
```

---

## ⚙️ Kurulum

### 1. Python

Bilgisayarınızda Python'un kurulu olması gerekir.

Python sürümünüzü kontrol etmek için:

```bash
python --version
```

---

### 2. Projeyi Klonlayın

```bash
git clone https://github.com/KULLANICI_ADIN/DEPO_ADI.git
```

Ardından proje klasörüne girin:

```bash
cd DEPO_ADI
```

---

### 3. Gerekli Kütüphaneleri Yükleyin

Terminal/CMD üzerinde:

```bash
pip install requests beautifulsoup4 matplotlib
```

`tkinter` ve `sqlite3` Python ile birlikte geldiği için ayrıca kurulmaları gerekmez.

> Linux sistemlerde Tkinter bazı dağıtımlarda ayrıca kurulmak zorunda olabilir.

---

## ▶️ Uygulamayı Çalıştırma

Proje klasöründe:

```bash
python main.py
```

uygulamasını çalıştırın.

Uygulama açıldığında Kandilli Rasathanesi'nden veriler alınır ve SQLite veritabanına kaydedilir.

Daha sonra şehir/bölge seçerek deprem verilerini görüntüleyebilirsiniz.

---

## 🖥️ Kullanım

Uygulama açıldıktan sonra:

### 1. Şehir/Bölge Seçimi

Açılır menüden görüntülemek istediğiniz şehir veya bölgeyi seçin.

`TÜM ZAMANLAR` seçeneği ile veritabanındaki son 500 deprem görüntülenebilir.

### 2. Güncelle

**Güncelle** butonu seçilen şehir/bölge için veritabanındaki güncel verileri tabloya getirir.

### 3. Grafik

**Grafik** butonu seçilen bölgedeki deprem büyüklüklerini zamana göre grafik üzerinde gösterir.

---

## 🗃️ Veritabanı Yapısı

Uygulama tarafından oluşturulan SQLite veritabanındaki `Depremler` tablosu:

| Alan       | Açıklama                             |
| ---------- | ------------------------------------ |
| `id`       | Benzersiz kayıt numarası             |
| `tarih`    | Depremin gerçekleştiği tarih ve saat |
| `enlem`    | Enlem bilgisi                        |
| `boylam`   | Boylam bilgisi                       |
| `derinlik` | Depremin derinliği                   |
| `buyukluk` | Deprem büyüklüğü                     |
| `yer`      | Depremin gerçekleştiği bölge         |

Aynı deprem kaydının tekrar eklenmesini önlemek amacıyla bazı alanlar üzerinde `UNIQUE` kısıtlaması bulunmaktadır.

---

## 🔄 Otomatik Güncelleme

Uygulama içerisinde ayrı bir thread kullanılarak veri güncelleme işlemi arka planda gerçekleştirilir.

```python
threading.Thread(
    target=arka_plan_guncelleme,
    daemon=True
).start()
```

Thread içerisinde her **60 saniyede bir** Kandilli Rasathanesi'nden yeni veriler alınır:

```text
Veri çek
   ↓
SQLite'a kaydet
   ↓
60 saniye bekle
   ↓
Tekrar veri çek
```

Bu sayede kullanıcı arayüzü açıkken veri toplama işlemi arka planda devam eder.

---

## 📷 Uygulama Görselleri

<img width="2876" height="1824" alt="image" src="https://github.com/user-attachments/assets/4c1b4ce3-a720-40cd-bd0a-0dbeba89af5b" />

<img width="1990" height="1142" alt="image" src="https://github.com/user-attachments/assets/1d33de67-e51d-4c79-b40c-43c008b4616c" />





## ⚠️ Veri Kaynağı

Deprem verileri **Kandilli Rasathanesi ve Deprem Araştırma Enstitüsü** tarafından yayınlanan web sayfasından alınmaktadır.

Uygulama eğitim/ödev ve yazılım geliştirme amacıyla hazırlanmıştır.

**Acil durumlarda bu uygulamaya güvenilmemeli; resmi kurumların duyuruları takip edilmelidir.**

---

## 📚 Öğrenilen Konular

Bu proje sayesinde aşağıdaki konularda pratik yapılmıştır:

* Python ile GUI geliştirme
* HTTP istekleri
* Web scraping
* HTML içerisinden veri ayrıştırma
* SQLite CRUD işlemleri
* SQL sorguları
* Thread kullanımı
* Veri filtreleme
* Regex kullanımı
* Tarih/saat işlemleri
* Veri görselleştirme
* Tkinter `Treeview`
* Python modüllerinin birlikte kullanılması

---

## 🔮 Gelecekte Eklenebilecek Özellikler

* [ ] Belirli bir büyüklüğün üzerindeki depremler için bildirim sistemi
* [ ] Harita üzerinde deprem konumlarını gösterme
* [ ] Deprem büyüklüğüne göre filtreleme
* [ ] Tarih aralığına göre filtreleme
* [ ] Daha gelişmiş grafikler
* [ ] Kullanıcı tarafından belirlenen şehirleri takip etme
* [ ] Deprem verilerini CSV/Excel olarak dışa aktarma
* [ ] Daha modern bir kullanıcı arayüzü
* [ ] İnternet bağlantısı olmadığında mevcut verileri görüntüleme

---

## 👨‍💻 Geliştirici

**Emir Duhan Atmaca**

Computer Engineering Student
Trakya University

---

## 📄 Lisans

Bu proje eğitim ve kişisel gelişim amacıyla geliştirilmiştir.
