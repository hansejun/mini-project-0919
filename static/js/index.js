import { createReview, getDetail } from "./api.js";
import { addHtml } from "./util/addHtml.js";

let cafe = {};
let reviews = [];
const btns = document.querySelectorAll(".rate-btn");
const rateContainer = document.querySelectorAll(".review-form__rate");
const reviewForm = document.querySelector(".review-form");
let rateValue = 0;
async function start() {
  const data = await getDetail(1);
  cafe = data.data.cafe;
  reviews = data.data.reviews;
  addHtml(cafe, reviews);
}

const handleBtnClick = (e) => {
  e.preventDefault();
  rateValue = Number(e.target.parentElement.value || e.target.value);
  let rateBtns = rateContainer[0].children;

  Array.prototype.forEach.call(rateBtns, (rateBtn, idx) => {
    if (idx + 1 <= rateValue) {
      rateBtn.children[0].classList.remove("gray");
      rateBtn.children[0].classList.add("blue");
    } else {
      rateBtn.children[0].classList.remove("blue");
      rateBtn.children[0].classList.add("gray");
    }
  });
};

const handleSubmit = async (e) => {
  e.preventDefault();
  const sendData = {
    comment: e.target.comment.value,
    createdAt: new Date().toISOString().substring(2, 10),
    rate: rateValue ? rateValue : 1,
    cafeId: cafe.id,
  };
  createReview(sendData);
};

start();

btns.forEach((btn) => {
  btn.addEventListener("click", handleBtnClick);
});

reviewForm.addEventListener("submit", handleSubmit);
