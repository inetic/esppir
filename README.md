# My entry project to Arduino/esp8266 programming


    echo '#define WIFI_SSID "MyWiFiSSID"' >  espsrc/wifi_credentials.h
    echo '#define WIFI_PASS "MyWiFiPASS"' >> espsrc/wifi_credentials.h
    cd espsrc
    <PATH_TO_ARDUINO_IDE>/arduino --pref sketchbook.path=`pwd` \
                                  --pref build.path=/tmp/esppir \
                                  --port $tty \
                                  --verbose-build \
                                  --upload ./main.ino

