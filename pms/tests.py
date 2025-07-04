from django.test import TestCase, Client
from django.urls import reverse


class URLsTest(TestCase):
    """Tests básicos para verificar que las URLs estén configuradas correctamente"""
    
    def setUp(self):
        self.client = Client()

    def test_home_url_responds(self):
        """Test que la URL home responda"""
        response = self.client.get('/')
        # Debe responder con 200 o redireccionar (302)
        self.assertIn(response.status_code, [200, 302])

    def test_room_search_url_responds(self):
        """Test que la URL de búsqueda de habitaciones responda"""
        response = self.client.get('/search/room/')
        self.assertIn(response.status_code, [200, 302])

    def test_booking_search_url_responds(self):
        """Test que la URL de búsqueda de reservas responda"""
        response = self.client.get('/search/booking/')
        self.assertIn(response.status_code, [200, 302])

    def test_rooms_url_responds(self):
        """Test que la URL de lista de habitaciones responda"""
        response = self.client.get('/rooms/')
        self.assertIn(response.status_code, [200, 302])

    def test_dashboard_url_responds(self):
        """Test que la URL del dashboard responda"""
        response = self.client.get('/dashboard/')
        self.assertIn(response.status_code, [200, 302])


class BookingSearchViewTest(TestCase):
    """Tests para la vista de búsqueda de reservas"""
    
    def setUp(self):
        self.client = Client()
        
    def test_booking_search_without_filter_redirects(self):
        """Test que sin filtro redirija a home"""
        response = self.client.get('/search/booking/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        
    def test_booking_search_with_filter_returns_response(self):
        """Test que con filtro devuelva una respuesta válida"""
        response = self.client.get('/search/booking/?filter=test')
        # Debe ser 200 (página encontrada) o 302 (redirección)
        self.assertIn(response.status_code, [200, 302])

    def test_booking_search_url_name_works(self):
        """Test que el nombre de URL funcione"""
        url = reverse('booking_search')
        self.assertEqual(url, '/search/booking/')


class RoomSearchViewTest(TestCase):
    """Tests para la vista de búsqueda de habitaciones"""
    
    def setUp(self):
        self.client = Client()
        
    def test_room_search_get_method(self):
        """Test que GET devuelva una respuesta válida"""
        response = self.client.get('/search/room/')
        self.assertIn(response.status_code, [200, 302])
        
    def test_room_search_post_method(self):
        """Test que POST devuelva una respuesta válida"""
        search_data = {
            'checkin': '2024-12-10',
            'checkout': '2024-12-12',
            'guests': '2'
        }
        response = self.client.post('/search/room/', search_data)
        self.assertIn(response.status_code, [200, 302, 400])  # 400 si faltan datos

    def test_room_search_url_name_works(self):
        """Test que el nombre de URL funcione"""
        url = reverse('search')
        self.assertEqual(url, '/search/room/')


class HomeViewTest(TestCase):
    """Tests para la vista home"""
    
    def setUp(self):
        self.client = Client()
        
    def test_home_view_accessible(self):
        """Test que la vista home sea accesible"""
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])

    def test_home_url_name_works(self):
        """Test que el nombre de URL funcione"""
        url = reverse('home')
        self.assertEqual(url, '/')


class DashboardViewTest(TestCase):
    """Tests para la vista dashboard"""
    
    def setUp(self):
        self.client = Client()
        
    def test_dashboard_accessible(self):
        """Test que el dashboard sea accesible"""
        response = self.client.get('/dashboard/')
        self.assertIn(response.status_code, [200, 302])

    def test_dashboard_url_name_works(self):
        """Test que el nombre de URL funcione"""
        url = reverse('dashboard')
        self.assertEqual(url, '/dashboard/')


class RoomsViewTest(TestCase):
    """Tests para la vista de lista de habitaciones"""
    
    def setUp(self):
        self.client = Client()
        
    def test_rooms_list_accessible(self):
        """Test que la lista de habitaciones sea accesible"""
        response = self.client.get('/rooms/')
        self.assertIn(response.status_code, [200, 302])

    def test_rooms_url_name_works(self):
        """Test que el nombre de URL funcione"""
        url = reverse('rooms')
        self.assertEqual(url, '/rooms/')


