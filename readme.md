## Bardzo proste API stworzone do przeglądania, dodawania, usuwania i modyfikowania produktów simracingowych.

Do stworzenia projektu wykorzystałem:

<ul>
  <li>FastAPI (Python)</li>
  <li>SQLAlchemy jako ORM</li>
  <li>Pydantic do tworzenia modeli</li>
  <li>PostgreSQL jako baza</li>
</ul>

### Endpointy:

<ul>
  <li>
    Podstawowe przeglądanie wszystkich produktów<br>
    <code>GET /products</code><br>
    Dozwolone jest:
    <ul>
      <li>Sortowanie po nazwie, cenie oraz ilości</li>
      <li>Filtrowanie po producencie</li>
      <li>Wybranie strony (paginacja) oraz ilości produktów na stronie (domyślnie tylko 20, poza 20 dozwolone tylko 30 lub 40)</li>
    </ul>
    <code>GET /products?size=30&sort_by=quantity&sort_order=desc&manufacturer=SIMAGIC&page=2</code>
  </li>
  <li>
    Przeglądanie jednego produktu <br>
    <code>GET /products{product_id}</code>
  </li>
  <li>
    Dodawanie produktów<br>
    <code>POST /products</code><br>
    body:
    <pre>
      {
        name: str
        category: 'Wheel base' | 'Pedals' | 'Wheels'
        manufacturer: 'MOZA' | 'SIMAGIC'
        price: float
        quantity: int
      }
    </pre>
    W przypadku dodania produktu, który już istnieje (taka sama nazwa) to wtedy podana przez nas ilość dodawana jest do już istniejącej.
  </li>
  <li>
    Modyfikowanie produktów<br>
    <code>PATCH /products/{product_id}</code><br>
    W body jest to samo co przy dodawaniu, z tym że wszystkie pola są opcjonalne
  </li>
  <li>
    Usuwanie produktów<br>
    <code>DELETE /products/{product_id}</code><br>
    Powoduje usunięcie produktu z bazy, nie zmniejsza jego ilości
  </li>
</ul>

Przed uruchomieniem aplikacji:

<ul>
  <li>
    należy pobrać zależności zapisane w pliku requirements.txt: <br>
    <code>pip install -r requirements.txt</code>
  </li>
  <li>
    Stworzyć bazę <code>products</code> w PostgreSQL
  </li>
  <li>
    W pliku alembic.ini zmienić url bazy: <br>
    <code>sqlalchemy.url = postgresql+psycopg2://<user>:<password>@localhost/products</code>
  </li>
  <li>
    Zaaplikować wszystkie migracje: <br>
    <code>alembic upgrade head</code>
  </li>
</ul>

Uruchomienie aplikacji: <br>
<code>launch api: uvicorn app.main:app --reload</code> <br>
