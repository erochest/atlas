

__version__ = '0.0'
__all__ = [
    'getregentry',
    ]


from _lamcour import decode, encode, error
import codecs as _codecs


class Codec(_codecs.Codec):
    decode = decode
    encode = encode


class StreamWriter(Codec, _codecs.StreamWriter):
    pass


class StreamReader(Codec, _codecs.StreamReader):
    pass


def getregentry():
    return (encode, decode, StreamReader, StreamWriter)

