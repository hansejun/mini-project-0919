export const addHtml = (cafe, reviews, userId) => {
  let avarageRate = 0;

  const handleDelete = (e) => {
    e.preventDefault();

    if (userId && e.target.value)
      $.ajax({
        url: `/api/review/${e.target.value}`,
        method: "DELETE",
        dataType: "text",
        success: function (data) {
          window.location.reload();
        },
      });
  };

  $(".cafe-title").text(cafe.name);
  $(".cafe-intro").text(cafe.content);
  $(".review-count").text(` (${reviews.length})`);
  $(".cafe-image").attr("src", cafe.url);
  $(".detail-address").text(cafe.address);
  reviews.map((review) => {
    avarageRate += Number(review.rate);
    $(".detail-reviews__container").append(
      `<div class="detail-reviews__container-item">
    <div>
      <img class="review-avatar" src="https://avatars.dicebear.com/api/bottts/${
        review._id
      }.svg" />
      <span class="review-name">${review.userId}</span>
    </div>
    <div class="container-item-review">
      <span class="review-createdAt">${dateConversion(review.createdAt)}</span>
      <pre class="review-comment">${review.comment}</pre>
      <div class="review-fn">
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
        ${
          userId == review.userId
            ? `<button class="review-delete" value=${review._id}>삭제</button>`
            : `<button class="review-delete none">삭제</button>`
        }
      </div>
    </div>
  </div>`
    );
  });
  if (avarageRate == 0) {
    $(".cafe-rate").text("0");
  } else {
    $(".cafe-rate").text((avarageRate / reviews.length).toFixed(1));
  }
  const deleteBtns = document.querySelectorAll(".review-delete");
  console.log(deleteBtns);
  deleteBtns.forEach((deleteBtn) => {
    deleteBtn.addEventListener("click", handleDelete);
  });
};

const dateConversion = (date) => {
  const nowDateString = new Date().toISOString().substring(2, 10);
  const nowDate = nowDateString.split("-").map((item) => Number(item));
  const compareDate = date.split("-").map((item) => Number(item));
  if (nowDate[0] > compareDate[0]) {
    return `${nowDate[0] - compareDate[0]}년전`;
  } else if (nowDate[1] > compareDate[1]) {
    return `${nowDate[1] - compareDate[1]}달전`;
  } else if (nowDate[2] > compareDate[2]) {
    return `${nowDate[2] - compareDate[2]}일전`;
  } else {
    return "오늘";
  }
};
