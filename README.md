# Assembly Conveyor Monitoring Client App

Pengumpulan Data Serial dan Komunikasi API dengan Python. Script Python ini menunjukkan cara mengumpulkan data serial dari Arduino Uno dan mengirimkannya ke endpoint API HTTP.

## Persyaratan

- Python 3.x
- Pustaka `pyserial` (`pip install pyserial`)
- Pustaka `requests` (`pip install requests`)
- Arduino Uno yang terhubung melalui USB

## Penggunaan

1. **Pemasangan**

    - Hubungkan Arduino Uno ke komputermu melalui USB.
    - Instal Python 3.x jika belum terinstal.
    - Instal pustaka Python yang diperlukan dengan menjalankan:
      
      ```bash
      pip install pyserial requests
      ```

2. **Konfigurasi**

    - Modifikasi file `config.json` untuk menyesuaikan durasi pengumpulan data dalam hitungan detik.
    - Gantikan placeholder API endpoint (`https://your-api-endpoint-here.com/data`) dalam script Python dengan endpoint API sebenarnya.

3. **Menjalankan Script**

    - Buka terminal atau command prompt.
    - Navigasi ke direktori yang berisi script Python.
    - Jalankan script menggunakan perintah:
      
      ```bash
      python main.py
      ```

4. **Perilaku yang Diharapkan**

    - Script akan mengumpulkan data serial dari Arduino Uno selama durasi yang ditentukan.
    - Setelah itu, akan mencoba mengirimkan data yang terkumpul ke endpoint API yang telah dikonfigurasi.
    - Kesalahan yang terjadi selama pengumpulan data atau komunikasi dengan API akan dicatat dalam `error.log`.

5. **Menghentikan Script**

    - Untuk menghentikan script, tekan `Ctrl+C` di terminal atau command prompt.

6. **Catatan**

    - Pastikan port serial yang benar (`serial_port`) dan baud rate (`baud_rate`) diatur dalam script Python berdasarkan konfigurasi Arduino Unomu.

