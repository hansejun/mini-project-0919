export const getDetail = async (id) => {
  const response = await (await fetch(`/api/detail/${id}`)).json();
  return response;
};

export const createReview = ({ createdAt, rate, cafeId, comment }) => {
  $.ajax({
    type: "POST",
    url: "/api/review",
    data: { createdAt, rate, cafeId, comment },
    success: function (response) {
      alert(response["msg"]);
      window.location.reload();
    },
  });

  return;
};
