// .cafe-title
// .cafe-rate
// .cafe-intro

// .review-count
// .review-name
// .review-createdAt
// .review-comment
// . review-rate  <i class="fas fa-star"></i>
const cafeTitle = document.querySelector(".cafe-title");
const cafeRate = document.querySelector(".cafe-rate");
const cafeIntro = document.querySelector(".cafe-intro");
const reviewCount = document.querySelector(".review-count");
export const addHtml = (cafe, reviews) => {
  let avarageRate = 0;
  cafeTitle.text = cafe.name;
  cafeIntro.text = cafe.content;
  reviewCount.text = reviews.length;
  console.log(reviews);
  reviews.map((review) => {
    avarageRate += review.rate;
    $(".detail-reviews__container").append(
      `<div class="detail-reviews__container-item">
    <div>
      <img class="review-avatar" src="https://avatars.dicebear.com/api/bottts/${
        review._id
      }.svg" />
      <span class="review-name">${review.userId}</span>
    </div>
    <div class="container-item-review">
      <span class="review-createdAt">${review.createdAt}</span>
      <p class="review-comment">${review.comment}</p>
      <span class="review-rate">
        ${Array(5)
          .fill(1)
          .map((_, idx) => {
            return idx + 1 > Number(review.rate)
              ? '<i class="fas fa-star gray"></i>'
              : '<i class="fas fa-star blue"></i>';
          })
          .join("")}
          
      </span>
    </div>
  </div>`
    );
  });
};
