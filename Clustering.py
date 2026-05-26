import pandas as pd
import matplotlib.pyplot as plt
import random
import math

# baca data
dataNilai = pd.read_csv('datasetMahasiswa.csv', sep=';')

# ambil nilai
data = dataNilai[['math', 'baca', 'tulis']].values.tolist()

# jumlah cluster
k = 3
b = 0
# centroid awal
centroid = random.sample(data, k)
# pengulangan clustering
print()
for baris in range(6):

    cluster = []

    # cari cluster terdekat
    for titik in data:

        jarak = []

        for c in centroid:
            d = math.sqrt(
                (titik[0]-c[0])**2 +
                (titik[1]-c[1])**2 +
                (titik[2]-c[2])**2
            )

            jarak.append(d)

        cluster.append(jarak.index(min(jarak)) + 1)

    # update centroid
    centroid_baru = []

    for i in range(k):
    
        anggota = [
            data[j]
            for j in range(len(data))
            if cluster[j] == i + 1
        ]

        x = sum(a[0] for a in anggota) / len(anggota)
        y = sum(a[1] for a in anggota) / len(anggota)
        z = sum(a[2] for a in anggota) / len(anggota)

        centroid_baru.append([x, y, z])

    centroid = centroid_baru
    print(f"Iterasi ke {b+1} {cluster}")
    b = b + 1
# simpan cluster
dataNilai['cluster'] = cluster
print()
print(dataNilai)

# visualisasi
gambar = plt.figure()
ax = gambar.add_subplot(111, projection='3d')

ax.scatter(
    dataNilai['math'],
    dataNilai['baca'],
    dataNilai['tulis'],
    c=dataNilai['cluster']
)



plt.show()