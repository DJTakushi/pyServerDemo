import neatApi.finDataUpdater as finDataUpdater
import neatApi.weatherUpdater as weatherUpdater

BASEURL = "https://www.takushi.us/"

fd = finDataUpdater.finDataUpdater(BASEURL)
fd.update()

w = weatherUpdater.weatherUpdater(BASEURL)
w.update()

print("done ")
