const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const WS_URL = API_URL.replace(/^http/, "ws") + "/ws/live";

const MAX_RETRIES = 8;
const BASE_DELAY_MS = 1000;

let retries = 0;
let messageCallback = null;
let statusCallback = null;

function notifyStatus(s) {
  if (statusCallback) statusCallback(s);
}

function connect() {
  notifyStatus("connecting");
  const socket = new WebSocket(WS_URL);

  socket.onopen = () => {
    retries = 0;
    notifyStatus("live");
  };

  socket.onmessage = (event) => {
    if (messageCallback) messageCallback(JSON.parse(event.data));
  };

  socket.onclose = () => {
    if (retries >= MAX_RETRIES) {
      notifyStatus("disconnected");
      return;
    }
    notifyStatus("reconnecting");
    const delay = BASE_DELAY_MS * 2 ** retries;
    retries++;
    setTimeout(connect, delay);
  };

  socket.onerror = () => socket.close();
}

connect();

export function subscribe(cb) {
  messageCallback = cb;
}

export function subscribeStatus(cb) {
  statusCallback = cb;
}
