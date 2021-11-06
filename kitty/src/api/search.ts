import axios from "axios";
import { SearchResult, QA } from "@/api/models";
import { AuthClient } from "@/main";

function search(q: string): Promise<Array<SearchResult>> {
  return new Promise((resolve, reject) => {
    axios
      .get(`qa/search/${q}`)
      .then((resp) => resolve(resp.data))
      .catch((error) => reject(error));
  });
}

function testTask(): Promise<void> {
  return new Promise((resolve, reject) => {
    axios
      .post('qa/test')
      .then((resp) => resolve(resp.data))
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

export { search, get, upload, testTask };
