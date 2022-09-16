import neatApi.finDataUpdater as finDataUpdater
import neatApi.weatherUpdater as weatherUpdater

fd = finDataUpdater.finDataUpdater()
fd.update()

w = weatherUpdater.weatherUpdater()
w.update()

print("done ")
