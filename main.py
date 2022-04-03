import cv2
from io import BytesIO
from matplotlib import mathtext
import numpy as np
from PIL import Image
import random
import requests

class Tan:

	def __init__(self):
		
		self.mathify = lambda word: word.replace("tan", r"$\frac{\sin}{\cos}$")
		
		self.iterator = self.image_iterator()
		self.next_image()

		cv2.namedWindow("tan")
	
	def get_image_from_word(self, word):

		buffer = BytesIO()
		mathified = self.mathify(word)

		mathtext.math_to_image(mathified, buffer, dpi=300, format="png")
		buffer.seek(0)

		return Image.open(buffer)

	def mainloop(self):

		while True:
			
			cv2.imshow("tan", self.image)
			key = cv2.waitKey(0)
			
			if key == 27: # escape
				break
			else:
				self.next_image()

	def next_image(self):
		self.image = next(self.iterator)

	def image_iterator(self):
		
		wordlist = open("wordlist.txt", "r").read().split()
		filtered = list(filter(lambda word: "tan" in word, wordlist))
		random.shuffle(filtered)

		template = Image.open("template.png")

		for word in filtered:

			base = template.copy()
			
			equation = self.get_image_from_word(word)
			equation.thumbnail((290, 290), Image.ANTIALIAS)
			base.paste(equation, (450 - (equation.size[0]//2), 450-(equation.size[1]//2)))
			try:
				image = self.get_google_img(word)
				if image:
					image.thumbnail((290, 290), Image.ANTIALIAS)
					base.paste(image, (450 - (image.size[0]//2), 150-(image.size[1]//2)))
			except: pass

			opencv_image = cv2.cvtColor(np.array(base), cv2.COLOR_RGB2BGR)

			yield opencv_image

	def get_google_img(self, query):

		url = "https://api.qwant.com/v3/search/images"
		headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
		params = {
			'count': 1,
			'q': query,
			't': 'images',
			'safesearch': 1,
			'locale': 'en_US',
			'offset': 0,
			'device': 'desktop'
		}
		
		res = requests.get(url, params=params, headers=headers)
		result = res.json().get("data").get("result").get("items")

		if len(result) == 0:
			return

		image = Image.open(requests.get(result[0].get("media"), stream=True).raw)
		return image

if __name__ == "__main__":

	tan = Tan()
	tan.mainloop()