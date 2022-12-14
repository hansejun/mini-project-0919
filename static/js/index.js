import { createReview, getDetail } from "./api.js";
import { addHtml } from "./util/addHtml.js";
import { createMap } from "./util/createMap.js";

let cafe = {};
let reviews = [];
let userId = "";
const btns = document.querySelectorAll(".rate-btn");
const rateContainer = document.querySelectorAll(".review-form__rate");
const reviewForm = document.querySelector(".review-form");
const logoutBtn = document.querySelector(".logout");
let rateValue = 0;
const path = location.pathname.substring(8);
const cookieExists = $.cookie("mytoken");
if (!cookieExists) {
  reviewForm.parentElement.classList.add("none");
}

async function start() {
  const data = await getDetail(Number(path));
  console.log(data);
  cafe = data.data.cafe;
  userId = data.data.userId;
  if (cafe.address.length < 3) {
    $(".map-box").addClass("none");
  } else {
    createMap(cafe.address, cafe.name);
  }

  reviews = data.data.reviews;
  addHtml(cafe, reviews, userId || "");
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
  const comment = e.target.comment.value;
  if (comment == "") {
    e.target.comment.focus();
    return;
  } else if (rateValue == 0) {
    alert("평점을 입력해주세요!");
    return;
  }

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

if ($.cookie("mytoken")) {
  $(".login").toggleClass("none");
  $(".join").toggleClass("none");
  $(".logout").toggleClass("none");
}
$(".logout").click(() => {
  $.removeCookie("mytoken", { path: "/" });
  alert("로그아웃!");
  window.location.href = "/";
});
