import axios from "axios";

export const api = axios.create({
  baseURL: "https://pdf2exam.org"
});
