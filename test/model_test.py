from __future__ import absolute_import
import unittest
import os
import time

# required since we leverage custom logging levels
from seedbox import logext as logmgr

# now include what we need to test
import seedbox.model.schema as schema

RESOURCE_PATH = os.getcwd()

class TestModelSchema(unittest.TestCase):
    """
    Tests all aspects of creating the database and its model. 
    Adding data, removing data and fetching data.
    Resetting database and backing up database.
    """
    
    def test_add_torrents(self):
        """
        Test adding torrents to the databases
        """
        # initialize the database and schema details.
        schema.init(RESOURCE_PATH)
        # make sure the table is really empty before we start
        schema.Torrent.clearTable()
        # did not think I would need to do this; hrmmm
        schema.MediaFile.clearTable()

        tornames = ['xxxx.torrent', 'xxxxx5.torrent', 'xxxx10.torrent', 'x1.torrent', 'XXXX10.torrent', 'test2.torrent']

        counter = 0
        # loop through and create the torrents
        for name in tornames:
            counter += 1
            torrent = schema.Torrent(name=name)
            # verify we have an instance
            self.assertIsInstance(torrent, schema.Torrent)
            # verify the defaults are set correctly
            self.assertEqual(torrent.name, name)
            self.assertIsNotNone(torrent.create_date)
            self.assertEqual(torrent.state, 'init')
            self.assertEqual(torrent.retry_count, 0)
            self.assertFalse(torrent.failed)
            self.assertIsNone(torrent.error_msg)
            self.assertFalse(torrent.invalid)
            self.assertFalse(torrent.purged)
            self.assertEqual(len(list(torrent.media_files)), 0)

        # make sure the total list size is the total number we processed
        self.assertEqual(len(tornames), counter)

    def test_add_mediafiles(self):
        """
        Test adding media files to the database
        """
        # initialize the database and schema details
        schema.init(RESOURCE_PATH)
        # make sure the table is really empty before we start
        schema.Torrent.clearTable()
        # did not think I would need to do this; hrmmm
        schema.MediaFile.clearTable()

        # create the torrent
        torrent = schema.Torrent(name='test.torrent')
        mediafiles = ['vid11.mp4', 'vid2.mp4', 'vid3.mp4', 'vid4.mp4', 'vid5.avi']

        counter = 0
        # now create the media files
        for media in mediafiles:
            counter += 1
            (name, ext) = media.split('.')
            media_file = schema.MediaFile(filename=name, file_ext='.'+ext, torrent=torrent)
            self.assertIsInstance(media_file, schema.MediaFile)
            self.assertEqual(media_file.filename, name)
            self.assertEqual(media_file.file_ext, '.'+ext)
            self.assertIsNone(media_file.file_path)
            self.assertEqual(media_file.size, 0)
            self.assertFalse(media_file.compressed)
            self.assertFalse(media_file.synced)
            self.assertFalse(media_file.missing)
            self.assertFalse(media_file.skipped)
            self.assertEqual(media_file.torrent.id, torrent.id)
        
        # make sure the total list size is the total number we processed
        self.assertEqual(len(mediafiles), counter)

    def test_fetch_torrents(self):
        """
        Testing fetching torrents from database
        """
        # initialize the database and schema details.
        schema.init(RESOURCE_PATH)
        # make sure the table is really empty before we start
        schema.Torrent.clearTable()
        # did not think I would need to do this; hrmmm
        schema.MediaFile.clearTable()

        tornames = ['xxxx.torrent', 'xxxxx5.torrent', 'xxxx10.torrent', 'x1.torrent', 'XXXX10.torrent', 'test2.torrent']

        # loop through and create the torrents
        for name in tornames:
            schema.Torrent(name=name)

        # do simple search to get a list of torrents back...default value for failed
        # is always False, so we should get back the same number we just put in.
        search = schema.Torrent.selectBy(failed=False)

        self.assertEqual(len(tornames), len(list(search)))

    def test_fetch_mediafiles(self):
        """
        Testing fetching media files from database
        """
        # initialize the database and schema details
        schema.init(RESOURCE_PATH)
        # make sure the table is really empty before we start
        schema.Torrent.clearTable()
        # did not think I would need to do this; hrmmm
        schema.MediaFile.clearTable()

        # create the torrent
        torrent = schema.Torrent(name='test.torrent')
        mediafiles = ['vid11.mp4', 'vid2.mp4', 'vid3.mp4', 'vid4.mp4', 'vid5.avi']

        # now create the media files
        for media in mediafiles:
            (name, ext) = media.split('.')
            schema.MediaFile(filename=name, file_ext='.'+ext, size=100, torrent=torrent)

        # the torrent should now have a reference to a list of media files
        # and the number should be same as our list above.
        self.assertEqual(len(mediafiles), len(list(torrent.media_files)))

        # we can also search for the media files directly using the torrent
        # and the results should be same as list above
        search = schema.MediaFile.selectBy(torrent=torrent.id)
        results = list(search)
        self.assertEqual(len(mediafiles), len(results))

        # now compare one last time with direct from torrent and via search
        self.assertEqual(len(list(torrent.media_files)), len(results))

    def test_update_torrents(self):
        """
        Testing updating torrents in database
        """
        # initialize the database and schema details
        schema.init(RESOURCE_PATH)
        # make sure the table is really empty before we start
        schema.Torrent.clearTable()
        # did not think I would need to do this; hrmmm
        schema.MediaFile.clearTable()

        # create the torrent
        torrent = schema.Torrent(name='test.torrent')

        torrent.name = 'testX.torrent'
        torrent.state = 'active'
        torrent.retry_count = 5
        torrent.failed = True
        torrent.error_msg = 'error message...blah blah blah'
        torrent.invalid = True
        torrent.purged = True

        self.assertNotEqual(torrent.name, 'test.torrent')
        self.assertEqual(torrent.name, 'testX.torrent')

        self.assertIsNotNone(torrent.create_date)

        self.assertNotEqual(torrent.state, 'init')
        self.assertEqual(torrent.state, 'active')

        self.assertNotEqual(torrent.retry_count, 0)
        self.assertEqual(torrent.retry_count, 5)

        self.assertTrue(torrent.failed)
        self.assertIsNot(torrent.failed, False)

        self.assertIsNotNone(torrent.error_msg)

        self.assertTrue(torrent.invalid)
        self.assertIsNot(torrent.invalid, False)

        self.assertTrue(torrent.purged)
        self.assertIsNot(torrent.purged, False)

        self.assertEqual(len(list(torrent.media_files)), 0)

    def test_update_mediafiles(self):
        """
        Testing updating mediafiles in database
        """
        # initialize the database and schema details
        schema.init(RESOURCE_PATH)
        # make sure the table is really empty before we start
        schema.Torrent.clearTable()
        # did not think I would need to do this; hrmmm
        schema.MediaFile.clearTable()

        # create the torrent
        torrent = schema.Torrent(name='test.torrent')
        other_torrent = schema.Torrent(name='othertest.torrent')

        media_file = schema.MediaFile(filename='video1', file_ext='.avi', torrent=torrent)

        media_file.filename = 'new_video'
        media_file.file_ext = '.mp4'
        media_file.file_path = '/usr/local/download/'
        media_file.size = 500000
        media_file.compressed = True
        media_file.synced = True
        media_file.missing = True
        media_file.skipped = True
        media_file.torrent = other_torrent

        self.assertNotEqual(media_file.filename, 'video1')
        self.assertEqual(media_file.filename, 'new_video')

        self.assertNotEqual(media_file.file_ext, '.avi')
        self.assertEqual(media_file.file_ext, '.mp4')

        self.assertIsNotNone(media_file.file_path)

        self.assertNotEqual(media_file.size, 0)
        self.assertEqual(media_file.size, 500000)

        self.assertTrue(media_file.compressed)
        self.assertIsNot(media_file.compressed, False)

        self.assertTrue(media_file.synced)
        self.assertIsNot(media_file.synced, False)

        self.assertTrue(media_file.missing)
        self.assertIsNot(media_file.missing, False)

        self.assertTrue(media_file.skipped)
        self.assertIsNot(media_file.skipped, False)

        self.assertNotEqual(media_file.torrent.id, torrent.id)
        self.assertEqual(media_file.torrent.id, other_torrent.id)

    def test_delete_torrents(self):
        """
        Testing deleting torrents from database
        """
        # initialize the database and schema details
        schema.init(RESOURCE_PATH)
        # make sure the table is really empty before we start
        schema.Torrent.clearTable()
        # did not think I would need to do this; hrmmm
        schema.MediaFile.clearTable()

        # create the torrent
        torrent = schema.Torrent(name='test.torrent')
        self.assertIsInstance(torrent, schema.Torrent)

        other_torrent = schema.Torrent(name='othertest.torrent')
        self.assertIsInstance(torrent, schema.Torrent)

        schema.Torrent.delete(id=torrent.id)
        
        search = schema.Torrent.selectBy(name='test.torrent')
        # because name is unique, it will always be Zero or One entry
        # so we can use the getOne() feature. By passing in None we avoid
        # get back an exception, and therefore we can check for no torrent
        fetched_torrent = search.getOne(None)
        self.assertIsNone(fetched_torrent)

        schema.Torrent.delete(id=other_torrent.id)

        search = schema.Torrent.selectBy(name='othertest.torrent')
        # because name is unique, it will always be Zero or One entry
        # so we can use the getOne() feature. By passing in None we avoid
        # get back an exception, and therefore we can check for no torrent
        fetched_torrent = search.getOne(None)
        self.assertIsNone(fetched_torrent)

    def test_delete_mediafiles(self):
        """
        Testing deleting media files from database
        """
        # initialize the database and schema details
        schema.init(RESOURCE_PATH)
        # make sure the table is really empty before we start
        schema.Torrent.clearTable()
        # did not think I would need to do this; hrmmm
        schema.MediaFile.clearTable()

        # create the torrent
        torrent = schema.Torrent(name='test.torrent')
        mediafiles = ['vid1.mp4', 'vid2.mp4', 'vid3.mp4']

        media_instances = []
        # now create the media files
        for media in mediafiles:
            (name, ext) = media.split('.')
            media_file = schema.MediaFile(filename=name, file_ext='.'+ext, torrent=torrent)
            self.assertIsInstance(media_file, schema.MediaFile)
            media_instances.append(media_file)

        # loop through the list of media instances we just created above.
        # delete the record in the database, then attempt to fetch that instance
        # back using the name we had given it previously. We should get back
        # None since the record no longer exists.
        for instance in media_instances:
            name = instance.filename
            schema.MediaFile.delete(id=instance.id)
            search = schema.MediaFile.selectBy(filename=name)
            fetched_media = search.getOne(None)
            self.assertIsNone(fetched_media)

    def test_reset_database(self):
        """
        Testing resetting the database
        """
        # might be tough to test this one; would need to figure out how to 
        # close the connection, and therefore the db file in order to actually
        # perform a reset. Since the connection is never externalized by either
        # the framework or by the schema module. We'd have to do some serious hacking
        # and that is just not worth it. So I'll leave this as a placeholder for now.
        self.assertTrue(True)

    def test_backup_database(self):
        """
        Testing backing up the database
        """
        # perform backup
        schema.backup(RESOURCE_PATH)
        
        # capture the current year as a string
        year = time.strftime('%Y')
        files = os.listdir(RESOURCE_PATH)

        # now walk through the list of files in the current directory
        # if the files end with '.db' and start with current year
        # then we have found the backup. Set the found flag and 
        # delete the file so it will not be there next time.
        # if we fail to find it we will fail this test as the
        # flag will still be False.
        found = False
        for item in files:
            (name, ext) = os.path.splitext(item)
            if ext == '.db' and name.startswith(year):
                found = True
                os.remove(os.path.join(RESOURCE_PATH, item))

        self.assertTrue(found)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModelSchema)
    unittest.TextTestRunner(verbosity=2).run(suite)
