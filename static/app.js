const SERVER_MAX_UPTIME = 15 * 60 * 1000; // 15 minutes

ws = new WebSocket("ws://localhost:8765");

const app = new Vue({
  el: "#app",
  data() {
    return {
      connected: false,
      remaining: null,
      input: "",
      lines: "",
    };
  },
  methods: {
    submit() {
      ws.send(this.input);
      this.input = "";
    },
  },
});

let expiresAt = null;

ws.onmessage = ({ data }) => {
  uptimeRaw = data.match(/CONSWOLE_SERVER_UPTIME:(.+)/);
  if (uptimeRaw) {
    uptime = Number(uptimeRaw[1]);
    expiresAt = new Date(Date.now() - uptime * 1000 + SERVER_MAX_UPTIME);
    return;
  }
  app.lines += data;
};

ws.onopen = () => {
  app.connected = true;
};
ws.onclose = () => {
  app.connected = false;
  app.input = "Disconnected from server";
};

function leadZero(n) {
  if (n < 10) return `0${n}`;
  return `${n}`;
}

function updateRemaining() {
  function setRemainingMsg(rem) {
    app.remaining = `Session time remaining: ${rem}`;
  }

  if (!expiresAt) {
    setRemainingMsg("unknown");
    return;
  }
  const remSecTotal = (expiresAt - Date.now()) / 1000;
  const remMin = Math.floor(remSecTotal / 60);
  const remSec = Math.floor(remSecTotal % 60);
  setRemainingMsg(`${leadZero(remMin)}:${leadZero(remSec)}`);
}

setInterval(updateRemaining, 500);
updateRemaining();
