import axios from "axios";
import { SearchResult, QA } from "@/api/models";

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

export { search, get };
