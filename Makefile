build:
	"pip" install cx_freeze requests apnggif
	"python" buildstickerscraper.py build
	"python" buildemojiscraper.py build

clean:
	rm -rf build