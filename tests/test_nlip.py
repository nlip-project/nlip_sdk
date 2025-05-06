# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-8b-code-instruct
import unittest
from nlip_sdk.nlip import NLIP_Message, NLIP_SubMessage, NLIP_Factory, AllowedFormats,ReservedTokens

class TestNLIPEncodeText(unittest.TestCase):
    def test_default_values(self):
        expected = NLIP_Message(
            messagetype=None, format=AllowedFormats.text, subformat="english", content="message"
        )
        actual = NLIP_Factory.create_text(content="message",language="english")
        self.assertEqual(expected, actual)

    def test_control_true(self):
        expected = NLIP_Message(
            messagetype= ReservedTokens.control, format=AllowedFormats.text, subformat="english", content="message"
        )
        actual = NLIP_Factory.create_text("message", messagetype= ReservedTokens.control)
        self.assertEqual(expected, actual)

    def test_language_spanish(self):
        expected = NLIP_Message(
            messagetype=None, format=AllowedFormats.text, subformat="spanish", content="message"
        )
        actual = NLIP_Factory.create_text("message", language="spanish")
        self.assertEqual(expected, actual)
    
    def test_def_messagetype(self):
        expected = NLIP_Message(
           format=AllowedFormats.text, subformat="spanish", content="message"
        )
        actual = NLIP_Factory.create_text("message", language="spanish")
        self.assertEqual(expected, actual)

class TestNLIPExtractText(unittest.TestCase):
    def test_basic_message(self):
        msg = NLIP_Message(messagetype=ReservedTokens.control,format=AllowedFormats.text, subformat='English', content='Hello world!')
        self.assertEqual(msg.extract_text(), 'Hello world!')

    def test_case_format(self):
        msg = NLIP_Message(messagetype=ReservedTokens.control,format=AllowedFormats.text, subformat='English', content='Hello world!')
        self.assertEqual(msg.extract_text(language='engLish'), 'Hello world!')

    def test_submessage(self):
        sub = NLIP_SubMessage(format=AllowedFormats.text, content='Goodbye world!', subformat='french')
        self.assertEqual(sub.extract_field(format=AllowedFormats.text,subformat='English'), None)

    def test_message(self):
        sub = NLIP_SubMessage(format=AllowedFormats.text, subformat='English', content='Goodbye world!')
        msg = NLIP_Message(messagetype=None, format=AllowedFormats.text, subformat='english', content='Hello world!', submessages=[sub])
        self.assertEqual(msg.extract_text(), 'Hello world!'+' '+ 'Goodbye world!')


class TestReservedTokens(unittest.TestCase):
    def test_match_auth(self):
        for field in ['authorization', 'Authorization', 'AuthorizatioN:']:
            self.assertEqual(True,ReservedTokens.is_auth(field))
        
    def test_match_conv(self):
        for field in ['conversation', 'conVersation-id', 'Conversation/']:
            self.assertEqual(True, ReservedTokens.is_conv(field))

    def test_suffix(self):
        for field in ['conversation', 'authorization']:
            for seperator in ['','/','-',':','::']:
                for index in [str(25), '3949494']:
                    value = field+seperator + index
                    self.assertEqual(index, ReservedTokens.get_suffix(value,seperator) )


class TestCorrelator(unittest.TestCase):
    def test_correlator(self):
        msg = NLIP_Factory.create_text("Hello")
        conv = "token012345"
        msg.add_conversation_token(conv)
        extract = msg.extract_conversation_token()
        self.assertEqual(conv, extract)



if __name__ == "__main__":
    unittest.main()