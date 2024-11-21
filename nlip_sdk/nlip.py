"""
 *******************************************************************************
 * 
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *******************************************************************************/
"""
# Documentation Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-8b-code-instruct

"""
This file contains the definition of NLIP Message Structures. 

"""

from enum import Enum
from typing import Union

from pydantic import BaseModel

class CaseInsensitiveEnum(str, Enum):
    """ A custom implementation of an enumerated class that is case-insensitive"""
    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None


class AllowedFormats(CaseInsensitiveEnum):
    """
    The values of the format field that are defined by NLIP Specification
    """
    text = "text"
    token = "token"
    structured = "structured"
    binary = "binary"
    location = "location"
    generic = "generic"

class ReservedTokens(CaseInsensitiveEnum):
    """
    The values of the reserved values of subformat when token is format
    - as defined by NLIP Specification
    auth is authentication token 
    conv is conversation id token
    """
    auth = 'authorization'
    conv = 'conversation'

    @classmethod
    def is_reserved(cls, field:str):
        return field is not None and field.lower().startswith((cls.auth, cls.conv))

    @classmethod
    def is_auth(cls, field:str):
        return field is not None and field.lower().startswith(cls.auth)
    
    @classmethod
    def is_conv(cls, field:str):
        return field is not None and field.lower().startswith(cls.conv)
    
    @classmethod
    def get_suffix(cls, field:str, seperator='') -> str:
        if cls.is_auth(field):
            return field[len(cls.auth)+len(seperator):].strip()
        elif cls.is_conv(field):
            return field[len(cls.conv)+len(seperator):].strip()
        else:
            return field


class NLIP_SubMessage(BaseModel):
    """Represents a sub-message in the context of the NLIP protocol.

    Attributes:
        format (AllowedFormats): The format of the sub-message.
        subformat (str): The subformat of the sub-message.
        content (Union[str, dict]): The content of the message. Can be a string or a dictionary. 
        If a dictionary, the content would be encoded as a nested JSON. 
    """
    format: AllowedFormats
    subformat: str
    content: Union[str, dict]

class NLIP_BasicMessage(BaseModel):
    """The Basic Message with no sub-messages in the context of the NLIP protocol.

    Attributes:
        control (bool): whether the message is a control message or not
        format (AllowedFormats): The format of the sub-message.
        subformat (str): The subformat of the sub-message.
        content (Union[str, dict]): The content of the message. Can be a string or a dictionary. 
        If a dictionary, the content would be encoded as a nested JSON. 
    """
    control: bool
    format: str
    subformat: str
    content: Union[str, dict]

class NLIP_Message(BaseModel):
    control: bool
    format: str
    subformat: str
    content: Union[str, dict]
    submessages: list[NLIP_SubMessage] = list()


def nlip_encode_text(message: str, control:bool=False, language:str="english") -> NLIP_BasicMessage:
    """This function encodes a text message into a NLIP BasicMessage object. 
    The function takes three parameters: message (a string representing the text message), 
    control (a boolean indicating whether the message is a control message), 
    and language (a string representing the language of the message). 
    It returns a NLIP BasicMessage object with the specified properties.

    Args:
        message (str): The text content that is to be encoded
        control (bool): if the message is a control command - default False
        language (bool): if the message is a control command - default False
    
    Returns:
        NLIP_BasicMessage: The encoded NLIP message with no submessages.
    """
    
    return NLIP_BasicMessage(
        control=control, format=AllowedFormats.text, subformat=language, content=message
    )


def nlip_extract_field(msg:NLIP_BasicMessage | NLIP_Message | NLIP_SubMessage,format:str, subformat:str = 'None') -> any: 
    """This function extracts the field matching specified format from the message. 
    For a NLIP_Message, only the primary field is checked 
    When the subformat is None, it is not compared. 
    If the subformat is specified, both the format and subformat should match. 

    

    Args:
        msg (NLIP_Message | NLIP_BasicMesssage|NLIP_SubMessage): The input message
        format (str): The format of the message
        subformat (str): The subformat of the message
    
    Returns:
        contents: The content from matching field/subfield or None 
    """

    if msg is None:
        return None
    if isinstance(msg, (NLIP_Message, NLIP_BasicMessage, NLIP_SubMessage)): 
        if msg.format is not None and msg.subformat is not None: 
            if msg.format.lower() == format.lower():
                if subformat is None: 
                    return msg.content
                else: 
                    if subformat.lower() == msg.subformat.lower(): 
                        return msg.content 
    return None


def nlip_extract_field_list(msg: NLIP_BasicMessage | NLIP_SubMessage | NLIP_Message, format:str, subformat:str = None) -> list:
    """This function extracts all the fields of specified format from the message. 
    The extracted fields are put together in a list, each entry corresponding to a submesage
    Note that when the message is a BasicMessage 

    Args:
        msg (NLIP_Message|NLIP_BasicMesssage|NLIP_SubMessage): The input message
        language (str): The subformat of the message
    
    Returns:
        list: A list containing all matching fields in the message. 
    """

    if msg is None:
        return list()
    if isinstance(msg, (NLIP_BasicMessage,NLIP_SubMessage)): 
        field = nlip_extract_field(msg, format, subformat)
        return  list() if field is None else [field]
    else: 
        if isinstance(msg, NLIP_Message):
            field = nlip_extract_field(msg, format, subformat)
            field_list = list() if field is None else [field]
            for submsg in msg.submessages:
                value = nlip_extract_field(submsg, format, subformat)
                if value is not None: 
                    field_list = field_list + [value]
            
            return field_list
    return list()
    
def nlip_extract_text(msg: NLIP_BasicMessage | NLIP_SubMessage | NLIP_Message, language:str = 'english', separator=' ') -> str:
    """This function extracts all text message in given language from a message. 
    The extracted text is a concatanation of all the messages that are included in 
    the submessages (if any) carried as content in the specified language. 

    Args:
        msg (NLIP_Message|NLIP_BasicMesssage|NLIP_SubMessage): The input message
        language (str): The subformat of the message - specify None if language does not matter
        separator (str): The separator to insert 
    
    Returns:
        txt: The combined text.
    """
    if msg is None:
        return ''

    text_list = nlip_extract_field_list(msg,AllowedFormats.text, language)
    if len(text_list) > 0:
        return separator.join(text_list)
    else:
        return ''
