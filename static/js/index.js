import { getDetail } from "./api.js";
import { addHtml } from "./util/addHtml.js";

let cafe = {};
let reviews = [];
let btns = document.querySelectorAll(".rate-btn");
let rateContainer = document.querySelectorAll(".review-form__rate");
let rateValue = 0;
async function start() {
  const data = await getDetail(1);
  cafe = data.data.cafe;
  reviews = data.data.reviews;
  addHtml(cafe, reviews);
}

const handleBtnClick = (e) => {
  e.preventDefault();
  rateValue = Number(e.target.parentElement.value);
  let rateBtns = rateContainer[0].children;
  console.log(rateBtns);

  Array.prototype.forEach.call(rateBtns, (rateBtn, idx) => {
    console.log(idx);
    if (idx + 1 > rateValue) {
      rateBtn.classList.add("blue");
    }
  });
};

start();
btns.forEach((btn) => {
  btn.addEventListener("click", handleBtnClick);
});
