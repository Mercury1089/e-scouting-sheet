import cv2
import qrtools
import csv


def show_webcam(mirror=False):
	tempString = ""
	SETUP_LIST = 'setupList.csv'
	EVENT_LIST = 'eventList.csv'
	inputString = ""
	cam = cv2.VideoCapture(0)
	iAr = []
	file = "test_image.png"
	while True:
		ret_val, img = cam.read()
		camera_capture = img
		if mirror: 
			img = cv2.flip(img, 1)
		cv2.imshow('1089 Scouting Scanner', img)
		if cv2.waitKey(1) == 27: 
			break  # esc to quit
		cv2.imwrite(file, camera_capture)
		qr = qrtools.QR()
		qr.decode(file) 
		if qr.data != "NULL" and qr.data != tempString:
			inputString = qr.data
			iAr = inputString.strip().split(",")
			team=iAr[2]
			match=iAr[1]
			chunks = lambda iAr, n=10: [iAr[i:i+n] for i in range(0, len(iAr), n)]
			with open(SETUP_LIST, 'ab+') as csvfile:
				csvWrite = csv.writer(csvfile, dialect='excel', delimiter=',')
#				print chunks(iAr)
#				print len(iAr)
				csvWrite.writerow(iAr[:7] + iAr[len(iAr)-7:])
			with open(EVENT_LIST, 'ab+') as csvfile:
				csvWrite = csv.writer(csvfile, dialect='excel', delimiter=',')
				setupArr = [team,match]
				newEvent = iAr	
				del newEvent[:7]
				del newEvent[len(newEvent)-7:]
				chunklen = len(chunks(newEvent))
				for i in chunks(newEvent)[:chunklen-1]:
					csvWrite.writerow(i)
			tempString = qr.data
			print "Saved"
		else:
			camera_capture = img
	cv2.destroyAllWindows()

def main():
	show_webcam(mirror=True)

if __name__ == '__main__':
	main()