class URLNamesTest(TestCase):
    """Tests para verificar que todos los nombres de URL funcionen"""
    
    def test_all_basic_url_names_resolve(self):
        """Test que todos los nombres de URL básicos se resuelvan"""
        url_names = [
            'home',
            'search', 
            'booking_search',
            'dashboard',
            'rooms'
        ]
        
        for name in url_names:
            with self.subTest(url_name=name):
                try:
                    url = reverse(name)
                    self.assertIsNotNone(url)
                except Exception as e:
                    self.fail(f"URL name '{name}' failed to resolve: {e}")

    def test_parameterized_url_names_resolve(self):
        """Test que las URLs con parámetros se resuelvan"""
        parameterized_urls = [
            ('booking', {'pk': '1'}),
            ('edit_booking', {'pk': '1'}),
            ('delete_booking', {'pk': '1'}),
            ('room_details', {'pk': '1'})
        ]
        
        for name, kwargs in parameterized_urls:
            with self.subTest(url_name=name):
                try:
                    url = reverse(name, kwargs=kwargs)
                    self.assertIsNotNone(url)
                except Exception as e:
                    self.fail(f"URL name '{name}' failed to resolve: {e}")


class ViewsBasicTest(TestCase):
    """Tests básicos para verificar que las vistas no fallen inmediatamente"""
    
    def setUp(self):
        self.client = Client()

    def test_views_dont_crash(self):
        """Test que las vistas básicas no fallen al cargar"""
        urls_to_test = [
            '/',
            '/search/room/',
            '/rooms/',
            '/dashboard/'
        ]
        
        for url in urls_to_test:
            with self.subTest(url=url):
                try:
                    response = self.client.get(url)
                    # Cualquier respuesta HTTP válida es OK (no un crash)
                    self.assertIsNotNone(response.status_code)
                    self.assertLess(response.status_code, 500)  # No error 500
                except Exception as e:
                    self.fail(f"URL '{url}' caused an exception: {e}")


class RoomFilterTestCase(TestCase):
    """Tests para la funcionalidad de filtro de habitaciones"""
    
    def setUp(self):
        """Configurar datos de prueba"""
        from .models import Room, Room_type
        
        self.client = Client()
        
        # Crear tipos de habitación
        self.room_type_individual = Room_type.objects.create(
            name="Individual",
            price=20.0,
            max_guests=1
        )
        
        self.room_type_doble = Room_type.objects.create(
            name="Doble",
            price=30.0,
            max_guests=2
        )
        
        # Crear habitaciones de prueba
        self.room1 = Room.objects.create(
            room_type=self.room_type_individual,
            name="Room 1.1",
            description="Habitación individual 1.1"
        )
        
        self.room2 = Room.objects.create(
            room_type=self.room_type_individual,
            name="Room 1.2",
            description="Habitación individual 1.2"
        )
        
        self.room3 = Room.objects.create(
            room_type=self.room_type_doble,
            name="Room 2.1",
            description="Habitación doble 2.1"
        )
        
        self.room4 = Room.objects.create(
            room_type=self.room_type_doble,
            name="Suite Executive",
            description="Suite ejecutiva"
        )
    
    def test_rooms_view_without_filter(self):
        """Test que la vista de habitaciones muestra todas las habitaciones sin filtro"""
        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['rooms']), 4)
        self.assertEqual(response.context['room_filter'], '')
    
    def test_rooms_view_with_filter_room_1(self):
        """Test filtro por 'Room 1' debe mostrar Room 1.1 y Room 1.2"""
        response = self.client.get(reverse('rooms'), {'room_filter': 'Room 1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['rooms']), 2)
        self.assertEqual(response.context['room_filter'], 'Room 1')
        
        room_names = [room['name'] for room in response.context['rooms']]
        self.assertIn('Room 1.1', room_names)
        self.assertIn('Room 1.2', room_names)
        self.assertNotIn('Room 2.1', room_names)
        self.assertNotIn('Suite Executive', room_names)
    
    def test_rooms_view_with_filter_suite(self):
        """Test filtro por 'Suite' debe mostrar solo Suite Executive"""
        response = self.client.get(reverse('rooms'), {'room_filter': 'Suite'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['rooms']), 1)
        self.assertEqual(response.context['room_filter'], 'Suite')
        
        room_names = [room['name'] for room in response.context['rooms']]
        self.assertIn('Suite Executive', room_names)
    
    def test_rooms_view_with_filter_no_results(self):
        """Test filtro que no coincide con ninguna habitación"""
        response = self.client.get(reverse('rooms'), {'room_filter': 'NoExiste'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['rooms']), 0)
        self.assertEqual(response.context['room_filter'], 'NoExiste')
    
    def test_rooms_view_filter_case_insensitive(self):
        """Test que el filtro no distingue mayúsculas y minúsculas"""
        response = self.client.get(reverse('rooms'), {'room_filter': 'room 1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['rooms']), 2)
        
        room_names = [room['name'] for room in response.context['rooms']]
        self.assertIn('Room 1.1', room_names)
        self.assertIn('Room 1.2', room_names)
