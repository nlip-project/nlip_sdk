# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-8b-code-instruct
import unittest
from nlip_sdk import nlip as nlip

class TestNLIPEncodeText(unittest.TestCase):
    def test_default_values(self):
        expected = nlip.NLIP_BasicMessage(
            control=False, format=nlip.AllowedFormats.text, subformat="english", content="message"
        )
        actual = nlip.nlip_encode_text("message")
        self.assertEqual(expected, actual)

    def test_control_true(self):
        expected = nlip.NLIP_BasicMessage(
            control=True, format=nlip.AllowedFormats.text, subformat="english", content="message"
        )
        actual = nlip.nlip_encode_text("message", control=True)
        self.assertEqual(expected, actual)

    def test_language_spanish(self):
        expected = nlip.NLIP_BasicMessage(
            control=False, format=nlip.AllowedFormats.text, subformat="spanish", content="message"
        )
        actual = nlip.nlip_encode_text("message", language="spanish")
        self.assertEqual(expected, actual)

class TestNLIPExtractText(unittest.TestCase):
    def test_basic_message(self):
        msg = nlip.NLIP_BasicMessage(control=True,format=nlip.AllowedFormats.text, subformat='English', content='Hello world!')
        self.assertEqual(nlip.nlip_extract_text(msg), 'Hello world!')

    def test_case_format(self):
        msg = nlip.NLIP_BasicMessage(control=True,format=nlip.AllowedFormats.text, subformat='English', content='Hello world!')
        self.assertEqual(nlip.nlip_extract_text(msg,language='engLish'), 'Hello world!')

    def test_submessage(self):
        sub = nlip.NLIP_SubMessage(format=nlip.AllowedFormats.text, content='Goodbye world!', subformat='french')
        self.assertEqual(nlip.nlip_extract_text(sub), '')

    def test_message(self):
        sub = nlip.NLIP_SubMessage(format=nlip.AllowedFormats.text, subformat='English', content='Goodbye world!')
        msg = nlip.NLIP_Message(control=False, format=nlip.AllowedFormats.text, subformat='english', content='Hello world!', submessages=[sub])
        self.assertEqual(nlip.nlip_extract_text(msg), 'Hello world!'+' '+ 'Goodbye world!')

    def test_none(self):
        self.assertEqual(nlip.nlip_extract_text(None), '')

class TestReservedTokens(unittest.TestCase):
    def test_match_auth(self):
        for field in ['authorization', 'Authorization', 'AuthorizatioN:']:
            self.assertEqual(True,nlip.ReservedTokens.is_auth(field))
        
    def test_match_conv(self):
        for field in ['conversation', 'conVersation-id', 'Conversation/']:
            self.assertEqual(True, nlip.ReservedTokens.is_conv(field))

    def test_suffix(self):
        for field in ['conversation', 'authorization']:
            for seperator in ['','/','-',':','::']:
                for index in [str(25), '3949494']:
                    value = field+seperator + index
                    self.assertEqual(index, nlip.ReservedTokens.get_suffix(value,seperator) )


if __name__ == "__main__":
    unittest.main()