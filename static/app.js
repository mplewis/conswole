ws = new WebSocket("ws://localhost:8765");

const app = new Vue({
  el: "#app",
  methods: {
    submit() {
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
  app.lines += event.data + "<br>";
};
ws.onopen = () => {
  ws.send("print('Hello world!')");
};
