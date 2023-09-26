import AppSettings from "../config";
import axios from "axios";

export const auth_request = axios.create({ baseURL: AppSettings.authURL });
export const chat_request = axios.create({ baseURL: AppSettings.chatURL });
