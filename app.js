ws = new WebSocket("ws://localhost:8765");

const app = new Vue({
  el: "#app",
  methods: {
    submit(event) {
      ws.send(this.input);
      this.input = "";
    },
  },
  data() {
    return {
      input: "",
      lines: "",
    };
  },
});

ws.onmessage = (event) => {
  console.log(event);
  app.lines += event.data + "\n";
};
ws.onopen = () => {
  ws.send("1 + 2 + 3 + 4");
};
