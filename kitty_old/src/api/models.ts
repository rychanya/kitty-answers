type answerType = string | Array<string> | { [answer: string]: string };

export interface QA {
  _id: string;
  by: string;
  answers: Array<string>;
  type: string;
  question: string;
  extra_answers: Array<string>;
  correct: answerType;
  incorrect: Array<answerType>;
  incomplete: boolean;
}

export interface SearchGroup {
  type: string;
  question: string;
}

export interface SearchResult {
  _id: SearchGroup;
  data: Array<QA>;
}
