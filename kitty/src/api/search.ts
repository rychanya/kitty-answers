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

function upload(): Promise<any> {
  return new Promise((res, rej) => {
    AuthClient.getTokenSilently().then((token) => {
      axios
        .put(
          "qa/upload",
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((resp) => res(resp.data))
        .catch((error) => rej(error));
    });
  });
}

export { search, get, upload };
