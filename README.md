# mine1

Moja zabawa w aplikację chmurową. 
Nie będzie rozwijana do pełnej funkcjonalności - tylko tyle ile będzie mi potrzebne do testów, na jakie akurat nabiorę ochoty.

# możliwe dalsze kroki - _kolejność dowolna_

* dokończyć aktualne oddzielanie deploymentu
* rozwijać oddzielne pomysły w odrębnych gałęziach i ćwiczyć synchronizowanie pomiędzy gałęziami
* deployment gałęzi bocznej - obok produkcyjnej
* HTTPS
* uzupełnienie odpowiedzi API o nagłówki, wyniki/kody błędów
* paging, podzbiór pól
* dodanie autoryzacji API, OAuth2
* WADL, Swagger/OpenAPI
* dodanie nowego frontu opartego o API
* dostęp wskroś chmur
* wariantowy wybór backendu do frontu: albo bezpośrednio albo poprzez API
* utrwalanie danych w sqlite w pamięci
* utrwalanie danych w sqlite na dysku
* utrwalanie danych w prawdziwej bazie jakiś MySQL + jakiś Postgres (rozważania/eksperymenty z izolacją, synchronizacją, etc)
* wiązana z różnymi bazami danych - w tym wskroś chmur
* sesje użytkownika
* testy funckjonalne
* testy dostępności
* format wyniku JSON/XML
* automatyzacja deploymentu dla local+cf+heroku
* dodanie kolejnych chmur openshift+google+? od razu w wersji skryptowej
* test funkcjonalności w trybie A/B
* green/blue i/lub canary deployment


# API

## root

	.../api/v1/...

## kolekcje zasobów
	[częściowo] GET .../games
	[done] POST .../games
	DELETE .../games      

## zasoby
	[done] GET .../games/3654
	DELETE .../games/3654

## działania
	[done] POST .../games/3654/set_flag?x=2&y=3&state=true
	[done] POST .../games/3654/set_flag?x=0&y=2&state=false
	[done] POST .../games/3654/step?x=2&y=3
