from __future__ import print_function

import io
import unittest

from svgelements import *


class TestElementGroup(unittest.TestCase):

    def test_group_bbox(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewBox="0, 0, 100, 100" height="200" width="200">
                        <g>
                        <rect x="0" y="20" width="50" height="50"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q, width=500, height=500)
        m *= 'scale(2)'
        for e in m.select(lambda e: isinstance(e, Rect)):
            self.assertEqual(e.x, 0)
            self.assertEqual(e.y, 40)
            self.assertEqual(e.width, 100)
            self.assertEqual(e.height, 100)
        self.assertEqual(m.width, 200)
        self.assertEqual(m.height, 200)

    def test_group_2rect(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewBox="0, 0, 100, 100" height="200" width="200">
                        <g>
                        <rect x="0" y="20" width="50" height="50"/>
                        <rect x="0" y="0" width="50" height="50" transform="rotate(45)"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q, width=500, height=500, reify=False)
        m *= 'scale(2)'
        rects = list(m.select(lambda e: isinstance(e, Rect)))
        r0 = rects[0]
        self.assertEqual(r0.implicit_x, 0)
        self.assertEqual(r0.implicit_y, 80)
        self.assertEqual(r0.implicit_width, 200)
        self.assertEqual(r0.implicit_height, 200)
        self.assertEqual(m.width, 200)
        self.assertEqual(m.height, 200)
        self.assertEqual(r0.bbox(), (0.0, 80.0, 200.0, 280.0))
        m.reify()
        self.assertEqual(m.implicit_width, 400)
        self.assertEqual(m.implicit_height, 400)
        r1 = rects[1]
        self.assertEqual(r1.implicit_x, 0)
        self.assertEqual(r1.implicit_y, 0)
        self.assertEqual(r1.implicit_width, 200)
        self.assertEqual(r1.implicit_height, 200)
        print(r1.bbox())
