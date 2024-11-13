from typing import Union, List
from nlip_sdk import nlip_pb2

def nlip_encode_text(message: str, control: bool = False, language: str = "english") -> nlip_pb2.NLIP_BasicMessage:
    """This function encodes a text message into an NLIP BasicMessage object.
    The function takes three parameters: message (a string representing the text message), 
    control (a boolean indicating whether the message is a control message), 
    and language (a string representing the language of the message). 
    It returns a NLIP BasicMessage object with the specified properties.

    Args:
        message (str): The text content that is to be encoded
        control (bool): if the message is a control command - default False
        language (str): the language of the message - default "english"
    
    Returns:
        NLIP_BasicMessage: The encoded NLIP message with no submessages.
    """
    
    # Create a Protobuf NLIP_BasicMessage object directly
    message_obj = nlip_pb2.NLIP_BasicMessage()
    message_obj.control = control
    message_obj.format = nlip_pb2.AllowedFormats.TEXT  # Use the Protobuf AllowedFormats enum
    message_obj.subformat = language
    message_obj.text_content = message  # Directly set the text content
    
    return message_obj


def nlip_extract_field(msg: Union[nlip_pb2.NLIP_BasicMessage, nlip_pb2.NLIP_Message, nlip_pb2.NLIP_SubMessage], 
                       format: str, subformat: str = 'None') -> Union[str, dict, None]:
    """This function extracts the field matching specified format from the message. 
    For a NLIP_Message, only the primary field is checked. 
    When the subformat is None, it is not compared. 
    If the subformat is specified, both the format and subformat should match.

    Args:
        msg (NLIP_Message | NLIP_BasicMessage | NLIP_SubMessage): The input message
        format (str): The format of the message
        subformat (str): The subformat of the message
    
    Returns:
        contents: The content from matching field/subfield or None 
    """

    if msg is None:
        return None

    # Check the message type and match the format and subformat
    if isinstance(msg, (nlip_pb2.NLIP_Message, nlip_pb2.NLIP_BasicMessage, nlip_pb2.NLIP_SubMessage)):
        if msg.format is not None and msg.subformat is not None:
            if msg.format == nlip_pb2.AllowedFormats[format.upper()]:  # Directly use Protobuf enum comparison
                if subformat is None:
                    return msg.text_content
                else:
                    if subformat.lower() == msg.subformat.lower():
                        return msg.text_content
    return None


def nlip_extract_field_list(msg: Union[nlip_pb2.NLIP_BasicMessage, nlip_pb2.NLIP_SubMessage, nlip_pb2.NLIP_Message], 
                            format: str, subformat: str = None) -> List[Union[str, dict]]:
    """This function extracts all the fields of specified format from the message. 
    The extracted fields are put together in a list, each entry corresponding to a submessage.
    
    Args:
        msg (NLIP_Message | NLIP_BasicMessage | NLIP_SubMessage): The input message
        format (str): The format of the message
        subformat (str): The subformat of the message
    
    Returns:
        list: A list containing all matching fields in the message.
    """

    if msg is None:
        return []

    field_list = []

    # Extract the field from the main message or submessage
    if isinstance(msg, (nlip_pb2.NLIP_BasicMessage, nlip_pb2.NLIP_SubMessage)): 
        field = nlip_extract_field(msg, format, subformat)
        if field is not None:
            field_list.append(field)
    elif isinstance(msg, nlip_pb2.NLIP_Message):
        field = nlip_extract_field(msg, format, subformat)
        if field is not None:
            field_list.append(field)
        
        # Also extract fields from submessages
        for submsg in msg.submessages:
            value = nlip_extract_field(submsg, format, subformat)
            if value is not None:
                field_list.append(value)
    
    return field_list


def nlip_extract_text(msg: Union[nlip_pb2.NLIP_BasicMessage, nlip_pb2.NLIP_SubMessage, nlip_pb2.NLIP_Message], 
                      language: str = 'english', separator: str = ' ') -> str:
    """This function extracts all text messages in the given language from a message. 
    The extracted text is a concatenation of all the messages that are included in 
    the submessages (if any) carried as content in the specified language. 

    Args:
        msg (NLIP_Message | NLIP_BasicMessage | NLIP_SubMessage): The input message
        language (str): The subformat of the message - specify None if language does not matter
        separator (str): The separator to insert between text messages
    
    Returns:
        str: The combined text content from all matching fields
    """
    if msg is None:
        return ''

    text_list = nlip_extract_field_list(msg, 'text', language)
    if text_list:
        return separator.join(text_list)
    else:
        return ''
