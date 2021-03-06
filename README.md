# Python_dynamic_modules_presentation_with_integrated_plate_detection_and_reporting
Documentation Linki -> https://hasansarman.github.io/Python_dynamic_modules_presentation_with_integrated_plate_detection_and_reporting/

Herhangi bir sistem yada dependency ile sorun yasiyorsniz gelistirmeye baslanmak icin asagidaki linkten VIRTUALBOX image indirebilir akabinde.. u image VIRTUALBOX isimli program ile IMPORT ederek hemen kullanmaya baslayabilirsiniz. 
https://drive.google.com/file/d/1FXQh1EvDW6vCuCxjaWSUISdRZF3Vx1L_/view?usp=sharing

Docker asinaliginiz varsa .. DockerFile i ( GPU icin ayarli) kullanabilirsiniz.. lubcuda ve cudnn sorunlari olmadan gerekli her turk objenin kurulmus halidir.. 


![Image of excel output](https://hasansarman.github.io/Python_dynamic_modules_presentation_with_integrated_plate_detection_and_reporting/excel.png)



Bu yazilimdaki amac ->

1- DINAMIK olarak runtime da module eklenme yontemlerini gosterebilmek


2- farkli moduller kullanarak birden fazla algoritmayi ortak bir sekilde degerlendirebilmek ( old_result klasoru ve INPUT_OUTPUT/reports fikir verecektir.)


3- pythonda karsilasilan araliksiz Run/Debug islemleri sirasinda test edilen kod ve ciktilarin surekli olarka karisikliga sebeb olmasi musanesebityle otomatik ZIP olusturarark log /cikti/reporlarin paketlenmesi.. 

4- test edilmesi plananan her modul icin ornek -> Human detection icin , coco .. hog ..  dnn gibi bir cok farkli model/yapi denenirken bunlarin birbirleri arasindaki tam performans degerleri. her bir model icin resim hazirlama zamanindan islenmesi ve load timelara kadar gecen surelerin verimli bir sekilde kiyaslanabilmesi icin basit bir test platfomu olarak yazildi. sizlere sadece 

5- python da yeni yeni gelisim gosteren arkadaslara, basit ama sig fonksiyonlarla nasil bir yapi kurulabilecegi gosterilmek istendi.. excel.. csv gibi onemli toolarin nasil entegre edilerek kullanilabilecegi ogretilmis oldu.. 

6- piyasada bircok python profiler oldugu halde.. b8rada timing gibi kisimlarin elle tutulmasinin nedeni ortadaki karisikligi azaltmak.. ve piyasada bir cok basit profilerin temelde ne yaptigini gosterebilmekti. 

7- Cython veya pyinstaller ile paketleyip tum dependencyleri yaninda SO dosyasi olarak basabilecegim halde..  bu yazilimda PYTHON da yazilmis bir kodun gercekte nasil MODULER calismasi gerektigini gostermek icin.. 


OTOMATIK dependency injection ekledim.. bu kisim statics. uzerindeki listeyi alip bu listede adi gecen kutuphaneleri tarayip bulamadiklarini runtime da kurmak uzerine kurulu basit bir yapidir.. 
buradaki asil amac pythonda ihmal edilen IMPORT optimizasyonuna parmak basmaktir.. Duzgun ve optimize edilmis bir impoirt yapisi.. ileride size yaziliminizin herhangi bir dependency gereksinimi yuzunden patlamadan dinamik oalrak genlesebilmesi olanagini nasil taniyacagini gostermektedir. 

Yazarken daha once kullanma firsati bulamadigim TEXTBOX gibi ilave kutuphaneleri kullanarak bu tip bir kodu bilinen hazir library ler ile yazip gecistirtmemek adina kodu biraz uzun tuttum.tesseract modulunde ozellikle opencv yontemleri ile image kalitesi ve tesseract performansi arttirmaya yonelik bir calisma yaptim.. alternatif library ler ile daha kolay sonuc alabildigim halde.. opencv base code ile nasil yapialcagini gostermektedir.


openalpr modulu aslinda fazla bir sey yapmadan sadece hazir bir library uzerinde claistirip yetkin sonuclar almak icin kullanildi.. 

Burada RE kullanarak cikti olarak testlerdeki TURK plaka yapisini bazi alip textlerdeki kirlilikleri temizleyerek yola devam etmek cok kolay olacak basari oranini bir cok resimde bir ust seviyeye tasiyacakti..fakat benim gormek istedigim ALGORITMA daki basari oranini saklamaktadir.. o yuzden kullanmadim. 

kodun calisabilmesi icin gerekli KUutuphaneler dinamik yuklenmektedir..

```
git clone https://github.com/hasansarman/Python_dynamic_modules_presentation_with_integrated_plate_detection_and_reporting.git
```
openalpr in kurulabilmesi icin asagidaki adimlar izlenmeli.. 
```
sudo apt-get install libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev

sudo apt-get install liblog4cplus-dev libcurl3-dev

sudo apt-get install beanstalkd

git clone https://github.com/openalpr/openalpr.git

cd openalpr/src
mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..
make

sudo make install
```

TEST PLATFOMUNUN DUZGUN CALISABILMESI ICIN VE SIZE GERCEK SKORLARI VE BASARIYI GOSTEREBILMESI ICIN Statics.RESULTSET dosyasini laistirmadan once kendi resultlariniza gore duzenlerseniz.. olusturdugu raporlarda tum sapma sekilleri ve duzeltmeler icin gerekli yuzdelik oneriyi yapacaktir. 



Tum datalar ve ciktilar asagidaki klasor yapisi ile tutulmaktadir.. 

logs/ -> her calismada yeni bir dosya olusuturp loglari hem konsoldan hemde file olarak yazar.. 


INPUT_OUTPUT/img => input imagelerin listesi

INPUT_OUTPUT/outputs => Her modulun step by step ciktisi alinmak istenirse yazilacak olan dosya.. islemler bitince ziplenerek saklanir.. 

INPUT_OUTPUT/reports/ => her claistirmadan calisma zamani ile 1 klasor acarak her module icin timing ve basari oranlarini iceren bilahare 1 adet excel dosyasindada tum data ve ciktilari tutan dosyalari tutar

old_results -> gecmis loglar ve reportlar ziplenerek timestamp ile tutulur
 html -> documentation.. 




BAZI ORNEK CIKTILAR














```

+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                         Module Name                          |   Process   | start time | end_time  | delta_time_seconds |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                         TestOpenalp                          |   Total     | 38095.995  | 38099.141 |       3.146        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                         TestOpenalp                          |  Prep Work  | 38095.995  | 38095.995 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                     bos-plaka-bulma.jpg                      |  img Prep   | 38095.995  | 38095.995 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                     bos-plaka-bulma.jpg                      | img process | 38095.995  | 38096.163 |       0.168        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                      tr-plaka-png-4.png                      |  img Prep   | 38096.163  | 38096.163 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                      tr-plaka-png-4.png                      | img process | 38096.163  | 38096.313 |        0.15        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        turkije23.jpg                         |  img Prep   | 38096.313  | 38096.313 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        turkije23.jpg                         | img process | 38096.313  | 38096.501 |       0.189        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                          0x0-2.jpg                           |  img Prep   | 38096.501  | 38096.501 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                          0x0-2.jpg                           | img process | 38096.501  | 38096.643 |       0.142        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
| 44_ab_044_malatya_ozel_plaka_sat_l_k_8390135523727512913.jpg |  img Prep   | 38096.643  | 38096.643 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
| 44_ab_044_malatya_ozel_plaka_sat_l_k_8390135523727512913.jpg | img process | 38096.643  | 38096.788 |       0.145        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|       app-plakalar-cesitleri-129120064433690-1223.jpeg       |  img Prep   | 38096.788  | 38096.788 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|       app-plakalar-cesitleri-129120064433690-1223.jpeg       | img process | 38096.788  | 38096.968 |        0.18        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|        app-plakalar-cesitleri-129120064433690-12.jpeg        |  img Prep   | 38096.968  | 38096.968 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|        app-plakalar-cesitleri-129120064433690-12.jpeg        | img process | 38096.968  | 38097.14  |       0.171        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|             61BB2F3F8DE7424F88551964D7D0252F.jpg             |  img Prep   |  38097.14  | 38097.14  |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|             61BB2F3F8DE7424F88551964D7D0252F.jpg             | img process |  38097.14  | 38097.285 |       0.145        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        turkije36.jpg                         |  img Prep   | 38097.285  | 38097.285 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        turkije36.jpg                         | img process | 38097.285  | 38097.477 |       0.192        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                          5DYvgL.jpg                          |  img Prep   | 38097.477  | 38097.477 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                          5DYvgL.jpg                          | img process | 38097.477  | 38097.66  |       0.183        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       plaka-png-1.png                        |  img Prep   |  38097.66  | 38097.66  |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       plaka-png-1.png                        | img process |  38097.66  | 38097.805 |       0.145        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                      download33221.jpg                       |  img Prep   | 38097.805  | 38097.805 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                      download33221.jpg                       | img process | 38097.805  | 38097.944 |       0.138        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       download223.jpg                        |  img Prep   | 38097.944  | 38097.944 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       download223.jpg                        | img process | 38097.944  | 38098.061 |       0.117        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                440px-Turkey_licenceplate.jpg                 |  img Prep   | 38098.061  | 38098.061 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                440px-Turkey_licenceplate.jpg                 | img process | 38098.061  | 38098.191 |       0.131        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                rckdr5Tfmka3XzHlJJU0JA222.jpg                 |  img Prep   | 38098.191  | 38098.191 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                rckdr5Tfmka3XzHlJJU0JA222.jpg                 | img process | 38098.191  | 38098.343 |       0.152        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       unnamed (1).jpg                        |  img Prep   | 38098.343  | 38098.343 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       unnamed (1).jpg                        | img process | 38098.343  | 38098.49  |       0.147        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        images (3).jpg                        |  img Prep   |  38098.49  | 38098.49  |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        images (3).jpg                        | img process |  38098.49  | 38098.642 |       0.152        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       turk35GA4434.jpg                       |  img Prep   | 38098.642  | 38098.642 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       turk35GA4434.jpg                       | img process | 38098.642  | 38098.868 |       0.227        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        images (2).jpg                        |  img Prep   | 38098.868  | 38098.868 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        images (2).jpg                        | img process | 38098.868  | 38099.001 |       0.132        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                          images.jpg                          |  img Prep   | 38099.001  | 38099.001 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                          images.jpg                          | img process | 38099.001  | 38099.141 |       0.141        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+





+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                         Module Name                          |   Process   | start time | end_time  | delta_time_seconds |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                         TestOpenalp                          |   Total     | 38095.995  | 38099.141 |       3.146        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                         TestOpenalp                          |  Prep Work  | 38095.995  | 38095.995 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                     bos-plaka-bulma.jpg                      |  img Prep   | 38095.995  | 38095.995 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                     bos-plaka-bulma.jpg                      | img process | 38095.995  | 38096.163 |       0.168        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                      tr-plaka-png-4.png                      |  img Prep   | 38096.163  | 38096.163 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                      tr-plaka-png-4.png                      | img process | 38096.163  | 38096.313 |        0.15        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        turkije23.jpg                         |  img Prep   | 38096.313  | 38096.313 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        turkije23.jpg                         | img process | 38096.313  | 38096.501 |       0.189        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                          0x0-2.jpg                           |  img Prep   | 38096.501  | 38096.501 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                          0x0-2.jpg                           | img process | 38096.501  | 38096.643 |       0.142        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
| 44_ab_044_malatya_ozel_plaka_sat_l_k_8390135523727512913.jpg |  img Prep   | 38096.643  | 38096.643 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
| 44_ab_044_malatya_ozel_plaka_sat_l_k_8390135523727512913.jpg | img process | 38096.643  | 38096.788 |       0.145        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|       app-plakalar-cesitleri-129120064433690-1223.jpeg       |  img Prep   | 38096.788  | 38096.788 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|       app-plakalar-cesitleri-129120064433690-1223.jpeg       | img process | 38096.788  | 38096.968 |        0.18        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|        app-plakalar-cesitleri-129120064433690-12.jpeg        |  img Prep   | 38096.968  | 38096.968 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|        app-plakalar-cesitleri-129120064433690-12.jpeg        | img process | 38096.968  | 38097.14  |       0.171        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|             61BB2F3F8DE7424F88551964D7D0252F.jpg             |  img Prep   |  38097.14  | 38097.14  |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|             61BB2F3F8DE7424F88551964D7D0252F.jpg             | img process |  38097.14  | 38097.285 |       0.145        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        turkije36.jpg                         |  img Prep   | 38097.285  | 38097.285 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        turkije36.jpg                         | img process | 38097.285  | 38097.477 |       0.192        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                          5DYvgL.jpg                          |  img Prep   | 38097.477  | 38097.477 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                          5DYvgL.jpg                          | img process | 38097.477  | 38097.66  |       0.183        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       plaka-png-1.png                        |  img Prep   |  38097.66  | 38097.66  |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       plaka-png-1.png                        | img process |  38097.66  | 38097.805 |       0.145        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                      download33221.jpg                       |  img Prep   | 38097.805  | 38097.805 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                      download33221.jpg                       | img process | 38097.805  | 38097.944 |       0.138        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       download223.jpg                        |  img Prep   | 38097.944  | 38097.944 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       download223.jpg                        | img process | 38097.944  | 38098.061 |       0.117        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                440px-Turkey_licenceplate.jpg                 |  img Prep   | 38098.061  | 38098.061 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                440px-Turkey_licenceplate.jpg                 | img process | 38098.061  | 38098.191 |       0.131        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                rckdr5Tfmka3XzHlJJU0JA222.jpg                 |  img Prep   | 38098.191  | 38098.191 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                rckdr5Tfmka3XzHlJJU0JA222.jpg                 | img process | 38098.191  | 38098.343 |       0.152        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       unnamed (1).jpg                        |  img Prep   | 38098.343  | 38098.343 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       unnamed (1).jpg                        | img process | 38098.343  | 38098.49  |       0.147        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        images (3).jpg                        |  img Prep   |  38098.49  | 38098.49  |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        images (3).jpg                        | img process |  38098.49  | 38098.642 |       0.152        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       turk35GA4434.jpg                       |  img Prep   | 38098.642  | 38098.642 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                       turk35GA4434.jpg                       | img process | 38098.642  | 38098.868 |       0.227        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        images (2).jpg                        |  img Prep   | 38098.868  | 38098.868 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                        images (2).jpg                        | img process | 38098.868  | 38099.001 |       0.132        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                          images.jpg                          |  img Prep   | 38099.001  | 38099.001 |        0.0         |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+
|                          images.jpg                          | img process | 38099.001  | 38099.141 |       0.141        |
+--------------------------------------------------------------+-------------+------------+-----------+--------------------+


```

