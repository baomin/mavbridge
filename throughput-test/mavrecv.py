import time
from optparse import OptionParser
import sys
from pymavlink import mavutil


class MAVRecv:
    conn = None

    def __init__(self, conn):
        self.conn = conn

    def start(self):
        """Receives packets in a loop, prints out total received packets on Ctrl-C"""
        print "Starting receive loop"
        packets_received = 0
        bytes_received = 0
        start_time = time.time()
        while True:
            try:
                m = self.conn.recv_msg()

                if m:
                    try:
                        packets_received += 1
                        buf = m.pack(self.conn.mav)
                        bytes_received += len(buf)
                    except TypeError:
                        pass
                    try:
                        if m.id == 0:
                            #heartbeat was received, send the same message in response
                            self.conn.write(buf)
                    except AttributeError:
                        pass

            except KeyboardInterrupt:
                break

        dt = time.time() - start_time
        print "Total packets received: %d" % packets_received
        print "%.2f messages/second" % (packets_received / dt)
        print "%.2f bytes/second" % (bytes_received / dt)


if __name__ == "__main__":

    usage = "mavrecv.py [options] device"
    parser = OptionParser(usage)

    (opts, args) = parser.parse_args()

    if len(args) < 1:
        print("Usage: %s" % usage)
        sys.exit(1)

    conn = mavutil.mavlink_connection(args[0])
    print "Connected"
    s = MAVRecv(conn)
    s.start()
