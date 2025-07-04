from django.test import TestCase, Client
from django.urls import reverse

# Testeo de URLs
class URLsTest(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_home_url_responds(self):
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])

    def test_room_search_url_responds(self):
        response = self.client.get('/search/room/')
        self.assertIn(response.status_code, [200, 302])

    def test_booking_search_url_responds(self):
        response = self.client.get('/search/booking/')
        self.assertIn(response.status_code, [200, 302])

    def test_rooms_url_responds(self):
        response = self.client.get('/rooms/')
        self.assertIn(response.status_code, [200, 302])

    def test_dashboard_url_responds(self):
        response = self.client.get('/dashboard/')
        self.assertIn(response.status_code, [200, 302])

# Testeo de vistas 
class BookingSearchViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        
    def test_booking_search_without_filter_redirects(self):
        response = self.client.get('/search/booking/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        
    def test_booking_search_with_filter_returns_response(self):
        response = self.client.get('/search/booking/?filter=test')
        self.assertIn(response.status_code, [200, 302])

    def test_booking_search_url_name_works(self):
        url = reverse('booking_search')
        self.assertEqual(url, '/search/booking/')


class RoomSearchViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        
    def test_room_search_get_method(self):
        response = self.client.get('/search/room/')
        self.assertIn(response.status_code, [200, 302])
        
    def test_room_search_post_method(self):

        search_data = {
            'checkin': '2024-12-10',
            'checkout': '2024-12-12',
            'guests': '2'
        }
        response = self.client.post('/search/room/', search_data)
        self.assertIn(response.status_code, [200, 302, 400])  

    def test_room_search_url_name_works(self):

        url = reverse('search')
        self.assertEqual(url, '/search/room/')


class HomeViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        
    def test_home_view_accessible(self):
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])

    def test_home_url_name_works(self):
        url = reverse('home')
        self.assertEqual(url, '/')


class DashboardViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        
    def test_dashboard_accessible(self):
        response = self.client.get('/dashboard/')
        self.assertIn(response.status_code, [200, 302])

    def test_dashboard_url_name_works(self):
        url = reverse('dashboard')
        self.assertEqual(url, '/dashboard/')


class RoomsViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        
    def test_rooms_list_accessible(self):
        response = self.client.get('/rooms/')
        self.assertIn(response.status_code, [200, 302])

    def test_rooms_url_name_works(self):
        url = reverse('rooms')
        self.assertEqual(url, '/rooms/')


class URLNamesTest(TestCase):
    
    def test_all_basic_url_names_resolve(self):

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
    
    def setUp(self):
        self.client = Client()

    def test_views_dont_crash(self):

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
                    self.assertIsNotNone(response.status_code)
                    self.assertLess(response.status_code, 500)  
                except Exception as e:
                    self.fail(f"URL '{url}' caused an exception: {e}")


class RoomFilterTestCase(TestCase):
    
    def setUp(self):
        """Configurar datos de prueba"""
        from .models import Room, Room_type
        
        self.client = Client()
        
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

        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['rooms']), 4)
        self.assertEqual(response.context['room_filter'], '')
    
    def test_rooms_view_with_filter_room_1(self):

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

        response = self.client.get(reverse('rooms'), {'room_filter': 'Suite'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['rooms']), 1)
        self.assertEqual(response.context['room_filter'], 'Suite')
        
        room_names = [room['name'] for room in response.context['rooms']]
        self.assertIn('Suite Executive', room_names)
    
    def test_rooms_view_with_filter_no_results(self):

        response = self.client.get(reverse('rooms'), {'room_filter': 'NoExiste'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['rooms']), 0)
        self.assertEqual(response.context['room_filter'], 'NoExiste')
    
    def test_rooms_view_filter_case_insensitive(self):

        response = self.client.get(reverse('rooms'), {'room_filter': 'room 1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['rooms']), 2)
        
        room_names = [room['name'] for room in response.context['rooms']]
        self.assertIn('Room 1.1', room_names)
        self.assertIn('Room 1.2', room_names)
