import pandas as pd
import matplotlib.pyplot as plt
import math

dataNilai = pd.read_csv(
    r'C:\Bima\Elbima Kuliah\Semester 2\Tugas\Matematika Informatika\CLUSTERING\Kode Program\datasetMahasiswa.csv',
    sep=';'
)

data = dataNilai[['math', 'baca', 'tulis']].values.tolist()

print(dataNilai[['math', 'baca', 'tulis']].describe().round(2))

cluster1 = []
k = 3
b = 0

centroid = [
    [85, 90, 98],
    [25, 30, 35],
    [50, 55, 60]
]

hasil_iterasi = []

print()

for baris in range(6):

    cluster2 = []

    # Menentukan cluster setiap data
    for titik in data:
        jarak = []

        for c in centroid:
            d = math.sqrt(
                (titik[0] - c[0])**2 +
                (titik[1] - c[1])**2 +
                (titik[2] - c[2])**2
            )
            jarak.append(d)

        cluster2.append(jarak.index(min(jarak)) + 1)

    # Cek apakah cluster sudah stabil
    if cluster2 == cluster1:
        print(f"Centroid stabil di iterasi ke {b}")
        break

    cluster1 = cluster2.copy()

    print(f"\n--- Iterasi ke-{b+1} ---")

    for i in range(k):

        indeks_cluster = [
            j for j in range(len(cluster2))
            if cluster2[j] == i + 1
        ]

        jumlah = len(indeks_cluster)

        print(f"  Cluster {i+1}: {jumlah} siswa")

        hasil_iterasi.append({
            'Iterasi': f'Iterasi ke-{b+1}',
            'Cluster': f'Cluster {i+1}',
            'Jumlah Siswa': jumlah
        })

    # Update centroid
    centroid_baru = []

    for i in range(k):

        anggota = [
            data[j]
            for j in range(len(data))
            if cluster2[j] == i + 1
        ]

        x = sum(a[0] for a in anggota) / len(anggota)
        y = sum(a[1] for a in anggota) / len(anggota)
        z = sum(a[2] for a in anggota) / len(anggota)

        centroid_baru.append([x, y, z])

    centroid = centroid_baru
    b += 1

# TABEL RINGKASAN

df_hasil = pd.DataFrame(hasil_iterasi)

# Simpan hasil cluster
dataNilai['cluster'] = cluster2

# Z-SCORE & DETEKSI OUTLIER

n = len(data)

mean_math = sum(data[i][0] for i in range(n)) / n
mean_baca = sum(data[i][1] for i in range(n)) / n
mean_tulis = sum(data[i][2] for i in range(n)) / n

std_math = math.sqrt(
    sum((data[i][0] - mean_math) ** 2 for i in range(n)) / n
)

std_baca = math.sqrt(
    sum((data[i][1] - mean_baca) ** 2 for i in range(n)) / n
)

std_tulis = math.sqrt(
    sum((data[i][2] - mean_tulis) ** 2 for i in range(n)) / n
)

print("\n=== DETEKSI OUTLIER ===")

for i in range(n):

    z_math = (data[i][0] - mean_math) / std_math
    z_baca = (data[i][1] - mean_baca) / std_baca
    z_tulis = (data[i][2] - mean_tulis) / std_tulis

    if abs(z_math) > 3 or abs(z_baca) > 3 or abs(z_tulis) > 3:
        print(
            f"Data ke-{i+1} OUTLIER → "
            f"z_math={z_math:.2f}, "
            f"z_baca={z_baca:.2f}, "
            f"z_tulis={z_tulis:.2f}"
        )

print("Selesai cek outlier")

# HITUNG SSE

sse = 0

for i in range(len(data)):

    cluster_ke = cluster2[i] - 1
    c = centroid[cluster_ke]

    sse += (
        (data[i][0] - c[0])**2 +
        (data[i][1] - c[1])**2 +
        (data[i][2] - c[2])**2
    )

print(f"\nNilai SSE = {sse:.4f}")

print()
print(dataNilai)

# VISUALISASI 3D

gambar = plt.figure()

ax = gambar.add_subplot(projection='3d')

ax.scatter(
    dataNilai['math'],
    dataNilai['baca'],
    dataNilai['tulis'],
    c=dataNilai['cluster']
)

ax.set_xlabel('Math')
ax.set_ylabel('Baca')
ax.set_zlabel('Tulis')

plt.show()

# DISTRIBUSI JUMLAH SISWA PER CLUSTER

cluster_counts = [
    int(cluster2.count(i + 1))
    for i in range(k)
]

plt.figure()

plt.bar(
    ['Cluster 1', 'Cluster 2', 'Cluster 3'],
    cluster_counts,
    color=['blue', 'red', 'green']
)

plt.title('Distribusi Jumlah Siswa per Cluster')
plt.xlabel('Cluster')
plt.ylabel('Jumlah Siswa')

plt.savefig('distribusi_cluster.png')

plt.show()