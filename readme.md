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
    Podstawowe przeglądanie wszystkich produktów
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
    Dodawanie produktów
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
    Modyfikowanie produktów
    <code>PATCH /products/{product_id}</code><br>
    W body jest to samo co przy dodawaniu, z tym że wszystkie pola są opcjonalne
  </li>
  <li>
    Usuwanie produktów
    <code>DELETE /products/{product_id}</code><br>
    Powoduje usunięcie produktu z bazy, nie zmniejsza jego ilości
  </li>
</ul>

Uruchomienie aplikacji: <br>
<code>launch api: uvicorn app.main:app --reload</code> <br>

Stworzenie migracji: <br>
<code>create migration: alembic revision --autogenerate -m "migration_description"</code> <br>

Zaaplikowanie migracji: <br>
<code>apply migrations: alembic upgrade head</code>
