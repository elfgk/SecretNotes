from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64


pencere= Tk()
pencere.title("Gizli Notlar")
pencere.minsize(300,600)
pencere.config(bg="light blue")
pencere.geometry("400x700+500+50")


# arkaplan
gorsel = Image.open("yeni.jpg")
yeni_gorsel = gorsel.resize((400, 700), Image.LANCZOS)
arka_plan = ImageTk.PhotoImage(yeni_gorsel)
gorsel_label = Label(pencere, image=arka_plan)
gorsel_label.place(x=0, y=0, width=400, height=700)

gizli = Image.open("topsecret.jpg")
gizli_yeni = gizli.resize((150, 150), Image.LANCZOS)
gizli_yazisi = ImageTk.PhotoImage(gizli_yeni)
gizli_label = Label(pencere, image=gizli_yazisi)
gizli_label.pack()

baslik_yazisi = Label(text="Başlığınızı Giriniz:")
baslik_yazisi.place(relx=0.4, rely=0.33)

girilen_baslik = Entry(width=20)
girilen_baslik.place(relx=0.36, rely=0.36)

girilen_metin = Text(width=20, height=10)
girilen_metin.place(relx=0.32, rely=0.4)

sifre_yazisi = Label(text="Şifrenizi Giriniz:")
sifre_yazisi.place(relx=0.4, rely=0.65)

girilen_sifre = Entry(width=20, show="*")  # Şifreyi gizli göstermek
girilen_sifre.place(relx=0.36, rely=0.68)

# Şifreyi anahtara dönüştürme fonksiyonu
def sifre_anahtar_uret(sifre):
    salt = b't'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(sifre.encode()))
    return key



def sifrele_kaydet():
    baslik= girilen_baslik.get()
    sifre = girilen_sifre.get()
    metin = girilen_metin.get("1.0", "end-1c")

    if not sifre or not metin:
        messagebox.showwarning("Uyarı", "Şifre ve metin alanlarını doldur")
        return

    # Şifreyi anahtara dönüştür
    key = sifre_anahtar_uret(sifre)
    anahtar = Fernet(key)

    # Metni şifreleyip byte formatına çevir
    sifreli_metin = anahtar.encrypt(metin.encode())

    # Şifrelenmiş metni ekrana yazdır
    print("Şifrelenmiş metin:\n", sifreli_metin.decode())

    #Şifrelenmiş metni kullanıcıya göster
    messagebox.showinfo("Şifrelenmiş Metin", sifreli_metin.decode())

    dosya_adi = "metinler.txt"
    with open(dosya_adi, "a") as dosya:
        dosya.write(baslik  +"\n")
        dosya.write(sifreli_metin.decode()+"\n")  #Metni dosyaya yaz

    messagebox.showinfo("Bilgi", f"Şifrelenmiş metin '{dosya_adi}' dosyasına kaydedildi.")

def coz():
    sifre = girilen_sifre.get()
    sifreli_metin = girilen_metin.get("1.0", "end-1c").strip()  # Şifrelenmiş metin

    if not sifre or not sifreli_metin:
        messagebox.showwarning("Uyarı", "Şifre ve şifrelenmiş metin alanlarını doldurun.")
        return

    key = sifre_anahtar_uret(sifre)
    anahtar = Fernet(key)

    try:
        # Şifrelenmiş metni çöz
        cozulmus_metin = anahtar.decrypt(sifreli_metin.encode())
        girilen_metin.delete("1.0", "end")  # Önceki metni sil
        #girilen_metin.insert("1.0", cozulmus_metin.decode())  # Çözülmüş metni göster
        messagebox.showinfo("Çözülmüş Metin",cozulmus_metin.decode())
    except Exception as e:
        messagebox.showerror("Hata", f"Şifre yanlış veya metin çözülemedi.\nHata: {str(e)}")


kaydet_sifrele = Button(text="Kaydet ve Şifrele", command=sifrele_kaydet)
kaydet_sifrele.place(relx=0.4, rely=0.72)

desifre = Button(text="Çöz",command=coz)
desifre.place(relx=0.47, rely=0.77)


pencere.mainloop()
