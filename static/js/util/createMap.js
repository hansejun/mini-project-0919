const mapContainer = document.getElementById("map");
const mapOption = {
  center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
  level: 3, // 지도의 확대 레벨
};
export const createMap = (adress, name) => {
  const map = new kakao.maps.Map(mapContainer, mapOption);
  console.log(map);
  const geocoder = new kakao.maps.services.Geocoder();

  geocoder.addressSearch(
    address ? address : "서울특별시 관악구 행운1길 79 상가 104호",
    function (result, status) {
      // 정상적으로 검색이 완료됐으면
      if (status === kakao.maps.services.Status.OK) {
        var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

        // 결과값으로 받은 위치를 마커로 표시합니다
        var marker = new kakao.maps.Marker({
          map: map,
          position: coords,
        });

        // 인포윈도우로 장소에 대한 설명을 표시합니다
        var infowindow = new kakao.maps.InfoWindow({
          content: `<div style="width:150px;text-align:center;padding:6px 0;">${
            name ? name : "카페"
          }</div>`,
        });
        infowindow.open(map, marker);

        // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
        map.setCenter(coords);
      }
    }
  );
};
