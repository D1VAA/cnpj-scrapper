import re
import html
import urllib.parse


def decode_email_protection(encoded_email):
    def decode_email(encoded_string):
        try:
            decoded = ""
            key = int(encoded_string[:2], 16)
            for i in range(2, len(encoded_string), 2):
                char_code = int(encoded_string[i:i + 2], 16) ^ key
                decoded += chr(char_code)
            decoded = html.unescape(urllib.parse.unquote(decoded))
            return decoded
        except Exception as e:
            return ""

    pattern = r'<a href="/cdn-cgi/l/email-protection#([a-fA-F0-9]+)">(.+?)</a>'
    matches = re.findall(pattern, encoded_email)
    decoded_emails = []
    for match in matches:
        encoded_string, inner_text = match
        decoded_string = decode_email(encoded_string)
        decoded_emails.append(decoded_string)
    return decoded_emails

def email_extractor(a_email) -> list:
    try:
        for data in a_email:
            href = data['href']
            if 'email-protection#' in href:
                decoded = decode_email_protection(str(data))
        return decoded[0]
    except Exception:
        return 'Não encontrado'