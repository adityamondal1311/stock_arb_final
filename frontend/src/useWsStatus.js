import { useState, useEffect } from "react";
import { subscribeStatus } from "./websocket";

export function useWsStatus() {
  const [status, setStatus] = useState("connecting");
  useEffect(() => {
    subscribeStatus(setStatus);
  }, []);
  return status;
}
