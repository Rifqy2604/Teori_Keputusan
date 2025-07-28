import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nTekan Enter untuk kembali ke menu...")

def get_input_alternatif(kondisi):
    alternatif = {}
    while True:
        try:
            n = int(input("Berapa banyak alternatif (misalnya: Produk A, B, dst)? "))
            if n > 0:
                break
            else:
                print("❌ Jumlah alternatif harus lebih dari 0.")
        except ValueError:
            print("❌ Masukkan angka bulat.")

    for i in range(n):
        nama = input(f"\nNama alternatif #{i+1}: ")
        payoff = []
        for k in kondisi:
            while True:
                try:
                    nilai = float(input(f"  Keuntungan jika permintaan {k}: "))
                    payoff.append(nilai)
                    break
                except ValueError:
                    print("❌ Masukkan angka.")
        alternatif[nama] = payoff
    return alternatif

def get_probabilitas(kondisi):
    while True:
        print("\nMasukkan probabilitas untuk masing-masing kondisi:")
        probabilitas = []
        for k in kondisi:
            while True:
                try:
                    p = float(input(f"Probabilitas permintaan {k}: "))
                    if 0 <= p <= 1:
                        probabilitas.append(p)
                        break
                    else:
                        print("❌ Probabilitas harus antara 0 dan 1.")
                except ValueError:
                    print("❌ Masukkan angka desimal, contoh: 0.5")
        total = sum(probabilitas)
        if abs(total - 1.0) > 0.01:
            print(f"\n⚠️ Jumlah probabilitas = {total}, seharusnya 1.0")
            print("Silakan ulangi input.")
        else:
            return probabilitas

def hitung_emv(alternatif, probabilitas):
    emv_dict = {}
    for nama, payoff_list in alternatif.items():
        kombinasi = zip(probabilitas, payoff_list)
        emv = sum(prob * hasil for prob, hasil in kombinasi)
        emv_dict[nama] = emv
    return emv_dict

def hitung_laplace(alternatif):
    laplace_dict = {}
    for nama, payoff_list in alternatif.items():
        rata = sum(payoff_list) / len(payoff_list)
        laplace_dict[nama] = rata
    return laplace_dict

def hitung_evpi(alternatif, probabilitas, kondisi):
    jumlah_kondisi = len(kondisi)
    terbaik_per_kondisi = []
    for i in range(jumlah_kondisi):
        nilai_terbaik = max(alt[i] for alt in alternatif.values())
        terbaik_per_kondisi.append(nilai_terbaik)
    evwpi = sum(prob * val for prob, val in zip(probabilitas, terbaik_per_kondisi))
    emv_dict = hitung_emv(alternatif, probabilitas)
    emv_terbaik = max(emv_dict.values())
    evpi = evwpi - emv_terbaik
    return evwpi, emv_terbaik, evpi

def tampilkan_pohon_teks(alternatif, probabilitas, kondisi):
    print("\n[Keputusan]")
    for nama_alt, payoff in alternatif.items():
        print(f"├── {nama_alt}")
        for i in range(len(kondisi)):
            prob_str = f"P={probabilitas[i]:.2f}"
            print(f"│   ├── Permintaan {kondisi[i]} ({prob_str}): Payoff = {payoff[i]}")

def hitung_maximax(alternatif):
    return {nama: max(payoff) for nama, payoff in alternatif.items()}

def hitung_maximin(alternatif):
    return {nama: min(payoff) for nama, payoff in alternatif.items()}

# ================= MAIN LOOP =================
kondisi = ['Rendah', 'Sedang', 'Tinggi']
data_alt = {}
prob = []

while True:
    clear_screen()
    print("\n=== PROGRAM TEORI KEPUTUSAN ===")
    print("1. Masukkan Alternatif dan Probabilitas")
    print("2. Hitung EMV")
    print("3. Hitung Laplace")
    print("4. Hitung EVPI")
    print("5. Hitung Maximax")
    print("6. Hitung Maximin")
    print("0. Keluar")

    pilihan = input("Pilih opsi: ")

    if pilihan == "1":
        clear_screen()
        data_alt = get_input_alternatif(kondisi)
        prob_temp = get_probabilitas(kondisi)
        if prob_temp:
            prob = prob_temp
            print("\n✅ Data berhasil disimpan.")

            # TAMPILKAN TABEL SECARA MANUAL
            print("\n📊 Tabel Alternatif dan Payoff:")
            print(f"{'Alternatif':<15}" + "".join(f"{k:<10}" for k in kondisi))
            for nama, payoff in data_alt.items():
                print(f"{nama:<15}" + "".join(f"{v:<10}" for v in payoff))

            # TAMPILKAN PROBABILITAS
            print("\n📈 Probabilitas:")
            for k, p in zip(kondisi, prob):
                print(f"  - Permintaan {k}: {p:.2f}")
        pause()

    elif pilihan == "2":
        clear_screen()
        if not data_alt or not prob:
            print("⚠️ Masukkan data dulu di opsi 1.")
            pause()
            continue
        hasil = hitung_emv(data_alt, prob)
        print("\n--- Hasil EMV ---")
        for alt, val in hasil.items():
            print(f"{alt}: {val}")
        terbaik = max(hasil, key=hasil.get)
        print(f">>> Keputusan terbaik: {terbaik}")
        tampilkan_pohon_teks(data_alt, prob, kondisi)
        pause()

    elif pilihan == "3":
        clear_screen()
        if not data_alt:
            print("⚠️ Masukkan data dulu di opsi 1.")
            pause()
            continue
        hasil = hitung_laplace(data_alt)
        print("\n--- Hasil Laplace ---")
        for alt, val in hasil.items():
            print(f"{alt}: {val}")
        terbaik = max(hasil, key=hasil.get)
        print(f">>> Keputusan terbaik: {terbaik}")
        pause()

    elif pilihan == "4":
        clear_screen()
        if not data_alt or not prob:
            print("⚠️ Masukkan data dulu di opsi 1.")
            pause()
            continue
        evwpi, emv_terbaik, evpi = hitung_evpi(data_alt, prob, kondisi)
        print("\n--- Hasil EVPI ---")
        print(f"EVwPI: {evwpi}")
        print(f"EMV terbaik: {emv_terbaik}")
        print(f"EVPI: {evpi}")
        pause()

    elif pilihan == "5":
        clear_screen()
        if not data_alt:
            print("⚠️ Masukkan data dulu di opsi 1.")
            pause()
            continue
        hasil = hitung_maximax(data_alt)
        print("\n--- Hasil Maximax ---")
        for alt, val in hasil.items():
            print(f"{alt}: {val}")
        terbaik = max(hasil, key=hasil.get)
        print(f">>> Keputusan terbaik: {terbaik}")
        pause()

    elif pilihan == "6":
        clear_screen()
        if not data_alt:
            print("⚠️ Masukkan data dulu di opsi 1.")
            pause()
            continue
        hasil = hitung_maximin(data_alt)
        print("\n--- Hasil Maximin ---")
        for alt, val in hasil.items():
            print(f"{alt}: {val}")
        terbaik = max(hasil, key=hasil.get)
        print(f">>> Keputusan terbaik: {terbaik}")
        pause()

    elif pilihan == "0":
        print("👋 Terima kasih, program selesai.")
        break

    else:
        print("❌ Opsi tidak dikenali.")
        pause()
