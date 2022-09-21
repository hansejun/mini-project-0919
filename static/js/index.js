import { getDetail } from "./api.js";
import { addHtml } from "./util/addHtml.js";

let cafe = {};
let reviews = [];

async function start() {
  const data = await getDetail(1);
  cafe = data.data.cafe;
  reviews = data.data.reviews;
  addHtml(cafe, reviews);
}

start();
