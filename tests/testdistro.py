#!/usr/bin/env python2.4
from basetest import BaseTest, empty_feed
import sys, tempfile, os, shutil, StringIO
import unittest, logging

sys.path.insert(0, '..')
from zeroinstall.injector import distro, model, qdom

class TestDistro(BaseTest):
	def setUp(self):
		BaseTest.setUp(self)
		self.feed = model.ZeroInstallFeed(empty_feed, local_path = '/empty.xml')

	def tearDown(self):	
		BaseTest.tearDown(self)

	def factory(self, id):
		return self.feed._get_impl(id)

	def testDefault(self):
		host = distro.Distribution()

		host.get_package_info('gimp', self.factory)
		self.assertEquals(self.feed.implementations, {})

	def testDebian(self):
		host = distro._host_distribution

		self.assertEquals(2, len(host.versions))

		host.get_package_info('gimp', self.factory)
		self.assertEquals({}, self.feed.implementations)

		host.get_package_info('python-bittorrent', self.factory)
		self.assertEquals(1, len(self.feed.implementations))
		bittorrent = self.feed.implementations['package:deb:python-bittorrent:3.4.2-10']
		self.assertEquals('3.4.2-10', bittorrent.get_version())

		host.get_package_info('libxcomposite-dev', self.factory)
		self.assertEquals(2, len(self.feed.implementations))
		libxcomposite = self.feed.implementations['package:deb:libxcomposite-dev:0.3.1-1']
		self.assertEquals('0.3.1-1', libxcomposite.get_version())
	
	def testCleanVersion(self):
		self.assertEquals('1', distro.try_cleanup_distro_version('1:0.3.1-1'))
		self.assertEquals('0.3.1-1', distro.try_cleanup_distro_version('0.3.1-1ubuntu0'))

suite = unittest.makeSuite(TestDistro)
if __name__ == '__main__':
	sys.argv.append('-v')
	unittest.main()