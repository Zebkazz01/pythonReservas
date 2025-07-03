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