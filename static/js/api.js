export const getDetail = async (id) => {
  const response = await (await fetch(`/api/detail/${id}`)).json();
  return response;
};
