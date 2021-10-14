import axios from "axios";
import { SearchResult } from "@/api/models";

function search(q: string): Promise<Array<SearchResult>> {
  return new Promise((resolve, reject) => {
    axios
      .get(`qa/search/${q}`)
      .then((resp) => resolve(resp.data))
      .catch((error) => reject(error));
  });
}

export { search };
