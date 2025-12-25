export const socket = new WebSocket("ws://localhost:8000/ws/live");

export function subscribe(callback) {
  socket.onmessage = (event) => {
    callback(JSON.parse(event.data));
  };
}
