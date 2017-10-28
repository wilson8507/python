import unittest

from circular_buffer import (
    CircularBuffer,
    BufferFullException,
    BufferEmptyException
)


# Tests adapted from `problem-specifications//canonical-data.json` @ v1.0.1

class CircularBufferTest(unittest.TestCase):
    def test_read_empty_buffer(self):
        buf = CircularBuffer(1)
        with self.assertRaises(BufferEmptyException):
            buf.read()

    def test_read_just_written_item(self):
        buf = CircularBuffer(1)
        buf.write('1')
        self.assertEqual(buf.read(), '1')

    def test_write_and_read_back_one_item(self):
        buf = CircularBuffer(1)
        buf.write('1')
        self.assertEqual(buf.read(), '1')
        with self.assertRaises(BufferEmptyException):
            buf.read()

    def test_write_and_read_back_multiple_items_ordered(self):
        buf = CircularBuffer(2)
        buf.write('1')
        buf.write('2')
        self.assertEqual(buf.read(), '1')
        self.assertEqual(buf.read(), '2')

    def test_full_buffer_cant_written(self):
        buf = CircularBuffer(1)
        buf.write('1')
        with self.assertRaises(BufferFullException):
            buf.write('2')

    def test_alternate_write_and_read(self):
        buf = CircularBuffer(1)
        buf.write('1')
        self.assertEqual(buf.read(), '1')
        buf.write('2')
        self.assertEqual(buf.read(), '2')

    def test_read_back_oldest_item(self):
        buf = CircularBuffer(3)
        buf.write('1')
        buf.write('2')
        self.assertEqual(buf.read(), '1')
        buf.write('3')
        self.assertEqual(buf.read(), '2')
        self.assertEqual(buf.read(), '3')

    def test_clearing_buffer(self):
        buf = CircularBuffer(1)
        buf.write('1')
        buf.clear()
        with self.assertRaises(BufferEmptyException):
            buf.read()

    def test_clear_free_buffer_for_write(self):
        buf = CircularBuffer(1)
        buf.write('1')
        buf.clear()
        buf.write('2')
        self.assertEqual(buf.read(), '2')

    def test_clear_does_nothin_empty_buffer(self):
        buf = CircularBuffer(1)
        buf.clear()
        buf.write('1')
        self.assertEqual(buf.read(), '1')

    def test_overwrite_non_full_buffer(self):
        buf = CircularBuffer(2)
        buf.write('1')
        buf.overwrite('2')
        self.assertEqual(buf.read(), '1')
        self.assertEqual(buf.read(), '2')

    def test_overwrite_replaces_oldest_item(self):
        buf = CircularBuffer(2)
        buf.write('1')
        buf.write('2')
        buf.overwrite('3')
        self.assertEqual(buf.read(), '2')
        self.assertEqual(buf.read(), '3')

    def test_write_full_buffer(self):
        buf = CircularBuffer(2)
        buf.write('1')
        buf.write('2')
        with self.assertRaises(BufferFullException):
            buf.write('A')

    def test_over_write_replaces_oldest_remaning_item(self):
        buf = CircularBuffer(3)
        buf.write('1')
        buf.write('2')
        buf.write('3')
        self.assertEqual(buf.read(), '1')
        buf.write('4')
        buf.overwrite('5')
        self.assertEqual(buf.read(), '3')
        self.assertEqual(buf.read(), '4')
        self.assertEqual(buf.read(), '5')


if __name__ == '__main__':
    unittest.main()
