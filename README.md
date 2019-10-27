# SaveOurSpace
<h1> Uruchomienie </h2>

Dla uruchomienia kodu należy mieć zainstalowaną bibliotekę `pygame`
```
 pip install pygame
```
Po tym za pomocą polecenia należy uruchomić plik
```
python game.py
```

<h1>About</h1>
Dawno-dawno temu niektóre Państwa zaczęli wysyłać satelity na orbity, żeby zademonstrować innym swoją moc. Na szczęście okazało się że są to przydatne narzędzia, które można wykorzystać w wielu dziedzinach i na orbicie zaczęło się pojawiać coraz więcej satelitów, które przynosiły ze sobą najróżniejsze wygody. Wszystko musiałoby być dobrze, jednak tkwił w tym haczyk. Zepsute satelity pozostawali na orbicie. Mądrze zrozumieli, że jak pójdzie tak dalej, to grozi nam niebezpieczeństwo i zaprojektowali rakietę, która miała za cel oczyścić kosmos. Udało się !
Okazało się że nie jesteśmy jedyną cywilizacją we wszechświecie która ma taki problem i teraz na ciebie położyła się misja uratować innych !


<h1>Instrukcja</h2>

Kiedy uruchomisz grę przed tobą pojawi się okienko, w którym będzie ci proszono wybrać planetę.
Zmieniać planety możesz za pomocą klawiszów `Right Arrow` oraz `Left Arrow`.
Potwierdzić swój wybór możesz za pomocą `Enter`. Od tego jaką planetę wybierzysz zależą:

- Wysokość na której będziesz startować.
- Ilość przeszkód na twojej drodze
- Jak szybko rakieta będzie się przyspieszać z wyłączonym silnikiem. ( To działa na tej zasadzie, że im cięższa planeta, tym większe przyspieszenie grawitacyjne )

Po wyborze planety będziesz musiał w analogiczny sposób wybrać rakietę. Parametry rakiet:

- Armour -- jaką ilość zetknięć z planetoidami będzie mogła wytrzymać rakieta
- Maneuverability -- sterowność rakiety

Po następnym kliknięciu `Enter` zaczyna się gra.
W prawym górnym rogu będą parametry:

- Odległość do planety
- Prędkość w obecnej chwili
- Safe landing -- maksymalna prędkość jaką musi posiadać rakieta, żeby po dotarciu do planety się nie rozbić.
*Jest liczona za pomocą wzoru `10 * pozostały_armour`*

Parametry w lewym górnym rogu:

- Score - ilość satelitów które udało ci się rozbić
- Armour - ile zetknięć jeszcze może wytrzymać twoja rakieta. *Uwaga!* Zetknięcia z satelitami nie wpływają na armour negatywnie. Naprzeciw, jeżeli uda ci się rozbić niebieską satelitę -- armour zostanie powiększony

<h2>Sterowanie</h2>
Sterowanie przebiega za pomocą strzałek, czyli:

- `Right arrow`,`Left arrow` - żeby poruszać się w strony.
- `Up arrow`, `Down arrow` żeby zwiększać/zmniejszać ciąg silnika ( o tym za chwilę ).

Jak tylko zaczynasz grać, zaczyna działać na ciebie grawitacja. Z tego powodu jeżeli nie będziesz nic robił, to rakieta  rozwinie dużą prędkość i  rozbije się o planetę. I tutaj ci się przyda silnik który możesz regulować !
Zwiększając ciąg silnika, redukujesz wpływ przyspieszenia grawitacyjnego. ( możesz nawet zwiększyć go na tyle, żeby polecić w górę jednak nie ma to większego sensu, bo celą gry jest dolecieć do planety i się nie rozbić ). *Ważne*  Masz nieograniczoną ilość paliwa.

<h2>Poziomy</h2>
Całe pole gry dzieli się na trzy poziomy:

- Pas planetoid -- to wszystko co jest powyżej 15 000 metrów ( odległość nie ma nic wspólnego z życiem :) ). W tym pasie pojawiają się tylko planetoidy. Twoim zadaniem jest unikać ich i starać się utrzymać jak najwięcej armouru do kolejnego poziomu
- Pas satelitów -- faktycznie jest to główna przestrzeń do grania. Tu już zaczynają pojawiać się satelity. Jednak nie wyklucza to tego, że także mogą się pojawić planetoidy, więc musisz uważać.
- Planeta -- miejsce w którym kończy się gra. Musisz ciągłe śledzić za parametrem Safe landing oraz swoją prędkością

<h2>Podsumowanie</h2>
No na koniec.
Twoje główne cele:

- Unikać planetoid
- Niszczyć satelity
- Dobrze się bawić !

Życzę powodzenia!








 


