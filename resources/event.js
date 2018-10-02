function EventReceiver(websocket, poller, channels, last_msg, onmessage) {
    this.websocket_path = websocket;
    this.channels = channels;
    this.last_msg = last_msg;
    this.poller_base = poller;
    this.poller_path = poller + channels.join('|');
    if (onmessage)
        this.onmessage = onmessage;
    var receiver = this;

    function init_poll() {
        function long_poll() {
            $.ajax({
                url: receiver.poller_path,
                data: {last: receiver.last_msg},
                success: function (data, status, jqXHR) {
                    receiver.onmessage(data.message);
                    receiver.last_msg = data.id;
                    long_poll();
                },
                error: function (jqXHR, status, error) {
                    if (jqXHR.status == 504)
                        long_poll();
                    else {
                        console.log('Long poll failure: ' + status);
                        console.log(jqXHR);
                        setTimeout(long_poll, 2000);
                    }
                },
                dataType: "json"
            });
        }
        long_poll();
    }

    this.onwsclose = null;
    this.websocket = null;
    init_poll();
}
