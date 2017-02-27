import cv2
import qrtools
import csv


def show_webcam(mirror=False):
	tempString = ""
	SETUP_LIST = 'setupList.csv'
	EVENT_LIST = 'eventList.csv'
	inputString = ""
	cam = cv2.VideoCapture(0)
	while True:
		ret_val, img = cam.read()
		camera_capture = img
		file = "test_image.png"
		if mirror: 
			img = cv2.flip(img, 1)
		cv2.imshow('1089 Scouting Scanner', img)
		if cv2.waitKey(1) == 27: 
			break  # esc to quit
		cv2.imwrite(file, camera_capture)
		qr = qrtools.QR()
		qr.decode("test_image.png") 
		if qr.data != "NULL" and qr.data != tempString:
			inputString = qr.data
			iAr = inputString.strip().split(",")
			chunks = lambda iAr, n=:10 [iAr[i:i+n] for i in range(0, len(iAr), n)]
			with open(SETUP_LIST, 'a+') as csvfile:
				csvWrite = csv.writer(csvfile, dialect='excel', delimiter=',')
#				print chunks(iAr)
#				print len(iAr)
				csvWrite.writerow(iAr[:6] + iAr[len(iAr)-7:])
			with open(EVENT_LIST, 'a+') as csvfile:
				csvWrite = csv.writer(csvfile, dialect='excel', delimiter=',')
				setupArr = [iAr[2],iAr[1]]
				newEvent = iAr
				del newEvent[:6]
				del newEvent[len(newEvent)-7:]
				print len(chunks(newEvent))
				for i in chunks(newEvent):
					csvWrite.writerow(setupArr + i)
			tempString = qr.data
		else:
			camera_capture = img
			file = "test_image.png"
	cv2.destroyAllWindows()

def main():
	show_webcam(mirror=True)

if __name__ == '__main__':
	main()