# -*- coding: utf-8 -*-
#
#    Test all end points are working as expected
#
#    :copyright: 2020 Sonu Kumar
#    :license: BSD-3-Clause
#

import unittest

import pyquery
from django.test import TestCase
from util import TestBase
from django.conf import settings
from error_tracker.django.models import ErrorModel


class ViewTestCase(TestCase, TestBase):
    def test_list_view(self):
        self.get('/value-error')
        self.post('/post-view')
        html = self.get('/dev', follow=True).content
        urls = [node.attrib['href'] for node in pyquery.PyQuery(html)('a')]
        # 2 links for delete operation and 2 links to navigate
        self.assertEqual(len(urls), 2 + 2)

        urls = [node.attrib['href'] for node in pyquery.PyQuery(html)('.view-link')]
        self.assertEqual(len(urls), 2)

    def test_detail_view(self):
        self.get('/value-error')
        html = self.get('/dev', follow=True).content
        url = [node.attrib['href'] for node in pyquery.PyQuery(html)('.view-link')][0]
        response = self.get(url).content
        row = pyquery.PyQuery(response)('.row')[0]
        p = pyquery.PyQuery(row)('p')
        divs = pyquery.PyQuery(row)('.row div')
        self.assertEqual(len(p), 5)
        self.assertEqual(len(divs), 2)

    def test_delete_view(self):
        self.get('/value-error')
        html = self.get('/dev', follow=True).content
        url = [node.attrib['href'] for node in pyquery.PyQuery(html)('.delete')][0]
        self.get(url, follow=True)
        self.assertEqual(len(self.get_exceptions()), 0)

    def test_pagination(self):
        self.get('/value-error')
        exception = self.get_exceptions()[0]
        hashx = exception.hash
        inserted = 0
        i = 0
        while inserted < 20:
            i += 1
            idx = str(i) + hashx[2:]
            inserted += 1
            ErrorModel.create_or_update_entity(idx, exception.host, exception.path,
                                               exception.method, exception.request_data,
                                               exception.exception_name,
                                               exception.traceback)

        response = self.get('/dev', follow=True).content
        urls = [node.attrib['href'] for node in pyquery.PyQuery(response)('a')]
        self.assertEqual(len(urls), settings.EXCEPTION_APP_DEFAULT_LIST_SIZE * 2 + 1)
        self.assertTrue('/dev/?page=2' in urls)

        response = self.get('/dev/?page=2', follow=True).content
        urls = [node.attrib['href'] for node in pyquery.PyQuery(response)('a')]
        self.assertEqual(len(urls), settings.EXCEPTION_APP_DEFAULT_LIST_SIZE * 2 + 2)
        self.assertTrue('/dev/?page=1' in urls)
        self.assertTrue('/dev/?page=3' in urls)

        response = self.get('/dev/?page=5', follow=True).content
        urls = [node.attrib['href'] for node in pyquery.PyQuery(response)('a')]
        self.assertTrue('/dev/?page=4' in urls)

        response = self.get('/dev/?page=6', follow=True).content
        urls = [node.attrib['href'] for node in pyquery.PyQuery(response)('a')]
        self.assertEqual(len(urls), 1)


if __name__ == '__main__':
    unittest.main()
