#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <map>
#include <string>

class Discovery {
public:
    Discovery() : _rx_buf(256, '\0')
    { }

    void start(uint16_t port)
    {
        _udp.begin(port);
    }

    void add_service(const std::string& key, const std::string& value)
    {
        _map[key] = value;
    }

    void update()
    {
        unsigned packet_size;
        while (packet_size = _udp.parsePacket())
        {
            auto remote_ip   = _udp.remoteIP();
            auto remote_port = _udp.remotePort();

            unsigned len = _udp.read( const_cast<char*>(_rx_buf.c_str())
                                    , _rx_buf.size());

            process_rx_packet(len, remote_ip, remote_port);
        }
    }

    static IPAddress broadcast_addr() {
        return IPAddress((uint32_t)WiFi.localIP() | ~((uint32_t)WiFi.subnetMask()));
    }

    void broadcast(uint16_t port, String msg) {
      _udp.beginPacket(broadcast_addr(), port);
      _udp.write(msg.c_str());
      _udp.endPacket();
    }

private:
    void process_rx_packet(unsigned len, IPAddress remote_ip, uint16_t remote_port)
    {
        std::string s = _rx_buf.substr(0, len);

        if (s != "discover") return;

        for (auto i = _map.begin(); i != _map.end(); ++i) {
            _udp.beginPacket(remote_ip, remote_port);
            _udp.write(i->first.c_str());
            _udp.write(":");
            _udp.write(i->second.c_str());
            if (std::next(i) != _map.end()) {
                _udp.write(" ");
            }
            _udp.endPacket();
        }
    }

private:
    WiFiUDP _udp;
    std::map<std::string, std::string> _map;
    std::string _rx_buf;
};
