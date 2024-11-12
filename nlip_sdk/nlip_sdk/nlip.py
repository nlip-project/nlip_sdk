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

def nlip_extract_text(msg: NLIP_BasicMessage | NLIP_SubMessage | NLIP_Message, language:str = 'english') -> str:
    """This function extracts all text message in given language from a message. 
    The extracted text is a concatanation of all the messages that are included in 
    the submessages (if any) carried as content in the specified language. 

    Args:
        msg (NLIP_Message|NLIP_BasicMesssage|NLIP_SubMessage): The input message
        language (str): The subformat of the message
    
    Returns:
        txt: The combined text.
    """
    if msg is None:
        return ''
    answer = ''
    if AllowedFormats.text == msg.format and msg.subformat.lower() == language.lower():
        answer = msg.content
    if isinstance(msg, NLIP_BasicMessage) or isinstance(msg,NLIP_SubMessage): 
            return answer
    else:
        for sub in msg.submessages:
            if AllowedFormats.text == sub.format and sub.subformat.lower() == language.lower():
                answer = answer + sub.content
    return answer

