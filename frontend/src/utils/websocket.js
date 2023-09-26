import AppSettings from "../config";
import { getItem } from "./storage";

export function createWebSocket(fromUserName) {
  const accessToken = getItem("chat_app_access_token");
  const URL = AppSettings.chatURL.split("//")[1];
  return new WebSocket(
    `ws://${URL}/ws/chat/${fromUserName}/?token=${accessToken}`
  );
}
