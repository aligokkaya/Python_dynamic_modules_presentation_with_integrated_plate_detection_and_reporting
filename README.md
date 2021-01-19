# Python_dynamic_modules_presentation_with_integrated_plate_detection_and_reporting
Documentation Linki -> https://hasansarman.github.io/Python_dynamic_modules_presentation_with_integrated_plate_detection_and_reporting/



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
```
```
sudo apt-get install liblog4cplus-dev libcurl3-dev
```
```
sudo apt-get install beanstalkd
```
openalpr/srcmkdir buildcd build# setup the compile environment
```
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..
```


```
sudo make install
```


```
wget http://plates.openalpr.com/h786poj.jpg -O lp.jpgalpr lp.jpg
```
