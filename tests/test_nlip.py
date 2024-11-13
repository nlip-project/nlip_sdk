import unittest
from nlip_sdk import nlip_pb2
from nlip_sdk import nlip

class TestNLIPEncodeText(unittest.TestCase):
    def test_default_values(self):
        expected = nlip_pb2.NLIP_BasicMessage(
            control=False, 
            format=nlip_pb2.AllowedFormats.TEXT,  
            subformat="english", 
            text_content="message"
        )
        actual = nlip.nlip_encode_text("message")
        self.assertEqual(expected, actual)

    def test_control_true(self):
        expected = nlip_pb2.NLIP_BasicMessage(
            control=True, 
            format=nlip_pb2.AllowedFormats.TEXT, 
            subformat="english", 
            text_content="message"
        )
        actual = nlip.nlip_encode_text("message", control=True)
        self.assertEqual(expected, actual)

    def test_language_spanish(self):
        expected = nlip_pb2.NLIP_BasicMessage(
            control=False, 
            format=nlip_pb2.AllowedFormats.TEXT, 
            subformat="spanish", 
            text_content="message"
        )
        actual = nlip.nlip_encode_text("message", language="spanish")
        self.assertEqual(expected, actual)

class TestNLIPExtractText(unittest.TestCase):
    def test_basic_message(self):
        msg = nlip_pb2.NLIP_BasicMessage(
            control=True,
            format=nlip_pb2.AllowedFormats.TEXT,
            subformat='English', 
            text_content='Hello world!'
        )
        self.assertEqual(nlip.nlip_extract_text(msg), 'Hello world!')

    def test_case_format(self):
        msg = nlip_pb2.NLIP_BasicMessage(
            control=True,
            format=nlip_pb2.AllowedFormats.TEXT,
            subformat='English', 
            text_content='Hello world!'
        )
        self.assertEqual(nlip.nlip_extract_text(msg, language='engLish'), 'Hello world!')

    def test_submessage(self):
        sub = nlip_pb2.NLIP_SubMessage(
            format=nlip_pb2.AllowedFormats.TEXT, 
            text_content='Goodbye world!', 
            subformat='french'
        )
        self.assertEqual(nlip.nlip_extract_text(sub), '')

    def test_message(self):
        sub = nlip_pb2.NLIP_SubMessage(
            format=nlip_pb2.AllowedFormats.TEXT, 
            subformat='English', 
            text_content='Goodbye world!'
        )
        msg = nlip_pb2.NLIP_Message(
            control=False, 
            format=nlip_pb2.AllowedFormats.TEXT, 
            subformat='english', 
            text_content='Hello world!', 
            submessages=[sub]
        )
        self.assertEqual(nlip.nlip_extract_text(msg), 'Hello world!' + ' ' + 'Goodbye world!')

    def test_none(self):
        self.assertEqual(nlip.nlip_extract_text(None), '')

if __name__ == "__main__":
    unittest.main()
