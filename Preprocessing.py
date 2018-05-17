import re, glob, nltk, string, csv, math
import numpy as np
from collections import Counter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory


factory1 = StopWordRemoverFactory()
stopword = factory1.create_stop_word_remover()

factory2 = StemmerFactory()
stemmer = factory2.create_stemmer()

with open('kamus/katadasar.txt', 'r') as filekatadasar,open('kamus/katadasar.txt', 'r') as filevocab:
    katadasar = filekatadasar.read().replace('\n', ',')
    vocab = filevocab.read().replace('\n', ',')

def preprocessing(dataset):
    tokenizing = dataset.split(' ')
    hasilprepro = []
    for i in range(len(tokenizing)):
        teks = re.sub('(\d)+(\.)*(\d)*', '', tokenizing[i])  # hapus digit
        teks = re.sub('[/+@.,%-%^*"!#-$-\']', '', teks)  # hapus simbol
        teks = teks.lower()

        #stopword removal
        prestopword = stopword.remove(teks)

        if prestopword in vocab and prestopword != '':
            hasilprepro.append(prestopword)
        else:
            #stemming
            hasilstem = stemmer.stem(prestopword)
            if hasilstem in katadasar and hasilstem != '':
                hasilprepro.append(hasilstem)
    return hasilprepro

def bacafile(filename):
    semua = []
    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            print("Data ke-", row[0])
            if row:
                HasilPrepro = preprocessing(row[1])
                semua.append(HasilPrepro)
            else:
                continue
            #print(HasilPrepro)
    return semua

def main7():
    panjangTang = bacafile('PusatBahasaP.csv')

    daftarDokumen = {}
    # tampung data dari direktori ke variable daftarDokumen
    for i in range(len(panjangTang)):
        daftarDokumen[i] = Counter(panjangTang[i])


    print(len(panjangTang))
    # print("handle data ", handledata)
    print("panjang tanggapan ", panjangTang)
    print("daftar dokumen ", daftarDokumen)

    # menampung daftar string
    daftarString = []
    for key, val in daftarDokumen.items():  # melompati(loop over) key di kamus
        for word, count_w in val.items():
            if word not in daftarString:
                daftarString.append(word)  # append untuk menambah objek word baru kedalam list

    print("daftar string : ", daftarString)
    # Membuat TF
    with open('TF.csv', 'w', newline='') as csvfile, open('IDF.csv', 'w', newline='') as csvfileIDF, open('TFxIDF.csv', 'w', newline='') as csvfileTFIDF:
        reswriterTFIDF = csv.writer(csvfileTFIDF, delimiter=',', quotechar='|')
        reswriterIDF = csv.writer(csvfileIDF, delimiter=',', quotechar='|')
        reswriter = csv.writer(csvfile, delimiter=',', quotechar='|')
        tempWord = [' ']
        tempWord.extend(daftarString)  # menambah string2 dari variable daftarString ke tempWord
        reswriter.writerow(tempWord)  # write 1 row
        reswriterIDF.writerow(tempWord)  # write 1 row
        reswriterTFIDF.writerow(tempWord)  # write 1 row
        secondDF = []
        TF = []
        ############### TF ###################
        for i in range(len(panjangTang)):
            rowjudul = "Tanggapan " + str(i)
            # hitung pertanggapan
            words = panjangTang[i]
            x = []
            currentDF = []
            for j in range(len(daftarString)):
                temp = daftarString[j]
                count = 0
                for k in range(len(words)):
                    if (temp == words[k]):
                        count += 1
                # Frequency weighting
                if count > 0:
                    count = round(1 + np.log(count), 2)
                    currentDF.append(1)
                else:
                    currentDF.append(0)
                x.append(count)

            x.insert(0, rowjudul)
            TF.append(x)
            reswriter.writerow(x)
            secondDF.append(currentDF)
        ############### TF ###################
        # print("panjang secondDF:",secondDF)
        # print("ini TF:", TF)
        # print("second df",secondDF)

        ############### IDF ###################
        hasilDF = []
        for i in range(len(secondDF)):
            first = []
            second = []
            dalem = secondDF[i]
            if i == 0:
                for j in range(len(dalem)):
                    hasilDF.append(dalem[j])
            else:
                for j in range(len(dalem)):
                    first.append(hasilDF[j])
                    second.append(dalem[j])
                hasilDF = []
            for k in range(len(first)):
                hasilDF.append(first[k] + second[k])
        # print("ini baru DF :", hasilDF)

        IDF=[]
        for j in range(len(hasilDF)):
            if hasilDF[j]==0:
                IDF.append(0)
            else:
                nilaiutkIDF = len(panjangTang)/hasilDF[j]
                nilaiIDF = math.log(nilaiutkIDF,10)
                IDF.append(nilaiIDF)
        #print("Hasil IDFnya :", IDF)
        IDF.insert(0,"IDFnya")
        reswriterIDF.writerow(IDF)
        ############### IDF ###################

        ############### TFxIDF ###################
        # print("IDF Final :",IDF)
        # print("panjang TF :",len(TF))
        TFxIDF =[]
        for k in range(len(TF)):
            rowjudul = "Tanggapan " + str(k)
            dalem = TF[k]
            sumTFIDF = []
            for i in range(len(dalem)):
                if i == 0:
                    sumTFIDF.insert(0, rowjudul)
                else:
                    sumTFIDF.append(dalem[i]*IDF[i])
            #sumTFIDF.insert(0, rowjudul)
            reswriterTFIDF.writerow(sumTFIDF)
        ############### TFxIDF ###################
main7()