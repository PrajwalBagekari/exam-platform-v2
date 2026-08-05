import axios from "axios";

export const api = axios.create({
  baseURL: "https://pdf-service:8001"
});