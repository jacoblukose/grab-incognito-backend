import hashlib

def getHashedValue(s, no_of_digits):
    """
    Given a string returns a hashed value limited to number passed 
    """ 
    return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10**no_of_digits