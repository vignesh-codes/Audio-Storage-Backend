import requests
from app import app
import unittest
import io
from io import BytesIO

'''
1. create - song, podcast, audiobook
2. create wrong fileType
3. get all data
4. get single name from song, podcast, audiobook
5. put single name from song, podcast, audiobook
6. delete single file
'''

class AudioTest(unittest.TestCase):

    def test_create_song(self):
        tester = app.test_client(self)
        payload = {'name': 'forTest',
                   'fileType':'song',
                   'hostOrAuthor': '',
                   'participentsOrNarrator': '',
                   'music_file': (io.BytesIO(b"Some test file with sample data"), 'forTest.mp3')
                   }
        

        response = tester.post("http://127.0.0.1:5000/data", content_type='multipart/form-data',
                               data=payload)
        self.assertEqual(200, response.status_code)


    def test_create_podcast(self):
        tester = app.test_client(self)
        payload = {'name': 'forTest',
                   'fileType':'podcast',
                   'hostOrAuthor': 'Mr.V',
                   'participentsOrNarrator': 'Sir V',
                   'music_file': (io.BytesIO(b"Some test file with sample data"), 'forTest.mp3')
                   }
        

        response = tester.post("http://127.0.0.1:5000/data", content_type='multipart/form-data',
                               data=payload)
        self.assertEqual(200, response.status_code)


    def test_create_audiobook(self):
        tester = app.test_client(self)
        payload = {'name': 'forTest',
                   'fileType':'audiobook',
                   'hostOrAuthor': 'Mr V',
                   'participentsOrNarrator': 'Sir V',
                   'music_file': (io.BytesIO(b"Some test file with sample data"), 'forTest.mp3')
                   }
        

        response = tester.post("http://127.0.0.1:5000/data", content_type='multipart/form-data',
                               data=payload)
        self.assertEqual(200, response.status_code)
        

    def test_create_with_wrong_song(self):
        tester = app.test_client(self)
        payload = {'name': 'NameLength',
                   'fileType':'song',
                   'hostOrAuthor': '',
                   'participentsOrNarrator': '',
                   'music_file': (io.BytesIO(b"Some test file with sample data"), 'test1.mp3')
                   }
        

        response = tester.post("http://127.0.0.1:5000/data", content_type='multipart/form-data',
                               data=payload)
        self.assertEqual(400, response.status_code)

    def test_create_with_wrong_podcast1(self):
        tester = app.test_client(self)
        payload = {'name': 'Podcast_1hhhhhhhhhhhhhhh',
                'fileType':'podcast',
                
                'music_file': (io.BytesIO(b"Some test file with sample data"), 'test1.mp3')
                }
        

        response = tester.post("http://127.0.0.1:5000/data", content_type='multipart/form-data',
                            data=payload)
        self.assertEqual(400, response.status_code)


    def test_create_with_wrong_podcast2(self):
        tester = app.test_client(self)
        payload = {'name': 'Podcast_1',
                'fileType':'podcast',
                'hostOrAuthor': 'somename',               
                'music_file': (io.BytesIO(b"Some test file with sample data"), 'test1.mp3')
                }
        

        response = tester.post("http://127.0.0.1:5000/data", content_type='multipart/form-data',
                            data=payload)
        self.assertEqual(400, response.status_code)

    def test_create_with_wrong_audiobook(self):
        tester = app.test_client(self)
        payload = {'name': 'Podcast_1',
                'hostOrAuthor': 'somename',               
                'music_file': (io.BytesIO(b"Some test file with sample data"), 'test1.mp3')
                }
        

        response = tester.post("http://127.0.0.1:5000/data", content_type='multipart/form-data',
                            data=payload)
        self.assertEqual(400, response.status_code)

    def test_create_with_wrong_fileType(self):
        tester = app.test_client(self)
        payload = {'name': 'nsw',
                   'fileType':'songs',
                   'hostOrAuthor': 'some',
                   'participentsOrNarrator': 'my.vi',
                   'music_file': (io.BytesIO(b"Some test file with sample data"), 'test1.mp3')
                   }
        

        response = tester.post("http://127.0.0.1:5000/data", content_type='multipart/form-data',
                               data=payload)
        self.assertEqual(400, response.status_code)


    def test_create_with_wrong_fileType(self):
        tester = app.test_client(self)
        payload = {'name': 'nsw',
                   'fileType':'songs',
                   'hostOrAuthor': 'some',
                   'participentsOrNarrator': 'my.vi',
                   'music_file': (io.BytesIO(b"Some test file with sample data"), 'test1.mp3')
                   }
        

        response = tester.post("http://127.0.0.1:5000/data", content_type='multipart/form-data',
                               data=payload)
        self.assertEqual(400, response.status_code)

    def test_get_all(self):
        tester = app.test_client(self)
        
        response = tester.get("http://127.0.0.1:5000/data")
        self.assertEqual(200, response.status_code)   


    def test_get_specific_song(self):
        tester = app.test_client(self)
        
        response = tester.get("http://127.0.0.1:5000/data/info/song/forTest")
        self.assertEqual(200, response.status_code)

    def test_get_specific_podcast(self):
        tester = app.test_client(self)
        
        response = tester.get("http://127.0.0.1:5000/data/info/podcast/forTest")
        self.assertEqual(200, response.status_code)


    def test_get_specific_audiobook(self):
        tester = app.test_client(self)
        
        response = tester.get("http://127.0.0.1:5000/data/info/audiobook/forTest")
        self.assertEqual(200, response.status_code)

    def test_delete_specific_song(self):
        tester = app.test_client(self)
        
        response = tester.delete("http://127.0.0.1:5000/data/info/song/forTest")
        self.assertEqual(400, response.status_code)

    def test_delete_specific_podcast(self):
        tester = app.test_client(self)
        
        response = tester.delete("http://127.0.0.1:5000/data/info/podcast/ss")
        self.assertEqual(400, response.status_code)


    def test_delete_specific_audiobook(self):
        tester = app.test_client(self)
        
        response = tester.delete("http://127.0.0.1:5000/data/info/audiobook/ss")
        self.assertEqual(400, response.status_code)
   

if __name__ == '__main__':
    unittest.main()