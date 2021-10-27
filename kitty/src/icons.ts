import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faUserSecret,
  faJedi,
  faSearch,
  faPaw,
  faCouch,
  faThumbsUp,
  faThumbsDown,
  faTag,
  faUser,
  faFileExcel,
  faCheck,
  faBan,
} from "@fortawesome/free-solid-svg-icons";
import { faTelegram } from "@fortawesome/free-brands-svg-icons";
import { dom } from "@fortawesome/fontawesome-svg-core";

function loadIcons() {
  library.add(
    faUserSecret,
    faJedi,
    faSearch,
    faPaw,
    faTelegram,
    faCouch,
    faThumbsUp,
    faThumbsDown,
    faTag,
    faUser,
    faFileExcel,
    faCheck,
    faBan
  );
  dom.watch();
}

export { loadIcons };
