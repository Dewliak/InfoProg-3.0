@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


InfoProg 2021 levelező fordulója, programozói B kategória
 
Készítette: Veres Z. Benedek, Selye János Gimnázium, Komárom

verzió : 3.0 GITHUB EDITION

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


Instaláció szükséges ahhoz, hogy a Pillow modult, ne a számítógépre instalálja, hanem a virtuális
környezetbe. A setup.bat gombra kattintva felinstalálódik a virtuális környezet, instalálás után 
a start.bat kattintva elindul a program.


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


Figyelmeztetés - a zipben található fájloknak, mind egy mappában kell lenniük.

!!A gépen rajta kell lennie valamilyen Python 3 verziónak(ajánlottab a legfrissebb)!!


A programban alapból találhatóak már műsorvezetők, műsorok és műsoridők, hogy joban meg lehessen nézni
a program funkcióit. A képeket a https://thispersondoesnotexist.com/ oldalról töltöttem le.

A .csv fájlokban már szerepelnek adatok.

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Start:
	Indításhoz futtasd le a start.bat fájlt (elindítja a virtuális környezetet és a programot) 

Program használata:
	A program elindulása után, kiválaszhatjuk a lehetőségeinket(Manager,Show,ShowTime,Playlist)
	
	=> MANAGER - itt tudjuk kezelni a műsorvezetőket, add gombal hozzá adhatunk egy új műsorvezetőt, az edit
		     gombbal átírhatjuk egy már létező műsorvezető adatait, a delete gombbal kitörölhetjük.
		     A új dolog hozzáadásánál, vagy a validate gombbal tudjuk ellenőrizni az adatokat, hogy
		     meg felelnek-e a kritérumoknak
	=> SHOW - itt tudjuk kezelni a műsorokat, a gombok ugyanúgy működnek mint az előzőnél

	=> SHOWTIME - itt tujuk kezelni a műsor időket, a gombok ugyanúgy működnek mint az előzőnél.	
	
	=> PLAYLIST - Kiválaszhatunk egy címkét a feltüntettek közül, majd megadjuk mennyi zeneszámot
		      szeretnénk a lejátszási listába, és kiválaszthatjuk hova szeretnénk generálni
		      a lejátszási listát (alapból oda generálja, ahol a program fálja található)

	
	=> EDIT - Az edit mód használata - EDITre kattintáskor (ha már nem a fő menüben vagyunk, azaz a managers,shows, vagy a show times ki van választva)
		elő jön a kezelő felület, ekkor ki kell elöször is választanunk a felső sorból a változtatásra váro tárgy id-ját, ezután a program kitölti
		a megfelelő helyeket és ekkor átírhatjuk azt amit szeretnénk.
	=> ADD - Az add mód használata - ADD gombra kattintáskor(miután már nem a fő menüben vagyunk) elő jön a kezelő felület és beírhatjuk a kívánt adatokat
		a program figyelmeztet, ha a szöveg nem felel meg a kritériumoknak

	



