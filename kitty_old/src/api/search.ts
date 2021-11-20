import axios, { AxiosResponse } from "axios";
import { SearchResult, QA } from "@/api/models";
import { AuthClient } from "@/main";

if (process.env.NODE_ENV == "development") {
  axios.defaults.baseURL = "http://127.0.0.1:8000/";
} else {
  axios.defaults.baseURL = "/api/";
}

function search(q: string): Promise<Array<SearchResult>> {
  return new Promise((resolve, reject) => {
    const data = { q: q }
    axios({
      method: 'post',
      url: 'qa/search',
      data: null,
      params: data
    })
      .then((resp: AxiosResponse<SearchResult[]>) => resolve(resp.data))
      .catch((error) => reject(error));
  });
}

function get(_id: string | string[]): Promise<QA> {
  if (typeof _id !== "string") {
    _id = _id[0];
  }
  return new Promise((resolve, reject) => {
    axios
      .get(`qa/${_id}`)
      .then((resp) => resolve(resp.data))
      .catch((error) => reject(error));
  });
}

function upload(file: File): Promise<any> {
  return new Promise((res, rej) => {
    const form = new FormData();
    form.append("file", file, file.name);
    AuthClient.getTokenSilently().then((token) => {
      axios
        .post("qa/upload", form, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        })
        .then((resp) => res(resp.data))
        .catch((error) => rej(error));
    });
  });
}

function get_upload(id: string | string[]): Promise<any> {
  if (typeof id !== "string") {
    id = id[0];
  }
  return new Promise((res, rej) => {
    AuthClient.getTokenSilently().then((token) => {
      axios
        .post(`qa/upload/${id}`, null, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((resp) => res(resp.data))
        .catch((error) => rej(error));
    });
  });
}

export { search, get, upload, get_upload };
