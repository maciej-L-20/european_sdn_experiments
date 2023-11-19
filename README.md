# SCHT laboratorium
Katalog zawiera skrypty i wyniki testów z laboratorium nr.1 i nr.2 z przedmiotu Sieci i chmury teleinformatyczne, wykonane przez Macieja Lipskiego i Jakuba Szwedę.
Poniżej opisano zawartość poszczególnych folderów. W celu uruchomienia aplikacji do kierowania strumieni, należy uruchomić skrypt userInterface.py. Aby uruchomić sieć należy:
1. Przenieść na maszynę wirtualną skrypt setup.sh
2. Uruchomić serwer pythona na własnym hoście w folderze scriptFiles (python3 -m http.server)
3. Przenieść na maszynę wirtualną skrypt setup.sh
4. Zmienić uprawnienia skryptu setup.sh (chmod +x setup.sh)
5. Uruchomić skrypt setup.sh z parametrem -h <ip hosta z serwerem w folderze scriptFile>
6. Uruchomić kontroler ONOS
7. Uruchomić sieć mininet wskazując jako plik definiujący topologię main.py (może to potrwać dłużej niż zwykle)
komendą ,,sudo -E mn --custom=main.py --topo mytopo --link tc --mac --switch ovs,protocols=OpenFlow14 --controller=remote,ip=<IP MASZYNY> --arp"
8. Uruchomić na własnym hoście skrypt userInterface.py (to także może chwilę potrwać)

## scriptFiles
Katalog zawiera wszystkie skrypty wykonane w ramach laboratorium oraz pliki zawierające dane potrzebne do ich działania.

-[ ] **graphLinks.json** - plik zawierający strukturę podobną do listy sąsiedztwa (słownik w którym kluczem jest id switcha, a wartością lista zawierająca listy reprezentujące łącza w formacie [połączone urządzenie, bw połączenia, delay połączenia] ) służąca do reprezentacji sieci w formie grafu
-[ ] **portmap.json** - plik zawierający słownik switchy i podłączonych do nich urządzeń, umożliwiający odczytanie, na którym porcie jest podłączony dany switch
- [ ] **flowProcessor.json** - skrypt do przetwarzania ścieżek, zawierający algorytmy znajdowania najlepszeszej ścieżki dla połączenia: najkrótszej pod względem opóźnienia lub najgrubszej pod względem przepustowości, w zależności od stanu sieci. Zawiera też metody do aktualizacji informacji o stanie sieci.
- [ ] **flowToOnos.json** - skrypt pozwalający na wysyłanie instrukcji kierowania pakietów do kontrolera ONOS zgodnie z podaną ścieżką. Posiada też metody do wysyłania ścieżek z pliku i przygotowywania na podstawie ścieżki instrukcji przyjmowanej przez kontroler w formacie json.
- [ ] **main.py** - skrypt definiujący topologię wykorzystywany przez emulator Mininet. Przygotowany w wersji pozwalającej na wczytanie miast i połączeń z pliku.
- [ ] **prep.py** -  skrypt pomocniczy pozwalający na wczytywanie danych w o miastach i łączach w sieci z pliku oraz zapytania do zewnętrznego API o współrzędne miast w celu obliczania odległości między miastami i na jej podstawie opóźnienia oraz zbudowanie modelu sieci w postaci grafu.
- [ ] **userInterface.py** - skrypt będący interfejsem użytkownika w aplikacji do kierowania pakietów.
- [ ] **map.py** - plik pozwalający rysować sieć na mapie na podstawie plików cities i links z wykorzystaniem biblioteki Cartopy
- [ ] **onosFlows.bat** - skrypt pozwalający na wysłanie do ONOSa instrukcji kierowania pakietów w formacie json
- [ ] **OnosAddFlows.sh** - skrypt analogiczny do onosFlows.bat dla systemów UNIX
- [ ] **cities** - plik z listą miast w sieci
- [ ] **links** - plik z listą łączy w sieci
- [ ] **setup.sh** - skrypt, który uruchomiony na masznie wirtualnej, po uruchomieniu serwera http na hoście, pobiera z niego potrzebne do startu naszej sieci mininet pliki oraz biblioteki. Przy uruchomieniu należy podać parametr -h <ip_hosta>

## lab2
Katalog ze skryptami iperf i wynikami testów z laboratorium nr.2
-[ ] **wyniki_aplikacjia** - wyniki testów wykonywanych na połączeniach zestawionych przez przygotowaną aplikację
- [ ] **zad1** - pliki .json definiujące ścieżki zestawiane w zadaniu 1. laboratorium nr.2 oraz wyniki eksperymentów z tego zadania
- [ ] **h1_h2** - pliki .json definiujące sposób kierowania pakietów w eksperymencie na łączu h1-h2 w zad 2 lab 2 oraz polecenia generatora iperf z tego zadania
- [ ] **exp** - katalogi zawierające instrukcje generatora Iperf oraz pliki .json definiujące pakiety.
- [ ] **logs** - pozostałe logi.

## lab1
Katalog ze skryptami iperf i wynikami testów z laboratorium nr.1
- [ ] **pingResults** -  katalog z wynikami testów wykonanych z wykorzystaniem komendy Ping
- [ ] **experiments** - skrypty uruchamiające odpowiednie generatory ruchu Iperf na potrzeby eksperymentów
- [ ] **task4** - wyniki testów z zadania 4. laboratorium nr.1

## logi
Katalog z logami wynikowymi testów
-[ ] **aplikacja** - wyniki testów wykonanych dla sesji zestawionych z wykorzystaniem przygotowanej aplikacji
- [ ] **powtorks** - wyniki powtórzonych testów z laboratorium nr.1
- [ ] **inneLogi** - pozostałe wyniki testów

## images
Katalog z wykonanymi z wykorzystaniem bilbioteki Cartopy mapami sieci
