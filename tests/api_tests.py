import unittest
import os
import shutil
import json
from urlparse import urlparse
from StringIO import StringIO

import sys; print sys.modules.keys()
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())
        
    def testGetSongs(self):
        """ Test the GET method on /api/songs. Should return a big old dictionary with their      names"""
        
        #Make some songs and files
        filea = models.File(name="test")
        songa = models.Song(file=1)
        fileb = models.File(name="another test")
        songb = models.Song(file=2)
        filec = models.File(name="yet another test")
        songc = models.Song(file=3)
        
        session.add_all([filea, songa, fileb, songb, filec, songc])
        session.commit()
        
        #Call up the list of songs
        response = self.client.get("/api/songs",
                   headers=[("Accept", "application/json")]                                  
                   )
        
        #See that it's returning the right code and the right data type
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        
        #Make sure there's the right number of posts
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)
            
        #Test to see that they're formatted right
        songa = data[0]
        print songa
        self.assertEqual(songa["id"], 1)
        self.assertEqual(songa["file"]["name"], "test")
        
        songb = data[1]
        self.assertEqual(songb["id"], 2)
        self.assertEqual(songb["file"]["name"], "another test")
        
        songc = data[2]
        self.assertEqual(songc["id"], 3)
        self.assertEqual(songc["file"]["name"], "yet another test")
        

