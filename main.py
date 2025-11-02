
import pytesseract
import PIL.Image
from PIL import Image
import cv2
import re
import phonenumbers

def get_email(s):
    result = []
    matches = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+", s)
    
    for email in matches:
        parts = email.split('@')
        if len(parts) == 2:
            user, domain = parts
            if '.' not in domain:
                tlds = ['com', 'org', 'net', 'edu', 'gov', 'ca', 'us', 'solutions']
                for tld in tlds:
                    if domain.endswith(tld):
                        domain = domain.replace(tld, f".{tld}")
                        break
            email = f"{user}@{domain}"
        result.append(email)
    
    return result

def get_phone(s):
  phone_numbers = []
  for match in phonenumbers.PhoneNumberMatcher(s, "US"):
    phone_numbers.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
  return phone_numbers

def get_name(s):
  name = []
  count = 0
  for i in s:
    if i == ' ':
      count += 1
      if count == 2:
        break
      name.append(i)
    elif i == ".":
      name.append(i)
      count -= 1
    else:
      name.append(i)
  return ["".join(name)]

def locate_name_coords(name, img):
  boxes = pytesseract.image_to_boxes(img)
  boxes = boxes.splitlines()
  
  
  count = 0
  
  for i in range(len(boxes)):
    parts = boxes[i].split(" ")
    if boxes[i][0] == name[0][count]:
      count += 1
    
    if count > 4:
      x, y = int(parts[1]), int(parts[4])
      break

  return x, y
  

def read_ss():
  image_file = "Tests/test3.png"
  img_ori = PIL.Image.open(image_file)

  width_ori, height_ori = img_ori.size
  img = img_ori.crop((0, height_ori/8, width_ori/4, 800))
  text = pytesseract.image_to_string(img)
  
  #img.show()
  #print(img.size

  #Extraction
  clean = re.sub(r"[^\x00-\x7F]+", " ", text)  # strip weird chars
  clean = re.sub(r"\s+", " ", clean).strip()
  name = get_name(clean)

  ##Locating where the Name
 
  width, height = img.size

  x, y = locate_name_coords(name, img)

  ##Locating Emails and Phone
  img_cut1 = img.crop((0, height - y + 300, x + 200, height - y + 700))
  text1 = pytesseract.image_to_string(img_cut1)
  
  clean1 = re.sub(r"[^\x00-\x7F]+", " ", text1)
  clean1 = re.sub(r"\s+", " ", clean1).strip()

  phones = get_phone(clean1)
  emails = get_email(clean1)

  ##Locating Position
  img_cut2 = img.crop((x - 50, height - y + 10, x + 250, height - y + 40))

  text2 = pytesseract.image_to_string(img_cut2)
  clean2 = re.sub(r"[^\x00-\x7F]+", " ", text2)
  position = re.sub(r"\s+", " ", clean2).strip()

  ##Getting Org
  img_cut3 = img_ori.crop((x + 400, height - y + 100, x + 800, height - y + 160))
  img_cut3.show()
  text3 = pytesseract.image_to_string(img_cut3)
  clean3 = re.sub(r"[^\x00-\x7F]+", " ", text3)
  organization = re.sub(r"\s+", " ", clean3).strip()
 
  print("Names:", name[0])
  print("Phones: ", phones)
  print("Emails: ", emails)
  print("Postion: ", position)
  print("Organization:", organization)

read_ss()


